# x = This is your folder where all of your kaiju tables are located
# y = These are the variables you want to group by
# USE ' ' AROUND BOTH X & Y!!!

import.species.sum <- function(x, numRows) {
  n <- as.numeric(length(list.files(x)))
  # Initialize output dataframe
  species <- data.frame(matrix(ncol=2, nrow=numRows))
    # nrow is based on (# species - 1) in sample 3715 because this is the first sample used to populate the dataframe
    # nrow will change as we populate the dataframe with all samples
    # The -1 is because we combined reads assigned to "unclassified" and "cannot be assigned to a (non-viral) species" (aka not classified at species level, but classified at a higher taxonomic level)
  colnames(species) <- c("Species", "Reads_3715")
    # I'll populate the dataframe sample-by-sample, so I'm only naming the colnames for the first sample
  
  for (i in 1:n) {
    filename <- list.files(x)[i]
    id <- substr(filename, 1,4)
      # Pull out squirrel ID
    wd <- paste0(x,"/",filename)
      # Path to each csv file
    df <- read.table(wd, sep="\t", header=T, quote="", fill=F)
      # Save each tsv file as a dataframe
      # quote and fill parameters from: https://kbroman.org/blog/2017/08/08/eof-within-quoted-string/
    df <- separate(df, col=taxon_name, int=c("Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Empty"), sep=";", remove=T)
      # Separate taxon name by ";" to split into taxonomic levels
      # Last 3 rows will have missing pieces because these are Viruses + unclassified seq's
    df <- df[,-1:-2]
      # Remove columns 1 & 2 (file path, relative abundance (we'll recalculate RA))
    df <- df[,-2]
      # Remove second column (taxon id)
    df <- df[,-3:-7]
      # Remove phylum, class, order, family, genus cols
      # Keeping domain col because that has unclassified + viruses
    df <- df[,-4]
      # remove empty col after species
    df$Species[which(df$Domain == "Viruses")] <- "Viruses"
      # Fill species col for viruses
    df$Species[which(df$Domain == "unclassified")] <- "Unclassified"
      # Fill species col for unclassified
    df$reads[which(df$Domain == "unclassified")] <- df$reads[which(df$Domain == "cannot be assigned to a (non-viral) species")] + df$reads[which(df$Domain == "unclassified")]
    df <- df[-which(df$Domain == "cannot be assigned to a (non-viral) species"),]
    df <- df[,-2]
      # Remove domain col
    
    if (i < 2){
      # Fill in output dataframe with 3715 info
      species$Species <- df$Species
      species$Reads_3715 <- df$reads
    } else {
      colnames(df) <- c(paste0("Reads_",id), "Species")
      # Rename relative abundance and read columns for inclusion in output dataframe
      species <- full_join(species, df, by=c("Species"))
      # This joins the output dataframe and sample dataframe by matching species columns
    }
  }
  
  # Replace NA's in read column with 0  
  species$Reads_3715 <- replace_na(species$Reads_3715, replace=0)
  species$Reads_3717 <- replace_na(species$Reads_3717, replace=0)
  species$Reads_3723 <- replace_na(species$Reads_3723, replace=0)
  species$Reads_3733 <- replace_na(species$Reads_3733, replace=0)
  species$Reads_3734 <- replace_na(species$Reads_3734, replace=0)
  species$Reads_3744 <- replace_na(species$Reads_3744, replace=0)
  species$Reads_3772 <- replace_na(species$Reads_3772, replace=0)
  species$Reads_3773 <- replace_na(species$Reads_3773, replace=0)
  species$Reads_3775 <- replace_na(species$Reads_3775, replace=0)
  
  # Recalculate relative abundances (RA) (divided by all reads)
  species$RA_3715 <- as.numeric((species$Reads_3715/ (sum(species$Reads_3715)) *100))
  species$RA_3717 <- as.numeric((species$Reads_3717/ (sum(species$Reads_3717)) *100))
  species$RA_3723 <- as.numeric((species$Reads_3723/ (sum(species$Reads_3723)) *100))
  species$RA_3733 <- as.numeric((species$Reads_3733/ (sum(species$Reads_3733)) *100))
  species$RA_3734 <- as.numeric((species$Reads_3734/ (sum(species$Reads_3734)) *100))
  species$RA_3744 <- as.numeric((species$Reads_3744/ (sum(species$Reads_3744)) *100))
  species$RA_3772 <- as.numeric((species$Reads_3772/ (sum(species$Reads_3772)) *100))
  species$RA_3773 <- as.numeric((species$Reads_3773/ (sum(species$Reads_3773)) *100))
  species$RA_3775 <- as.numeric((species$Reads_3775/ (sum(species$Reads_3775)) *100))
  
  
  # Create new dataframe to prepare for summary
  species.prep <- data.frame(matrix(ncol=6, nrow=(nrow(species)*9)))
  colnames(species.prep) <- c("Species", "Relative_Abundance", "Sample", "Season", "Sex", "Diet")
  species.prep$Species <- rep(species$Species, 9)
  
  # Add in Rel Abund
  species.prep$Relative_Abundance[1:nrow(species)] <- species$RA_3715
  species.prep$Relative_Abundance[(nrow(species)+1):(nrow(species)*2)] <- species$RA_3717
  species.prep$Relative_Abundance[((nrow(species)*2)+1):(nrow(species)*3)] <- species$RA_3723
  species.prep$Relative_Abundance[((nrow(species)*3)+1):(nrow(species)*4)] <- species$RA_3733
  species.prep$Relative_Abundance[((nrow(species)*4)+1):(nrow(species)*5)] <- species$RA_3734
  species.prep$Relative_Abundance[((nrow(species)*5)+1):(nrow(species)*6)] <- species$RA_3744
  species.prep$Relative_Abundance[((nrow(species)*6)+1):(nrow(species)*7)] <- species$RA_3772
  species.prep$Relative_Abundance[((nrow(species)*7)+1):(nrow(species)*8)] <- species$RA_3773
  species.prep$Relative_Abundance[((nrow(species)*8)+1):(nrow(species)*9)] <- species$RA_3775
  
  # Add in Sample
  species.prep$Sample[1:nrow(species)] <- rep("3715", nrow(species))
  species.prep$Sample[(nrow(species)+1):(nrow(species)*2)] <- rep("3717", nrow(species))
  species.prep$Sample[((nrow(species)*2)+1):(nrow(species)*3)] <- rep("3723", nrow(species))
  species.prep$Sample[((nrow(species)*3)+1):(nrow(species)*4)] <- rep("3733", nrow(species))
  species.prep$Sample[((nrow(species)*4)+1):(nrow(species)*5)] <- rep("3734", nrow(species))
  species.prep$Sample[((nrow(species)*5)+1):(nrow(species)*6)] <- rep("3744", nrow(species))
  species.prep$Sample[((nrow(species)*6)+1):(nrow(species)*7)] <- rep("3772", nrow(species))
  species.prep$Sample[((nrow(species)*7)+1):(nrow(species)*8)] <- rep("3773", nrow(species))
  species.prep$Sample[((nrow(species)*8)+1):(nrow(species)*9)] <- rep("3775", nrow(species))
  
  # Add in Season
  species.prep$Season[1:nrow(species)] <- rep("Summer", nrow(species))
  species.prep$Season[(nrow(species)+1):(nrow(species)*2)] <- rep("Summer", nrow(species))
  species.prep$Season[((nrow(species)*2)+1):(nrow(species)*3)] <- rep("Winter", nrow(species))
  species.prep$Season[((nrow(species)*3)+1):(nrow(species)*4)] <- rep("Winter", nrow(species))
  species.prep$Season[((nrow(species)*4)+1):(nrow(species)*5)] <- rep("Spring", nrow(species))
  species.prep$Season[((nrow(species)*5)+1):(nrow(species)*6)] <- rep("Summer", nrow(species))
  species.prep$Season[((nrow(species)*6)+1):(nrow(species)*7)] <- rep("Winter", nrow(species))
  species.prep$Season[((nrow(species)*7)+1):(nrow(species)*8)] <- rep("Spring", nrow(species))
  species.prep$Season[((nrow(species)*8)+1):(nrow(species)*9)] <- rep("Spring", nrow(species))
  species.prep$Season <- ordered(species.prep$Season, levels=c("Summer", "Winter", "Spring"))
  
  # Add in Sex
  species.prep$Sex[1:nrow(species)] <- rep("Female", nrow(species))
  species.prep$Sex[(nrow(species)+1):(nrow(species)*2)] <- rep("Female", nrow(species))
  species.prep$Sex[((nrow(species)*2)+1):(nrow(species)*3)] <- rep("Male", nrow(species))
  species.prep$Sex[((nrow(species)*3)+1):(nrow(species)*4)] <- rep("Female", nrow(species))
  species.prep$Sex[((nrow(species)*4)+1):(nrow(species)*5)] <- rep("Male", nrow(species))
  species.prep$Sex[((nrow(species)*5)+1):(nrow(species)*6)] <- rep("Male", nrow(species))
  species.prep$Sex[((nrow(species)*6)+1):(nrow(species)*7)] <- rep("Male", nrow(species))
  species.prep$Sex[((nrow(species)*7)+1):(nrow(species)*8)] <- rep("Female", nrow(species))
  species.prep$Sex[((nrow(species)*8)+1):(nrow(species)*9)] <- rep("Male", nrow(species))
  
  # Add in Diet
  species.prep$Diet[1:nrow(species)] <- rep("Feeding", nrow(species))
  species.prep$Diet[(nrow(species)+1):(nrow(species)*2)] <- rep("Feeding", nrow(species))
  species.prep$Diet[((nrow(species)*2)+1):(nrow(species)*3)] <- rep("Fasting", nrow(species))
  species.prep$Diet[((nrow(species)*3)+1):(nrow(species)*4)] <- rep("Fasting", nrow(species))
  species.prep$Diet[((nrow(species)*4)+1):(nrow(species)*5)] <- rep("Feeding", nrow(species))
  species.prep$Diet[((nrow(species)*5)+1):(nrow(species)*6)] <- rep("Feeding", nrow(species))
  species.prep$Diet[((nrow(species)*6)+1):(nrow(species)*7)] <- rep("Fasting", nrow(species))
  species.prep$Diet[((nrow(species)*7)+1):(nrow(species)*8)] <- rep("Feeding", nrow(species))
  species.prep$Diet[((nrow(species)*8)+1):(nrow(species)*9)] <- rep("Feeding", nrow(species))
  
  # Summarize dataframe
  species.sum <- species.prep %>%
    group_by(Season, Species) %>%
    summarize(Mean = mean(Relative_Abundance),
              SD = sd(Relative_Abundance),
              SE = se(Relative_Abundance))
  
  # Replace NA's in read column with 0
  species.sum$Mean <- replace_na(species.sum$Mean, replace=0)
  species.sum$SD <- replace_na(species.sum$SD, replace=0)
  species.sum$SE <- replace_na(species.sum$SE, replace=0)

  return(species.sum)  
}