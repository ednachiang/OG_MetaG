# x = This is your folder where all of your kaiju tables are located
# y = These are the variables you want to group by
# USE ' ' AROUND BOTH X & Y!!!

import.phylum.sum <- function(x) {
  n <- as.numeric(length(list.files(x)))
  # Initialize output dataframe
  phylum <- data.frame(matrix(ncol=4, nrow=170))
  colnames(phylum) <- c("Domain", "Phylum", "RA_Total_3715", "Reads_3715")
  # I'll populate the dataframe sample-by-sample, so I'm only naming the colnames for the first sample
  
  for (i in 1:n) {
    filename <- list.files(x)[i]
    id <- substr(filename, 1,4)
    # Pull out squirrel ID
    wd <- paste0(x,"/",filename)
    # Path to each csv file
    df <- assign(paste0("phylum.", id), read.table(wd, sep="\t", header=T))
    # Save each tsv file as a dataframe
    df <- separate(df, col=taxon_name, int=c("Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Empty"), sep=";", remove=T)
    # Separate taxon name by ";" to split into taxonomic levels
    # Last 3 rows will have missing pieces because these are Viruses + unclassified seq's
    df <- df[,-1]
    # Remove first column (file path)
    df <- df[,-3]
    # Remove third column (taxon id)
    df <- df[,-5:-10]
    # remove all taxonomic levels after phylum
    
    if (i < 2){
      # Fill in output dataframe with 3715 info
      phylum$Domain <- df$Domain
      phylum$Phylum <- df$Phylum
      phylum$RA_Total_3715 <- df$percent
      phylum$Reads_3715 <- df$reads
    } else {
      colnames(df) <- c(paste0("RA_Total_",id), paste0("Reads_",id), "Domain", "Phylum")
      # Rename relative abundance and read columns for inclusion in output dataframe
      phylum <- full_join(phylum, df, by=c("Domain", "Phylum"))
      # This joins the output dataframe and sample dataframe by matching the Domain and Phylum columns
    }
  }
  
  # Replace NA's in read column with 0  
  phylum$Reads_3715 <- replace_na(phylum$Reads_3715, replace=0)
  phylum$Reads_3717 <- replace_na(phylum$Reads_3717, replace=0)
  phylum$Reads_3723 <- replace_na(phylum$Reads_3723, replace=0)
  phylum$Reads_3733 <- replace_na(phylum$Reads_3733, replace=0)
  phylum$Reads_3734 <- replace_na(phylum$Reads_3734, replace=0)
  phylum$Reads_3744 <- replace_na(phylum$Reads_3744, replace=0)
  phylum$Reads_3772 <- replace_na(phylum$Reads_3772, replace=0)
  phylum$Reads_3773 <- replace_na(phylum$Reads_3773, replace=0)
  phylum$Reads_3775 <- replace_na(phylum$Reads_3775, replace=0)
  
  # Update unclassified sequences based on domain count total unclassified
  phylum[which(phylum$Domain == "unclassified",),3:20] <- c(0, 4515088, 0, 7511409, 0, 5341407, 0, 5784901, 0, 8807662, 0, 6258991, 0, 4868461, 0, 7159963, 0, 6928969)
  
  # Add phylum name for Viruses/Unclassified sequences
  phylum$Phylum[which(phylum$Domain == "unclassified")] <- "Unclassified"
  phylum$Phylum[which(phylum$Domain == "Viruses")] <- "Virus"
  
  # Remove misc unclassified row
  phylum <- phylum[-which(phylum$Domain == "cannot be assigned to a (non-viral) phylum"),]
  
  # Recalculate total relative abundances (RA) (divded by total reads)
  phylum$RA_Total_3715 <- as.numeric((phylum$Reads_3715/11754963)*100)
  phylum$RA_Total_3717 <- as.numeric((phylum$Reads_3717/14842572)*100)
  phylum$RA_Total_3723 <- as.numeric((phylum$Reads_3723/11337484)*100)
  phylum$RA_Total_3733 <- as.numeric((phylum$Reads_3733/11744317)*100)
  phylum$RA_Total_3734 <- as.numeric((phylum$Reads_3734/16029927)*100)
  phylum$RA_Total_3744 <- as.numeric((phylum$Reads_3744/11768188)*100)
  phylum$RA_Total_3772 <- as.numeric((phylum$Reads_3772/10611480)*100)
  phylum$RA_Total_3773 <- as.numeric((phylum$Reads_3773/12495850)*100)
  phylum$RA_Total_3775 <- as.numeric((phylum$Reads_3775/12974479)*100)
  
  # Recalculate classified relative abundances (RA) (divded by classified reads)
  phylum$RA_Classified_3715 <- as.numeric((phylum$Reads_3715/7239875)*100)
  phylum$RA_Classified_3717 <- as.numeric((phylum$Reads_3717/7331163)*100)
  phylum$RA_Classified_3723 <- as.numeric((phylum$Reads_3723/5996077)*100)
  phylum$RA_Classified_3733 <- as.numeric((phylum$Reads_3733/5959416)*100)
  phylum$RA_Classified_3734 <- as.numeric((phylum$Reads_3734/7222265)*100)
  phylum$RA_Classified_3744 <- as.numeric((phylum$Reads_3744/5509197)*100)
  phylum$RA_Classified_3772 <- as.numeric((phylum$Reads_3772/5743019)*100)
  phylum$RA_Classified_3773 <- as.numeric((phylum$Reads_3773/5335887)*100)
  phylum$RA_Classified_3775 <- as.numeric((phylum$Reads_3775/6045510)*100)

  
  # Create new dataframe to prepare for summary
  phylum.prep <- data.frame(matrix(ncol=7, nrow=(nrow(phylum)*9)))
  colnames(phylum.prep) <- c("Phylum", "Total_Relative_Abundance", "Classified_Relative_Abundance", "Sample", "Season", "Sex", "Diet")
  phylum.prep$Phylum <- (rep(phylum$Phylum, 9))
  
  # Add in Total Rel Abund
  phylum.prep$Total_Relative_Abundance[1:nrow(phylum)] <- phylum$RA_Total_3715
  phylum.prep$Total_Relative_Abundance[(nrow(phylum)+1):(nrow(phylum)*2)] <- phylum$RA_Total_3717
  phylum.prep$Total_Relative_Abundance[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- phylum$RA_Total_3723
  phylum.prep$Total_Relative_Abundance[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- phylum$RA_Total_3733
  phylum.prep$Total_Relative_Abundance[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- phylum$RA_Total_3734
  phylum.prep$Total_Relative_Abundance[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- phylum$RA_Total_3744
  phylum.prep$Total_Relative_Abundance[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- phylum$RA_Total_3772
  phylum.prep$Total_Relative_Abundance[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- phylum$RA_Total_3773
  phylum.prep$Total_Relative_Abundance[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- phylum$RA_Total_3775
  
  # Add in Classified Rel Abund
  phylum.prep$Classified_Relative_Abundance[1:nrow(phylum)] <- phylum$RA_Classified_3715
  phylum.prep$Classified_Relative_Abundance[(nrow(phylum)+1):(nrow(phylum)*2)] <- phylum$RA_Classified_3717
  phylum.prep$Classified_Relative_Abundance[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- phylum$RA_Classified_3723
  phylum.prep$Classified_Relative_Abundance[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- phylum$RA_Classified_3733
  phylum.prep$Classified_Relative_Abundance[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- phylum$RA_Classified_3734
  phylum.prep$Classified_Relative_Abundance[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- phylum$RA_Classified_3744
  phylum.prep$Classified_Relative_Abundance[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- phylum$RA_Classified_3772
  phylum.prep$Classified_Relative_Abundance[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- phylum$RA_Classified_3773
  phylum.prep$Classified_Relative_Abundance[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- phylum$RA_Classified_3775
  
  # Add in Sample
  phylum.prep$Sample[1:nrow(phylum)] <- rep("3715", 198)
  phylum.prep$Sample[(nrow(phylum)+1):(nrow(phylum)*2)] <- rep("3717", 198)
  phylum.prep$Sample[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- rep("3723", 198)
  phylum.prep$Sample[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- rep("3733", 198)
  phylum.prep$Sample[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- rep("3734", 198)
  phylum.prep$Sample[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- rep("3744", 198)
  phylum.prep$Sample[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- rep("3772", 198)
  phylum.prep$Sample[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- rep("3773", 198)
  phylum.prep$Sample[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- rep("3775", 198)
  
  # Add in Season
  phylum.prep$Season[1:nrow(phylum)] <- rep("Summer", 198)
  phylum.prep$Season[(nrow(phylum)+1):(nrow(phylum)*2)] <- rep("Summer", 198)
  phylum.prep$Season[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- rep("Winter", 198)
  phylum.prep$Season[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- rep("Winter", 198)
  phylum.prep$Season[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- rep("Spring", 198)
  phylum.prep$Season[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- rep("Summer", 198)
  phylum.prep$Season[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- rep("Winter", 198)
  phylum.prep$Season[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- rep("Spring", 198)
  phylum.prep$Season[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- rep("Spring", 198)
  phylum.prep$Season <- ordered(phylum.prep$Season, levels=c("Summer", "Winter", "Spring"))

  # Add in Sex
  phylum.prep$Sex[1:nrow(phylum)] <- rep("Female", 198)
  phylum.prep$Sex[(nrow(phylum)+1):(nrow(phylum)*2)] <- rep("Female", 198)
  phylum.prep$Sex[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- rep("Male", 198)
  phylum.prep$Sex[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- rep("Female", 198)
  phylum.prep$Sex[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- rep("Male", 198)
  phylum.prep$Sex[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- rep("Male", 198)
  phylum.prep$Sex[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- rep("Male", 198)
  phylum.prep$Sex[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- rep("Female", 198)
  phylum.prep$Sex[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- rep("Male", 198)
  
  # Add in Diet
  phylum.prep$Diet[1:nrow(phylum)] <- rep("Feeding", 198)
  phylum.prep$Diet[(nrow(phylum)+1):(nrow(phylum)*2)] <- rep("Feeding", 198)
  phylum.prep$Diet[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- rep("Fasting", 198)
  phylum.prep$Diet[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- rep("Fasting", 198)
  phylum.prep$Diet[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- rep("Feeding", 198)
  phylum.prep$Diet[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- rep("Feeding", 198)
  phylum.prep$Diet[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- rep("Fasting", 198)
  phylum.prep$Diet[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- rep("Feeding", 198)
  phylum.prep$Diet[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- rep("Feeding", 198)
  
  # Summarize dataframe
  phylum.sum <- phylum.prep %>%
    group_by(Season, Phylum) %>%
    summarize(Total_Mean = mean(Total_Relative_Abundance),
              Total_SD = sd(Total_Relative_Abundance),
              Total_SE = se(Total_Relative_Abundance),
              Classified_Mean = mean(Classified_Relative_Abundance),
              Classified_SD= sd(Classified_Relative_Abundance),
              Classified_SE = se(Classified_Relative_Abundance))
  
  return(phylum.sum)  
}