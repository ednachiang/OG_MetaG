# x = This is your folder where all of your kaiju tables are located
# y = These are the variables you want to group by
# USE ' ' AROUND BOTH X & Y!!!

import.class.sum <- function(x, numRows) {
  n <- as.numeric(length(list.files(x)))
  # Initialize output dataframe
  class <- data.frame(matrix(ncol=2, nrow=numRows))
    # nrow is based on (# classes - 1) in sample 3715 because this is the first sample used to populate the dataframe
    # nrow will change as we populate the dataframe with all samples
    # The -1 is because we combined reads assigned to "unclassified" and "cannot be assigned to a (non-viral) class" (aka not classified at class level, but classified at a higher taxonomic level)
  colnames(class) <- c("Class", "Reads_3715")
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
    df <- df[,-1:-2]
      # Remove columns 1 & 2 (file path, relative abundance (we'll recalculate RA))
    df <- df[,-2]
     # Remove second column (taxon id)
    df <- df[,-3]
      # Remove phylum col
      # Keeping domain col because that has unclassified + viruses
    df <- df[,-4:-8]
      # remove empty col after class
    df$Class[which(df$Domain == "Viruses")] <- "Viruses"
      # Fill class col for viruses
    df$Class[which(df$Domain == "unclassified")] <- "Unclassified"
      # Fill class col for unclassified
    df$reads[which(df$Domain == "unclassified")] <- df$reads[which(df$Domain == "cannot be assigned to a (non-viral) class")] + df$reads[which(df$Domain == "unclassified")]
    df <- df[-which(df$Domain == "cannot be assigned to a (non-viral) class"),]
    df <- df[,-2]
      # Remove domain col
    
    if (i < 2){
      # Fill in output dataframe with 3715 info
      class$Class <- df$Class
      class$Reads_3715 <- df$reads
    } else {
      colnames(df) <- c(paste0("Reads_",id), "Class")
        # Rename relative abundance and read columns for inclusion in output dataframe
      class <- full_join(class, df, by=c("Class"))
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
  
  
  # Recalculate relative abundances (RA) (divided by total reads)
  class$RA_3715 <- as.numeric((class$Reads_3715/ (sum(class$Reads_3715)) *100))
  class$RA_3717 <- as.numeric((class$Reads_3717/ (sum(class$Reads_3717)) *100))
  class$RA_3723 <- as.numeric((class$Reads_3723/ (sum(class$Reads_3723)) *100))
  class$RA_3733 <- as.numeric((class$Reads_3733/ (sum(class$Reads_3733)) *100))
  class$RA_3734 <- as.numeric((class$Reads_3734/ (sum(class$Reads_3734)) *100))
  class$RA_3744 <- as.numeric((class$Reads_3744/ (sum(class$Reads_3744)) *100))
  class$RA_3772 <- as.numeric((class$Reads_3772/ (sum(class$Reads_3772)) *100))
  class$RA_3773 <- as.numeric((class$Reads_3773/ (sum(class$Reads_3773)) *100))
  class$RA_3775 <- as.numeric((class$Reads_3775/ (sum(class$Reads_3775)) *100))

  
  # Create new dataframe to prepare for summary
  class.prep <- data.frame(matrix(ncol=6, nrow=(nrow(class)*9)))
  colnames(class.prep) <- c("Class", "Relative_Abundance", "Sample", "Season", "Sex", "Diet")
  class.prep$Class <- rep(class$Class, 9)
  
  # Add in Total Rel Abund
  class.prep$Relative_Abundance[1:nrow(class)] <- class$RA_3715
  class.prep$Relative_Abundance[(nrow(class)+1):(nrow(class)*2)] <- class$RA_3717
  class.prep$Relative_Abundance[((nrow(class)*2)+1):(nrow(class)*3)] <- class$RA_3723
  class.prep$Relative_Abundance[((nrow(class)*3)+1):(nrow(class)*4)] <- class$RA_3733
  class.prep$Relative_Abundance[((nrow(class)*4)+1):(nrow(class)*5)] <- class$RA_3734
  class.prep$Relative_Abundance[((nrow(class)*5)+1):(nrow(class)*6)] <- class$RA_3744
  class.prep$Relative_Abundance[((nrow(class)*6)+1):(nrow(class)*7)] <- class$RA_3772
  class.prep$Relative_Abundance[((nrow(class)*7)+1):(nrow(class)*8)] <- class$RA_3773
  class.prep$Relative_Abundance[((nrow(class)*8)+1):(nrow(class)*9)] <- class$RA_3775
 
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
    group_by(Season, Class) %>%
    summarize(Mean = mean(Relative_Abundance),
              SD = sd(Relative_Abundance),
              SE = se(Relative_Abundance))
  
  # Replace NA's in read column with 0
  class.sum$Mean <- replace_na(class.sum$Mean, replace=0)
  class.sum$SD <- replace_na(class.sum$SD, replace=0)
  class.sum$SE <- replace_na(class.sum$SE, replace=0)
  
  return(class.sum)  
}