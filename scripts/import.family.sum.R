# x = This is your folder where all of your kaiju tables are located
# y = These are the variables you want to group by
# USE ' ' AROUND BOTH X & Y!!!

import.family.sum <- function(x, numRows) {
  n <- as.numeric(length(list.files(x)))
  # Initialize output dataframe
  family <- data.frame(matrix(ncol=2, nrow=numRows))
  # nrow is based on (# families - 1) in sample 3715 because this is the first sample used to populate the dataframe
  # nrow will change as we populate the dataframe with all samples
  # The -1 is because we combined reads assigned to "unclassified" and "cannot be assigned to a (non-viral) family" (aka not classified at family level, but classified at a higher taxonomic level)
  colnames(family) <- c("Family", "Reads_3715")
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
    df <- df[,-3:-5]
      # Remove phylum, class, order cols
      # Keeping domain col because that has unclassified + viruses
    df <- df[,-4:-6]
      # remove all taxonomic levels after family
    df$Family[which(df$Domain == "Viruses")] <- "Viruses"
      # Fill family col for viruses
    df$Family[which(df$Domain == "unclassified")] <- "Unclassified"
      # Fill family col for unclassified
    df$reads[which(df$Domain == "unclassified")] <- df$reads[which(df$Domain == "cannot be assigned to a (non-viral) family")] + df$reads[which(df$Domain == "unclassified")]
    df <- df[-which(df$Domain == "cannot be assigned to a (non-viral) family"),]
    df <- df[,-2]
      # Remove domain col
    
    if (i < 2){
      # Fill in output dataframe with 3715 info
      family$Family <- df$Family
      family$Reads_3715 <- df$reads
    } else {
      colnames(df) <- c(paste0("Reads_",id), "Family")
      # Rename relative abundance and read columns for inclusion in output dataframe
      family <- full_join(family, df, by=c("Family"))
      # This joins the output dataframe and sample dataframe by matching family col
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
  
  # Recalculate relative abundances (RA) (divided by all reads)
  family$RA_3715 <- as.numeric((family$Reads_3715/ (sum(family$Reads_3715)) *100))
  family$RA_3717 <- as.numeric((family$Reads_3717/ (sum(family$Reads_3717)) *100))
  family$RA_3723 <- as.numeric((family$Reads_3723/ (sum(family$Reads_3723)) *100))
  family$RA_3733 <- as.numeric((family$Reads_3733/ (sum(family$Reads_3733)) *100))
  family$RA_3734 <- as.numeric((family$Reads_3734/ (sum(family$Reads_3734)) *100))
  family$RA_3744 <- as.numeric((family$Reads_3744/ (sum(family$Reads_3744)) *100))
  family$RA_3772 <- as.numeric((family$Reads_3772/ (sum(family$Reads_3772)) *100))
  family$RA_3773 <- as.numeric((family$Reads_3773/ (sum(family$Reads_3773)) *100))
  family$RA_3775 <- as.numeric((family$Reads_3775/ (sum(family$Reads_3775)) *100))
  
  
  # Create new dataframe to prepare for summary
  family.prep <- data.frame(matrix(ncol=6, nrow=(nrow(family)*9)))
  colnames(family.prep) <- c("Family", "Relative_Abundance", "Sample", "Season", "Sex", "Diet")
  family.prep$Family <- rep(family$Family, 9)
  
  # Add in Rel Abund
  family.prep$Relative_Abundance[1:nrow(family)] <- family$RA_3715
  family.prep$Relative_Abundance[(nrow(family)+1):(nrow(family)*2)] <- family$RA_3717
  family.prep$Relative_Abundance[((nrow(family)*2)+1):(nrow(family)*3)] <- family$RA_3723
  family.prep$Relative_Abundance[((nrow(family)*3)+1):(nrow(family)*4)] <- family$RA_3733
  family.prep$Relative_Abundance[((nrow(family)*4)+1):(nrow(family)*5)] <- family$RA_3734
  family.prep$Relative_Abundance[((nrow(family)*5)+1):(nrow(family)*6)] <- family$RA_3744
  family.prep$Relative_Abundance[((nrow(family)*6)+1):(nrow(family)*7)] <- family$RA_3772
  family.prep$Relative_Abundance[((nrow(family)*7)+1):(nrow(family)*8)] <- family$RA_3773
  family.prep$Relative_Abundance[((nrow(family)*8)+1):(nrow(family)*9)] <- family$RA_3775
  
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
    group_by(Season, Family) %>%
    summarize(Mean = mean(Relative_Abundance),
              SD = sd(Relative_Abundance),
              SE = se(Relative_Abundance))
  
  # Replace NA's in read column with 0
  family.sum$Mean <- replace_na(family.sum$Mean, replace=0)
  family.sum$SD <- replace_na(family.sum$SD, replace=0)
  family.sum$SE <- replace_na(family.sum$SE, replace=0)

  return(family.sum)  
}