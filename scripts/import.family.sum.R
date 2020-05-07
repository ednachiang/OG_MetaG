# x = This is your folder where all of your kaiju tables are located
# y = These are the variables you want to group by
# USE ' ' AROUND BOTH X & Y!!!

import.family.sum <- function(x) {
  n <- as.numeric(length(list.files(x)))
  # Initialize output dataframe
  family <- data.frame(matrix(ncol=7, nrow=715))
  # nrow is based on number of classes in sample 3715 because this is the first sample used to populate the dataframe
  # nrow will change as we populate the dataframe with all samples
  colnames(family) <- c("Domain", "Phylum", "Class", "Order", "Family", "RA_Total_3715", "Reads_3715")
  # I'll populate the dataframe sample-by-sample, so I'm only naming the colnames for the first sample
  
  for (i in 1:n) {
    filename <- list.files(x)[i]
    id <- substr(filename, 1,4)
    # Pull out squirrel ID
    wd <- paste0(x,"/",filename)
    # Path to each csv file
    df <- read.table(wd, sep="\t", header=T)
    # Save each tsv file as a dataframe
    df <- separate(df, col=taxon_name, int=c("Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Empty"), sep=";", remove=T)
    # Separate taxon name by ";" to split into taxonomic levels
    # Last 3 rows will have missing pieces because these are Viruses + unclassified seq's
    df <- df[,-1]
    # Remove first column (file path)
    df <- df[,-3]
    # Remove third column (taxon id)
    df <- df[,-7:-10]
    # remove all taxonomic levels after family
    
    if (i < 2){
      # Fill in output dataframe with 3715 info
      family$Domain <- df$Domain
      family$Phylum <- df$Phylum
      family$Class <- df$Class
      family$Order <- df$Order
      family$Family <- df$Family
      family$RA_Total_3715 <- df$percent
      family$Reads_3715 <- df$reads
    } else {
      colnames(df) <- c(paste0("RA_Total_",id), paste0("Reads_",id), "Domain", "Phylum", "Class", "Order")
      # Rename relative abundance and read columns for inclusion in output dataframe
      family <- full_join(family, df, by=c("Domain", "Phylum", "Class", "Order"))
      # This joins the output dataframe and sample dataframe by matching the Domain, Phylum, & Class columns
    }
  }
  
  # Replace NA's in read column with 0  
  family$Reads_3715 <- replace_na(family$Reads_3715, replace=0)
  family$Reads_3717 <- replace_na(family$Reads_3717, replace=0)
  family$Reads_3723 <- replace_na(family$Reads_3723, replace=0)
  family$Reads_3733 <- replace_na(family$Reads_3733, replace=0)
  family$Reads_3734 <- replace_na(family$Reads_3734, replace=0)
  family$Reads_3744 <- replace_na(family$Reads_3744, replace=0)
  family$Reads_3772 <- replace_na(family$Reads_3772, replace=0)
  family$Reads_3773 <- replace_na(family$Reads_3773, replace=0)
  family$Reads_3775 <- replace_na(family$Reads_3775, replace=0)
  
  # Update unclassified sequenced by combining "unclassified" + "cannot be assigned to a (non-viral)family"
  family[which(family$Domain == "unclassified"), 6:23] <- (family[which(family$Domain == "unclassified"), 6:23] + family[which(family$Domain == "cannot be assigned to a (non-viral) family"), 6:23])
  
  # Add phylum name for Viruses/Unclassified sequences
  family$Phylum[which(family$Domain == "unclassified")] <- "Unclassified"
  family$Phylum[which(family$Domain == "Viruses")] <- "Virus"
  
  # Add class name for Viruses/Unclassified sequences
  family$Class[which(family$Domain == "unclassified")] <- "Unclassified"
  family$Class[which(family$Domain == "Viruses")] <- "Virus"
  
  # Add order name for Viruses/Unclassified sequences
  family$Order[which(family$Domain == "unclassified")] <- "Unclassified"
  family$Order[which(family$Domain == "Viruses")] <- "Virus"
  
  # Add family name for Viruses/Unclassified sequences
  family$Family[which(family$Domain == "unclassified")] <- "Unclassified"
  family$Family[which(family$Domain == "Viruses")] <- "Virus"
  
  # Remove misc unclassified row
  family <- family[-which(family$Domain == "cannot be assigned to a (non-viral) family"),]
  
  
  # Recalculate classified relative abundances (RA) (divided by reads classified at order level)
  family$RA_Classified_3715 <- as.numeric((family$Reads_3715/ (sum(family$Reads_3715) - family$Reads_3715[which(family$Class == "Unclassified")]) *100))
  family$RA_Classified_3717 <- as.numeric((family$Reads_3717/ (sum(family$Reads_3717) - family$Reads_3717[which(family$Class == "Unclassified")]) *100))
  family$RA_Classified_3723 <- as.numeric((family$Reads_3723/ (sum(family$Reads_3723) - family$Reads_3723[which(family$Class == "Unclassified")]) *100))
  family$RA_Classified_3733 <- as.numeric((family$Reads_3733/ (sum(family$Reads_3733) - family$Reads_3733[which(family$Class == "Unclassified")]) *100))
  family$RA_Classified_3734 <- as.numeric((family$Reads_3734/ (sum(family$Reads_3734) - family$Reads_3734[which(family$Class == "Unclassified")]) *100))
  family$RA_Classified_3744 <- as.numeric((family$Reads_3744/ (sum(family$Reads_3744) - family$Reads_3744[which(family$Class == "Unclassified")]) *100))
  family$RA_Classified_3772 <- as.numeric((family$Reads_3772/ (sum(family$Reads_3772) - family$Reads_3772[which(family$Class == "Unclassified")]) *100))
  family$RA_Classified_3773 <- as.numeric((family$Reads_3773/ (sum(family$Reads_3773) - family$Reads_3773[which(family$Class == "Unclassified")]) *100))
  family$RA_Classified_3775 <- as.numeric((family$Reads_3775/ (sum(family$Reads_3775) - family$Reads_3775[which(family$Class == "Unclassified")]) *100))
  
  
  # Create new dataframe to prepare for summary
  family.prep <- data.frame(matrix(ncol=9, nrow=(nrow(order)*9)))
  colnames(family.prep) <- c("Phylum", "Class", "Order", "Total_Relative_Abundance", "Classified_Relative_Abundance", "Sample", "Season", "Sex", "Diet")
  family.prep$Phylum <- rep(family$Phylum, 9)
  family.prep$Class <- rep(family$Class, 9)
  family.prep$Order <- rep(family$Order, 9)
  
  # Add in Total Rel Abund
  family.prep$Total_Relative_Abundance[1:nrow(family)] <- family$RA_Total_3715
  family.prep$Total_Relative_Abundance[(nrow(family)+1):(nrow(family)*2)] <- family$RA_Total_3717
  family.prep$Total_Relative_Abundance[((nrow(family)*2)+1):(nrow(family)*3)] <- family$RA_Total_3723
  family.prep$Total_Relative_Abundance[((nrow(family)*3)+1):(nrow(family)*4)] <- family$RA_Total_3733
  family.prep$Total_Relative_Abundance[((nrow(family)*4)+1):(nrow(family)*5)] <- family$RA_Total_3734
  family.prep$Total_Relative_Abundance[((nrow(family)*5)+1):(nrow(family)*6)] <- family$RA_Total_3744
  family.prep$Total_Relative_Abundance[((nrow(family)*6)+1):(nrow(family)*7)] <- family$RA_Total_3772
  family.prep$Total_Relative_Abundance[((nrow(family)*7)+1):(nrow(family)*8)] <- family$RA_Total_3773
  family.prep$Total_Relative_Abundance[((nrow(family)*8)+1):(nrow(family)*9)] <- family$RA_Total_3775
  
  # Add in Classified Rel Abund
  family.prep$Classified_Relative_Abundance[1:nrow(family)] <- family$RA_Classified_3715
  family.prep$Classified_Relative_Abundance[(nrow(family)+1):(nrow(family)*2)] <- family$RA_Classified_3717
  family.prep$Classified_Relative_Abundance[((nrow(family)*2)+1):(nrow(family)*3)] <- family$RA_Classified_3723
  family.prep$Classified_Relative_Abundance[((nrow(family)*3)+1):(nrow(family)*4)] <- family$RA_Classified_3733
  family.prep$Classified_Relative_Abundance[((nrow(family)*4)+1):(nrow(family)*5)] <- family$RA_Classified_3734
  family.prep$Classified_Relative_Abundance[((nrow(family)*5)+1):(nrow(family)*6)] <- family$RA_Classified_3744
  family.prep$Classified_Relative_Abundance[((nrow(family)*6)+1):(nrow(family)*7)] <- family$RA_Classified_3772
  family.prep$Classified_Relative_Abundance[((nrow(family)*7)+1):(nrow(family)*8)] <- family$RA_Classified_3773
  family.prep$Classified_Relative_Abundance[((nrow(family)*8)+1):(nrow(family)*9)] <- family$RA_Classified_3775
  
  # Add in Sample
  family.prep$Sample[1:nrow(family)] <- rep("3715", nrow(family))
  family.prep$Sample[(nrow(family)+1):(nrow(family)*2)] <- rep("3717", nrow(family))
  family.prep$Sample[((nrow(family)*2)+1):(nrow(family)*3)] <- rep("3723", nrow(family))
  family.prep$Sample[((nrow(family)*3)+1):(nrow(family)*4)] <- rep("3733", nrow(family))
  family.prep$Sample[((nrow(family)*4)+1):(nrow(family)*5)] <- rep("3734", nrow(family))
  family.prep$Sample[((nrow(family)*5)+1):(nrow(family)*6)] <- rep("3744", nrow(family))
  family.prep$Sample[((nrow(family)*6)+1):(nrow(family)*7)] <- rep("3772", nrow(family))
  family.prep$Sample[((nrow(family)*7)+1):(nrow(family)*8)] <- rep("3773", nrow(family))
  family.prep$Sample[((nrow(family)*8)+1):(nrow(family)*9)] <- rep("3775", nrow(family))
  
  # Add in Season
  family.prep$Season[1:nrow(family)] <- rep("Summer", nrow(family))
  family.prep$Season[(nrow(family)+1):(nrow(family)*2)] <- rep("Summer", nrow(family))
  family.prep$Season[((nrow(family)*2)+1):(nrow(family)*3)] <- rep("Winter", nrow(family))
  family.prep$Season[((nrow(family)*3)+1):(nrow(family)*4)] <- rep("Winter", nrow(family))
  family.prep$Season[((nrow(family)*4)+1):(nrow(family)*5)] <- rep("Spring", nrow(family))
  family.prep$Season[((nrow(family)*5)+1):(nrow(family)*6)] <- rep("Summer", nrow(family))
  family.prep$Season[((nrow(family)*6)+1):(nrow(family)*7)] <- rep("Winter", nrow(family))
  family.prep$Season[((nrow(family)*7)+1):(nrow(family)*8)] <- rep("Spring", nrow(family))
  family.prep$Season[((nrow(family)*8)+1):(nrow(family)*9)] <- rep("Spring", nrow(family))
  family.prep$Season <- ordered(family.prep$Season, levels=c("Summer", "Winter", "Spring"))
  
  # Add in Sex
  family.prep$Sex[1:nrow(family)] <- rep("Female", nrow(family))
  family.prep$Sex[(nrow(family)+1):(nrow(family)*2)] <- rep("Female", nrow(family))
  family.prep$Sex[((nrow(family)*2)+1):(nrow(family)*3)] <- rep("Male", nrow(family))
  family.prep$Sex[((nrow(family)*3)+1):(nrow(family)*4)] <- rep("Female", nrow(family))
  family.prep$Sex[((nrow(family)*4)+1):(nrow(family)*5)] <- rep("Male", nrow(family))
  family.prep$Sex[((nrow(family)*5)+1):(nrow(family)*6)] <- rep("Male", nrow(family))
  family.prep$Sex[((nrow(family)*6)+1):(nrow(family)*7)] <- rep("Male", nrow(family))
  family.prep$Sex[((nrow(family)*7)+1):(nrow(family)*8)] <- rep("Female", nrow(family))
  family.prep$Sex[((nrow(family)*8)+1):(nrow(family)*9)] <- rep("Male", nrow(family))
  
  # Add in Diet
  family.prep$Diet[1:nrow(family)] <- rep("Feeding", nrow(family))
  family.prep$Diet[(nrow(family)+1):(nrow(family)*2)] <- rep("Feeding", nrow(family))
  family.prep$Diet[((nrow(family)*2)+1):(nrow(family)*3)] <- rep("Fasting", nrow(family))
  family.prep$Diet[((nrow(family)*3)+1):(nrow(family)*4)] <- rep("Fasting", nrow(family))
  family.prep$Diet[((nrow(family)*4)+1):(nrow(family)*5)] <- rep("Feeding", nrow(family))
  family.prep$Diet[((nrow(family)*5)+1):(nrow(family)*6)] <- rep("Feeding", nrow(family))
  family.prep$Diet[((nrow(family)*6)+1):(nrow(family)*7)] <- rep("Fasting", nrow(family))
  family.prep$Diet[((nrow(family)*7)+1):(nrow(family)*8)] <- rep("Feeding", nrow(family))
  family.prep$Diet[((nrow(family)*8)+1):(nrow(family)*9)] <- rep("Feeding", nrow(family))
  
  # Summarize dataframe
  family.sum <- family.prep %>%
    group_by(Season, Phylum, Class, Order, family) %>%
    summarize(Total_Mean = mean(Total_Relative_Abundance),
              Total_SD = sd(Total_Relative_Abundance),
              Total_SE = se(Total_Relative_Abundance),
              Classified_Mean = mean(Classified_Relative_Abundance),
              Classified_SD= sd(Classified_Relative_Abundance),
              Classified_SE = se(Classified_Relative_Abundance))
  
  # Replace NA's in read column with 0
  family.sum$Total_Mean <- replace_na(family.sum$Total_Mean, replace=0)
  family.sum$Total_SD <- replace_na(family.sum$Total_SD, replace=0)
  family.sum$Total_SE <- replace_na(family.sum$Total_SE, replace=0)
  family.sum$Classified_Mean <- replace_na(family.sum$Classified_Mean, replace=0)
  family.sum$Classified_SD <- replace_na(family.sum$Classified_SD, replace=0)
  family.sum$Classified_SE <- replace_na(family.sum$Classified_SE, replace=0)
  
  return(family.sum)  
}