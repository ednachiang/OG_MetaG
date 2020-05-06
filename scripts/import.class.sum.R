# x = This is your folder where all of your kaiju tables are located
# y = These are the variables you want to group by
# USE ' ' AROUND BOTH X & Y!!!

import.class.sum <- function(x) {
  n <- as.numeric(length(list.files(x)))
  # Initialize output dataframe
  class <- data.frame(matrix(ncol=5, nrow=174))
    # nrow is based on number of classes in sample 3715 because this is the first sample used to populate the dataframe
    # nrow will change as we populate the dataframe with all samples
  colnames(class) <- c("Domain", "Phylum", "Class", "RA_Total_3715", "Reads_3715")
  # I'll populate the dataframe sample-by-sample, so I'm only naming the colnames for the first sample
  
  for (i in 1:n) {
    filename <- list.files(x)[i]
    id <- substr(filename, 1,4)
      # Pull out squirrel ID
    wd <- paste0(x,"/",filename)
      # Path to each csv file
    df <- assign(paste0("class.", id), read.table(wd, sep="\t", header=T))
      # Save each tsv file as a dataframe
    df <- separate(df, col=taxon_name, int=c("Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Empty"), sep=";", remove=T)
      # Separate taxon name by ";" to split into taxonomic levels
      # Last 3 rows will have missing pieces because these are Viruses + unclassified seq's
    df <- df[,-1]
      # Remove first column (file path)
    df <- df[,-3]
      # Remove third column (taxon id)
    df <- df[,-6:-10]
      # remove all taxonomic levels after class
    
    if (i < 2){
      # Fill in output dataframe with 3715 info
      class$Domain <- df$Domain
      class$Phylum <- df$Phylum
      class$Class <- df$Class
      class$RA_Total_3715 <- df$percent
      class$Reads_3715 <- df$reads
    } else {
      colnames(df) <- c(paste0("RA_Total_",id), paste0("Reads_",id), "Domain", "Phylum", "Class")
      # Rename relative abundance and read columns for inclusion in output dataframe
      class <- full_join(class, df, by=c("Domain", "Phylum", "Class"))
      # This joins the output dataframe and sample dataframe by matching the Domain, Phylum, & Class columns
    }
  }
  
# Replace NA's in read column with 0  
  class$Reads_3715 <- replace_na(class$Reads_3715, replace=0)
  class$Reads_3717 <- replace_na(class$Reads_3717, replace=0)
  class$Reads_3723 <- replace_na(class$Reads_3723, replace=0)
  class$Reads_3733 <- replace_na(class$Reads_3733, replace=0)
  class$Reads_3734 <- replace_na(class$Reads_3734, replace=0)
  class$Reads_3744 <- replace_na(class$Reads_3744, replace=0)
  class$Reads_3772 <- replace_na(class$Reads_3772, replace=0)
  class$Reads_3773 <- replace_na(class$Reads_3773, replace=0)
  class$Reads_3775 <- replace_na(class$Reads_3775, replace=0)
  
  # Update unclassified sequences based on domain count total unclassified
  class[which(class$Domain == "unclassified"),3:20] <- c(0, 4515088, 0, 7511409, 0, 5341407, 0, 5784901, 0, 8807662, 0, 6258991, 0, 4868461, 0, 7159963, 0, 6928969)
  
  # Add phylum name for Viruses/Unclassified sequences
  class$Phylum[which(class$Domain == "unclassified")] <- "Unclassified"
  class$Phylum[which(class$Domain == "Viruses")] <- "Virus"
  
  # Add class name for Viruses/Unclassified sequences
  class$Class[which(class$Domain == "unclassified")] <- "Unclassified"
  class$Class[which(class$Domain == "Viruses")] <- "Virus"
  
  # Remove misc unclassified row
  class <- class[-which(class$Domain == "cannot be assigned to a (non-viral) class"),]
  
  # Recalculate total relative abundances (RA) (divided by total reads)
  class$RA_Total_3715 <- as.numeric((class$Reads_3715/11754963)*100)
  class$RA_Total_3717 <- as.numeric((class$Reads_3717/14842572)*100)
  class$RA_Total_3723 <- as.numeric((class$Reads_3723/11337484)*100)
  class$RA_Total_3733 <- as.numeric((class$Reads_3733/11744317)*100)
  class$RA_Total_3734 <- as.numeric((class$Reads_3734/16029927)*100)
  class$RA_Total_3744 <- as.numeric((class$Reads_3744/11768188)*100)
  class$RA_Total_3772 <- as.numeric((class$Reads_3772/10611480)*100)
  class$RA_Total_3773 <- as.numeric((class$Reads_3773/12495850)*100)
  class$RA_Total_3775 <- as.numeric((class$Reads_3775/12974479)*100)
  
  # Recalculate classified relative abundances (RA) (divided by classified reads)
  class$RA_Classified_3715 <- as.numeric((class$Reads_3715/7239875)*100)
  class$RA_Classified_3717 <- as.numeric((class$Reads_3717/7331163)*100)
  class$RA_Classified_3723 <- as.numeric((class$Reads_3723/5996077)*100)
  class$RA_Classified_3733 <- as.numeric((class$Reads_3733/5959416)*100)
  class$RA_Classified_3734 <- as.numeric((class$Reads_3734/7222265)*100)
  class$RA_Classified_3744 <- as.numeric((class$Reads_3744/5509197)*100)
  class$RA_Classified_3772 <- as.numeric((class$Reads_3772/5743019)*100)
  class$RA_Classified_3773 <- as.numeric((class$Reads_3773/5335887)*100)
  class$RA_Classified_3775 <- as.numeric((class$Reads_3775/6045510)*100)

  
  # Create new dataframe to prepare for summary
  class.prep <- data.frame(matrix(ncol=8, nrow=(nrow(class)*9)))
  colnames(class.prep) <- c("Phylum", "Class", "Total_Relative_Abundance", "Classified_Relative_Abundance", "Sample", "Season", "Sex", "Diet")
  class.prep$Phylum <- rep(class$Phylum, 9)
  class.prep$Class <- rep(class$Class, 9)
  
  # Add in Total Rel Abund
  class.prep$Total_Relative_Abundance[1:nrow(class)] <- class$RA_Total_3715
  class.prep$Total_Relative_Abundance[(nrow(class)+1):(nrow(class)*2)] <- class$RA_Total_3717
  class.prep$Total_Relative_Abundance[((nrow(class)*2)+1):(nrow(class)*3)] <- class$RA_Total_3723
  class.prep$Total_Relative_Abundance[((nrow(class)*3)+1):(nrow(class)*4)] <- class$RA_Total_3733
  class.prep$Total_Relative_Abundance[((nrow(class)*4)+1):(nrow(class)*5)] <- class$RA_Total_3734
  class.prep$Total_Relative_Abundance[((nrow(class)*5)+1):(nrow(class)*6)] <- class$RA_Total_3744
  class.prep$Total_Relative_Abundance[((nrow(class)*6)+1):(nrow(class)*7)] <- class$RA_Total_3772
  class.prep$Total_Relative_Abundance[((nrow(class)*7)+1):(nrow(class)*8)] <- class$RA_Total_3773
  class.prep$Total_Relative_Abundance[((nrow(class)*8)+1):(nrow(class)*9)] <- class$RA_Total_3775
  
  # Add in Classified Rel Abund
  class.prep$Classified_Relative_Abundance[1:nrow(class)] <- class$RA_Classified_3715
  class.prep$Classified_Relative_Abundance[(nrow(class)+1):(nrow(class)*2)] <- class$RA_Classified_3717
  class.prep$Classified_Relative_Abundance[((nrow(class)*2)+1):(nrow(class)*3)] <- class$RA_Classified_3723
  class.prep$Classified_Relative_Abundance[((nrow(class)*3)+1):(nrow(class)*4)] <- class$RA_Classified_3733
  class.prep$Classified_Relative_Abundance[((nrow(class)*4)+1):(nrow(class)*5)] <- class$RA_Classified_3734
  class.prep$Classified_Relative_Abundance[((nrow(class)*5)+1):(nrow(class)*6)] <- class$RA_Classified_3744
  class.prep$Classified_Relative_Abundance[((nrow(class)*6)+1):(nrow(class)*7)] <- class$RA_Classified_3772
  class.prep$Classified_Relative_Abundance[((nrow(class)*7)+1):(nrow(class)*8)] <- class$RA_Classified_3773
  class.prep$Classified_Relative_Abundance[((nrow(class)*8)+1):(nrow(class)*9)] <- class$RA_Classified_3775
  
  # Add in Sample
  class.prep$Sample[1:nrow(class)] <- rep("3715", nrow(class))
  class.prep$Sample[(nrow(class)+1):(nrow(class)*2)] <- rep("3717", nrow(class))
  class.prep$Sample[((nrow(class)*2)+1):(nrow(class)*3)] <- rep("3723", nrow(class))
  class.prep$Sample[((nrow(class)*3)+1):(nrow(class)*4)] <- rep("3733", nrow(class))
  class.prep$Sample[((nrow(class)*4)+1):(nrow(class)*5)] <- rep("3734", nrow(class))
  class.prep$Sample[((nrow(class)*5)+1):(nrow(class)*6)] <- rep("3744", nrow(class))
  class.prep$Sample[((nrow(class)*6)+1):(nrow(class)*7)] <- rep("3772", nrow(class))
  class.prep$Sample[((nrow(class)*7)+1):(nrow(class)*8)] <- rep("3773", nrow(class))
  class.prep$Sample[((nrow(class)*8)+1):(nrow(class)*9)] <- rep("3775", nrow(class))
  
  # Add in Season
  class.prep$Season[1:nrow(class)] <- rep("Summer", nrow(class))
  class.prep$Season[(nrow(class)+1):(nrow(class)*2)] <- rep("Summer", nrow(class))
  class.prep$Season[((nrow(class)*2)+1):(nrow(class)*3)] <- rep("Winter", nrow(class))
  class.prep$Season[((nrow(class)*3)+1):(nrow(class)*4)] <- rep("Winter", nrow(class))
  class.prep$Season[((nrow(class)*4)+1):(nrow(class)*5)] <- rep("Spring", nrow(class))
  class.prep$Season[((nrow(class)*5)+1):(nrow(class)*6)] <- rep("Summer", nrow(class))
  class.prep$Season[((nrow(class)*6)+1):(nrow(class)*7)] <- rep("Winter", nrow(class))
  class.prep$Season[((nrow(class)*7)+1):(nrow(class)*8)] <- rep("Spring", nrow(class))
  class.prep$Season[((nrow(class)*8)+1):(nrow(class)*9)] <- rep("Spring", nrow(class))
  class.prep$Season <- ordered(class.prep$Season, levels=c("Summer", "Winter", "Spring"))

  # Add in Sex
  class.prep$Sex[1:nrow(class)] <- rep("Female", nrow(class))
  class.prep$Sex[(nrow(class)+1):(nrow(class)*2)] <- rep("Female", nrow(class))
  class.prep$Sex[((nrow(class)*2)+1):(nrow(class)*3)] <- rep("Male", nrow(class))
  class.prep$Sex[((nrow(class)*3)+1):(nrow(class)*4)] <- rep("Female", nrow(class))
  class.prep$Sex[((nrow(class)*4)+1):(nrow(class)*5)] <- rep("Male", nrow(class))
  class.prep$Sex[((nrow(class)*5)+1):(nrow(class)*6)] <- rep("Male", nrow(class))
  class.prep$Sex[((nrow(class)*6)+1):(nrow(class)*7)] <- rep("Male", nrow(class))
  class.prep$Sex[((nrow(class)*7)+1):(nrow(class)*8)] <- rep("Female", nrow(class))
  class.prep$Sex[((nrow(class)*8)+1):(nrow(class)*9)] <- rep("Male", nrow(class))
  
  # Add in Diet
  class.prep$Diet[1:nrow(class)] <- rep("Feeding", nrow(class))
  class.prep$Diet[(nrow(class)+1):(nrow(class)*2)] <- rep("Feeding", nrow(class))
  class.prep$Diet[((nrow(class)*2)+1):(nrow(class)*3)] <- rep("Fasting", nrow(class))
  class.prep$Diet[((nrow(class)*3)+1):(nrow(class)*4)] <- rep("Fasting", nrow(class))
  class.prep$Diet[((nrow(class)*4)+1):(nrow(class)*5)] <- rep("Feeding", nrow(class))
  class.prep$Diet[((nrow(class)*5)+1):(nrow(class)*6)] <- rep("Feeding", nrow(class))
  class.prep$Diet[((nrow(class)*6)+1):(nrow(class)*7)] <- rep("Fasting", nrow(class))
  class.prep$Diet[((nrow(class)*7)+1):(nrow(class)*8)] <- rep("Feeding", nrow(class))
  class.prep$Diet[((nrow(class)*8)+1):(nrow(class)*9)] <- rep("Feeding", nrow(class))
  
  # Summarize dataframe
  class.sum <- class.prep %>%
    group_by(Season, Phylum, Class) %>%
    summarize(Total_Mean = mean(Total_Relative_Abundance),
              Total_SD = sd(Total_Relative_Abundance),
              Total_SE = se(Total_Relative_Abundance),
              Classified_Mean = mean(Classified_Relative_Abundance),
              Classified_SD= sd(Classified_Relative_Abundance),
              Classified_SE = se(Classified_Relative_Abundance))
  
  return(class.sum)  
}