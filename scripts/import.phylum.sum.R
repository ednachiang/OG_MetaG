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
  
  # Update unclassified sequenced by combining "unclassified" + "cannot be assigned to a (non-viral) phylum"
  phylum[which(phylum$Domain == "unclassified"), 3:20] <- (phylum[which(phylum$Domain == "unclassified"), 3:20] + phylum[which(phylum$Domain == "cannot be assigned to a (non-viral) phylum"), 3:20])

  # Add phylum name for Viruses/Unclassified sequences
  phylum$Phylum[which(phylum$Domain == "unclassified")] <- "Unclassified"
  phylum$Phylum[which(phylum$Domain == "Viruses")] <- "Virus"
  
  # Remove misc unclassified row
  phylum <- phylum[-which(phylum$Domain == "cannot be assigned to a (non-viral) phylum"),]
  
  # Recalculate classified relative abundances (RA) (divided by reads classified at phylum level)
  phylum$RA_Classified_3715 <- as.numeric((phylum$Reads_3715/ (sum(phylum$Reads_3715) - phylum$Reads_3715[which(phylum$Phylum == "Unclassified")]) *100))
  phylum$RA_Classified_3717 <- as.numeric((phylum$Reads_3717/ (sum(phylum$Reads_3717) - phylum$Reads_3717[which(phylum$Phylum == "Unclassified")]) *100))
  phylum$RA_Classified_3723 <- as.numeric((phylum$Reads_3723/ (sum(phylum$Reads_3723) - phylum$Reads_3723[which(phylum$Phylum == "Unclassified")]) *100))
  phylum$RA_Classified_3733 <- as.numeric((phylum$Reads_3733/ (sum(phylum$Reads_3733) - phylum$Reads_3733[which(phylum$Phylum == "Unclassified")]) *100))
  phylum$RA_Classified_3734 <- as.numeric((phylum$Reads_3734/ (sum(phylum$Reads_3734) - phylum$Reads_3734[which(phylum$Phylum == "Unclassified")]) *100))
  phylum$RA_Classified_3744 <- as.numeric((phylum$Reads_3744/ (sum(phylum$Reads_3744) - phylum$Reads_3744[which(phylum$Phylum == "Unclassified")]) *100))
  phylum$RA_Classified_3772 <- as.numeric((phylum$Reads_3772/ (sum(phylum$Reads_3772) - phylum$Reads_3772[which(phylum$Phylum == "Unclassified")]) *100))
  phylum$RA_Classified_3773 <- as.numeric((phylum$Reads_3773/ (sum(phylum$Reads_3773) - phylum$Reads_3773[which(phylum$Phylum == "Unclassified")]) *100))
  phylum$RA_Classified_3775 <- as.numeric((phylum$Reads_3775/ (sum(phylum$Reads_3775) - phylum$Reads_3775[which(phylum$Phylum == "Unclassified")]) *100))

  
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
  phylum.prep$Sample[1:nrow(phylum)] <- rep("3715", nrow(phylum))
  phylum.prep$Sample[(nrow(phylum)+1):(nrow(phylum)*2)] <- rep("3717", nrow(phylum))
  phylum.prep$Sample[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- rep("3723", nrow(phylum))
  phylum.prep$Sample[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- rep("3733", nrow(phylum))
  phylum.prep$Sample[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- rep("3734", nrow(phylum))
  phylum.prep$Sample[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- rep("3744", nrow(phylum))
  phylum.prep$Sample[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- rep("3772", nrow(phylum))
  phylum.prep$Sample[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- rep("3773", nrow(phylum))
  phylum.prep$Sample[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- rep("3775", nrow(phylum))
  
  # Add in Season
  phylum.prep$Season[1:nrow(phylum)] <- rep("Summer", nrow(phylum))
  phylum.prep$Season[(nrow(phylum)+1):(nrow(phylum)*2)] <- rep("Summer", nrow(phylum))
  phylum.prep$Season[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- rep("Winter", nrow(phylum))
  phylum.prep$Season[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- rep("Winter", nrow(phylum))
  phylum.prep$Season[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- rep("Spring", nrow(phylum))
  phylum.prep$Season[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- rep("Summer", nrow(phylum))
  phylum.prep$Season[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- rep("Winter", nrow(phylum))
  phylum.prep$Season[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- rep("Spring", nrow(phylum))
  phylum.prep$Season[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- rep("Spring", nrow(phylum))
  phylum.prep$Season <- ordered(phylum.prep$Season, levels=c("Summer", "Winter", "Spring"))

  # Add in Sex
  phylum.prep$Sex[1:nrow(phylum)] <- rep("Female", nrow(phylum))
  phylum.prep$Sex[(nrow(phylum)+1):(nrow(phylum)*2)] <- rep("Female", nrow(phylum))
  phylum.prep$Sex[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- rep("Male", nrow(phylum))
  phylum.prep$Sex[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- rep("Female", nrow(phylum))
  phylum.prep$Sex[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- rep("Male", nrow(phylum))
  phylum.prep$Sex[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- rep("Male", nrow(phylum))
  phylum.prep$Sex[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- rep("Male", nrow(phylum))
  phylum.prep$Sex[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- rep("Female", nrow(phylum))
  phylum.prep$Sex[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- rep("Male", nrow(phylum))
  
  # Add in Diet
  phylum.prep$Diet[1:nrow(phylum)] <- rep("Feeding", nrow(phylum))
  phylum.prep$Diet[(nrow(phylum)+1):(nrow(phylum)*2)] <- rep("Feeding", nrow(phylum))
  phylum.prep$Diet[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- rep("Fasting", nrow(phylum))
  phylum.prep$Diet[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- rep("Fasting", nrow(phylum))
  phylum.prep$Diet[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- rep("Feeding", nrow(phylum))
  phylum.prep$Diet[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- rep("Feeding", nrow(phylum))
  phylum.prep$Diet[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- rep("Fasting", nrow(phylum))
  phylum.prep$Diet[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- rep("Feeding", nrow(phylum))
  phylum.prep$Diet[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- rep("Feeding", nrow(phylum))
  
  # Summarize dataframe
  phylum.sum <- phylum.prep %>%
    group_by(Season, Phylum) %>%
    summarize(Total_Mean = mean(Total_Relative_Abundance),
              Total_SD = sd(Total_Relative_Abundance),
              Total_SE = se(Total_Relative_Abundance),
              Classified_Mean = mean(Classified_Relative_Abundance),
              Classified_SD= sd(Classified_Relative_Abundance),
              Classified_SE = se(Classified_Relative_Abundance))
  
  # Replace NA's in read column with 0
  phylum.sum$Total_Mean <- replace_na(phylum.sum$Total_Mean, replace=0)
  phylum.sum$Total_SD <- replace_na(phylum.sum$Total_SD, replace=0)
  phylum.sum$Total_SE <- replace_na(phylum.sum$Total_SE, replace=0)
  phylum.sum$Classified_Mean <- replace_na(phylum.sum$Classified_Mean, replace=0)
  phylum.sum$Classified_SD <- replace_na(phylum.sum$Classified_SD, replace=0)
  phylum.sum$Classified_SE <- replace_na(phylum.sum$Classified_SE, replace=0)
  
  return(phylum.sum)  
}
