# x = This is your folder where all of your kaiju tables are located
# y = These are the variables you want to group by
# USE ' ' AROUND BOTH X & Y!!!

import.genus.sum <- function(x, numRows) {
  n <- as.numeric(length(list.files(x)))
  # Initialize output dataframe
  genus <- data.frame(matrix(ncol=2, nrow=numRows))
  # nrow is based on (# genera - 1) in sample 3715 because this is the first sample used to populate the dataframe
  # nrow will change as we populate the dataframe with all samples
  # The -1 is because we combined reads assigned to "unclassified" and "cannot be assigned to a (non-viral) genus" (aka not classified at genus level, but classified at a higher taxonomic level)
  colnames(genus) <- c("Genus", "Reads_3715")
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
    df <- df[,-1:-2]
      # Remove columns 1 & 2 (file path, relative abundance (we'll recalculate RA))
    df <- df[,-2]
      # Remove second column (taxon id)
    df <- df[,-3:-6]
      # Remove phylum, class, order, family cols
      # Keeping domain col because that has unclassified + viruses
    df <- df[,-4:-5]
      # remove all taxonomic levels after family
    df$Genus[which(df$Domain == "Viruses")] <- "Viruses"
      # Fill genus col for viruses
    df$Genus[which(df$Domain == "unclassified")] <- "Unclassified"
      # Fill genus col for unclassified
    df$reads[which(df$Domain == "unclassified")] <- df$reads[which(df$Domain == "cannot be assigned to a (non-viral) genus")] + df$reads[which(df$Domain == "unclassified")]
    df <- df[-which(df$Domain == "cannot be assigned to a (non-viral) genus"),]
    df <- df[,-2]
      # Remove domain col
    
    if (i < 2){
      # Fill in output dataframe with 3715 info
      genus$Genus <- df$Genus
      genus$Reads_3715 <- df$reads
    } else {
      colnames(df) <- c(paste0("Reads_",id), "Genus")
      # Rename relative abundance and read columns for inclusion in output dataframe
      genus <- full_join(genus, df, by=c("Genus"))
      # This joins the output dataframe and sample dataframe by matching the genus col
    }
  }
  
  # Replace NA's in read column with 0  
  genus$Reads_3715 <- replace_na(genus$Reads_3715, replace=0)
  genus$Reads_3717 <- replace_na(genus$Reads_3717, replace=0)
  genus$Reads_3723 <- replace_na(genus$Reads_3723, replace=0)
  genus$Reads_3733 <- replace_na(genus$Reads_3733, replace=0)
  genus$Reads_3734 <- replace_na(genus$Reads_3734, replace=0)
  genus$Reads_3744 <- replace_na(genus$Reads_3744, replace=0)
  genus$Reads_3772 <- replace_na(genus$Reads_3772, replace=0)
  genus$Reads_3773 <- replace_na(genus$Reads_3773, replace=0)
  genus$Reads_3775 <- replace_na(genus$Reads_3775, replace=0)
  
  # Recalculate relative abundances (RA) (divided by all reads)
  genus$RA_3715 <- as.numeric((genus$Reads_3715/ (sum(genus$Reads_3715)) *100))
  genus$RA_3717 <- as.numeric((genus$Reads_3717/ (sum(genus$Reads_3717)) *100))
  genus$RA_3723 <- as.numeric((genus$Reads_3723/ (sum(genus$Reads_3723)) *100))
  genus$RA_3733 <- as.numeric((genus$Reads_3733/ (sum(genus$Reads_3733)) *100))
  genus$RA_3734 <- as.numeric((genus$Reads_3734/ (sum(genus$Reads_3734)) *100))
  genus$RA_3744 <- as.numeric((genus$Reads_3744/ (sum(genus$Reads_3744)) *100))
  genus$RA_3772 <- as.numeric((genus$Reads_3772/ (sum(genus$Reads_3772)) *100))
  genus$RA_3773 <- as.numeric((genus$Reads_3773/ (sum(genus$Reads_3773)) *100))
  genus$RA_3775 <- as.numeric((genus$Reads_3775/ (sum(genus$Reads_3775)) *100))
  
  
  # Create new dataframe to prepare for summary
  genus.prep <- data.frame(matrix(ncol=6, nrow=(nrow(genus)*9)))
  colnames(genus.prep) <- c("Genus", "Relative_Abundance", "Sample", "Season", "Sex", "Diet")
  genus.prep$Genus <- rep(genus$Genus, 9)
  
  # Add in Rel Abund
  genus.prep$Relative_Abundance[1:nrow(genus)] <- genus$RA_3715
  genus.prep$Relative_Abundance[(nrow(genus)+1):(nrow(genus)*2)] <- genus$RA_3717
  genus.prep$Relative_Abundance[((nrow(genus)*2)+1):(nrow(genus)*3)] <- genus$RA_3723
  genus.prep$Relative_Abundance[((nrow(genus)*3)+1):(nrow(genus)*4)] <- genus$RA_3733
  genus.prep$Relative_Abundance[((nrow(genus)*4)+1):(nrow(genus)*5)] <- genus$RA_3734
  genus.prep$Relative_Abundance[((nrow(genus)*5)+1):(nrow(genus)*6)] <- genus$RA_3744
  genus.prep$Relative_Abundance[((nrow(genus)*6)+1):(nrow(genus)*7)] <- genus$RA_3772
  genus.prep$Relative_Abundance[((nrow(genus)*7)+1):(nrow(genus)*8)] <- genus$RA_3773
  genus.prep$Relative_Abundance[((nrow(genus)*8)+1):(nrow(genus)*9)] <- genus$RA_3775
  
  # Add in Sample
  genus.prep$Sample[1:nrow(genus)] <- rep("3715", nrow(genus))
  genus.prep$Sample[(nrow(genus)+1):(nrow(genus)*2)] <- rep("3717", nrow(genus))
  genus.prep$Sample[((nrow(genus)*2)+1):(nrow(genus)*3)] <- rep("3723", nrow(genus))
  genus.prep$Sample[((nrow(genus)*3)+1):(nrow(genus)*4)] <- rep("3733", nrow(genus))
  genus.prep$Sample[((nrow(genus)*4)+1):(nrow(genus)*5)] <- rep("3734", nrow(genus))
  genus.prep$Sample[((nrow(genus)*5)+1):(nrow(genus)*6)] <- rep("3744", nrow(genus))
  genus.prep$Sample[((nrow(genus)*6)+1):(nrow(genus)*7)] <- rep("3772", nrow(genus))
  genus.prep$Sample[((nrow(genus)*7)+1):(nrow(genus)*8)] <- rep("3773", nrow(genus))
  genus.prep$Sample[((nrow(genus)*8)+1):(nrow(genus)*9)] <- rep("3775", nrow(genus))
  
  # Add in Season
  genus.prep$Season[1:nrow(genus)] <- rep("Summer", nrow(genus))
  genus.prep$Season[(nrow(genus)+1):(nrow(genus)*2)] <- rep("Summer", nrow(genus))
  genus.prep$Season[((nrow(genus)*2)+1):(nrow(genus)*3)] <- rep("Winter", nrow(genus))
  genus.prep$Season[((nrow(genus)*3)+1):(nrow(genus)*4)] <- rep("Winter", nrow(genus))
  genus.prep$Season[((nrow(genus)*4)+1):(nrow(genus)*5)] <- rep("Spring", nrow(genus))
  genus.prep$Season[((nrow(genus)*5)+1):(nrow(genus)*6)] <- rep("Summer", nrow(genus))
  genus.prep$Season[((nrow(genus)*6)+1):(nrow(genus)*7)] <- rep("Winter", nrow(genus))
  genus.prep$Season[((nrow(genus)*7)+1):(nrow(genus)*8)] <- rep("Spring", nrow(genus))
  genus.prep$Season[((nrow(genus)*8)+1):(nrow(genus)*9)] <- rep("Spring", nrow(genus))
  genus.prep$Season <- ordered(genus.prep$Season, levels=c("Summer", "Winter", "Spring"))
  
  # Add in Sex
  genus.prep$Sex[1:nrow(genus)] <- rep("Female", nrow(genus))
  genus.prep$Sex[(nrow(genus)+1):(nrow(genus)*2)] <- rep("Female", nrow(genus))
  genus.prep$Sex[((nrow(genus)*2)+1):(nrow(genus)*3)] <- rep("Male", nrow(genus))
  genus.prep$Sex[((nrow(genus)*3)+1):(nrow(genus)*4)] <- rep("Female", nrow(genus))
  genus.prep$Sex[((nrow(genus)*4)+1):(nrow(genus)*5)] <- rep("Male", nrow(genus))
  genus.prep$Sex[((nrow(genus)*5)+1):(nrow(genus)*6)] <- rep("Male", nrow(genus))
  genus.prep$Sex[((nrow(genus)*6)+1):(nrow(genus)*7)] <- rep("Male", nrow(genus))
  genus.prep$Sex[((nrow(genus)*7)+1):(nrow(genus)*8)] <- rep("Female", nrow(genus))
  genus.prep$Sex[((nrow(genus)*8)+1):(nrow(genus)*9)] <- rep("Male", nrow(genus))
  
  # Add in Diet
  genus.prep$Diet[1:nrow(genus)] <- rep("Feeding", nrow(genus))
  genus.prep$Diet[(nrow(genus)+1):(nrow(genus)*2)] <- rep("Feeding", nrow(genus))
  genus.prep$Diet[((nrow(genus)*2)+1):(nrow(genus)*3)] <- rep("Fasting", nrow(genus))
  genus.prep$Diet[((nrow(genus)*3)+1):(nrow(genus)*4)] <- rep("Fasting", nrow(genus))
  genus.prep$Diet[((nrow(genus)*4)+1):(nrow(genus)*5)] <- rep("Feeding", nrow(genus))
  genus.prep$Diet[((nrow(genus)*5)+1):(nrow(genus)*6)] <- rep("Feeding", nrow(genus))
  genus.prep$Diet[((nrow(genus)*6)+1):(nrow(genus)*7)] <- rep("Fasting", nrow(genus))
  genus.prep$Diet[((nrow(genus)*7)+1):(nrow(genus)*8)] <- rep("Feeding", nrow(genus))
  genus.prep$Diet[((nrow(genus)*8)+1):(nrow(genus)*9)] <- rep("Feeding", nrow(genus))
  
  # Summarize dataframe
  genus.sum <- genus.prep %>%
    group_by(Season, Genus) %>%
    summarize(Mean = mean(Relative_Abundance),
              SD = sd(Relative_Abundance),
              SE = se(Relative_Abundance))
  
  # Replace NA's in read column with 0
  genus.sum$Mean <- replace_na(genus.sum$Mean, replace=0)
  genus.sum$SD <- replace_na(genus.sum$SD, replace=0)
  genus.sum$SE <- replace_na(genus.sum$SE, replace=0)

  return(genus.sum)  
}