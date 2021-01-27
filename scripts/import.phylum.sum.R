# x = This is your folder where all of your kaiju tables are located
# y = These are the variables you want to group by
# USE ' ' AROUND BOTH X & Y!!!

import.phylum.sum <- function(x) {
  first <- list.files(x)[1]
  first.id <- substr(first, 1,4)
  first.df <- assign(paste0("phylum.", first.id), 
                     read.table(paste0(x,"/",first), sep="\t", header=T))
  numRows <- (nrow(first.df)-1)
  # nrow is based on (# phyla - 1) in sample 3715 because this is the first sample used to populate the dataframe
  # nrow will change as we populate the dataframe with all samples
  # The -1 is because we combined reads assigned to "unclassified" and "cannot be assigned to a (non-viral) phylum" (aka not classified at phylum level, but classified at a higher taxonomic level)
  
  n <- as.numeric(length(list.files(x)))
  # Initialize output dataframe
  phylum <- data.frame(matrix(ncol=2, nrow=numRows))
colnames(phylum) <- c("Phylum", "Reads_3715")
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
    df <- df[,-1:-2]
      # Remove columns 1 & 2 (file path, relative abundance (we'll recalculate RA))
    df <- df[,-2]
      # Remove second column (taxon id)
    df <- df[,-4:-9]
      # remove empty col after phylum
    df$Phylum[which(df$Domain == "Viruses")] <- "Viruses"
      # Fill phylum col for viruses
    df$Phylum[which(df$Domain == "unclassified")] <- "Unclassified"
      # Fill family col for unclassified
    df$reads[which(df$Domain == "unclassified")] <- df$reads[which(df$Domain == "cannot be assigned to a (non-viral) phylum")] + df$reads[which(df$Domain == "unclassified")]
    df <- df[-which(df$Domain == "cannot be assigned to a (non-viral) phylum"),]
    df <- df[,-2]
      # Remove domain col
    
    if (i < 2){
      # Fill in output dataframe with 3715 info
      phylum$Phylum <- df$Phylum
      phylum$Reads_3715 <- df$reads
    } else {
      colnames(df) <- c(paste0("Reads_",id), "Phylum")
       # Rename relative abundance and read columns for inclusion in output dataframe
      phylum <- full_join(phylum, df, by=c("Phylum"))
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
 
  
  # Recalculate relative abundances (RA) (divided by total reads)
  phylum$RA_3715 <- as.numeric((phylum$Reads_3715/ (sum(phylum$Reads_3715)) *100))
  phylum$RA_3717 <- as.numeric((phylum$Reads_3717/ (sum(phylum$Reads_3717)) *100))
  phylum$RA_3723 <- as.numeric((phylum$Reads_3723/ (sum(phylum$Reads_3723)) *100))
  phylum$RA_3733 <- as.numeric((phylum$Reads_3733/ (sum(phylum$Reads_3733)) *100))
  phylum$RA_3734 <- as.numeric((phylum$Reads_3734/ (sum(phylum$Reads_3734)) *100))
  phylum$RA_3744 <- as.numeric((phylum$Reads_3744/ (sum(phylum$Reads_3744)) *100))
  phylum$RA_3772 <- as.numeric((phylum$Reads_3772/ (sum(phylum$Reads_3772)) *100))
  phylum$RA_3773 <- as.numeric((phylum$Reads_3773/ (sum(phylum$Reads_3773)) *100))
  phylum$RA_3775 <- as.numeric((phylum$Reads_3775/ (sum(phylum$Reads_3775)) *100))

  
  # Create new dataframe to prepare for summary
  phylum.prep <- data.frame(matrix(ncol=6, nrow=(nrow(phylum)*9)))
  colnames(phylum.prep) <- c("Phylum", "Relative_Abundance", "Sample", "Season", "Sex", "Diet")
  phylum.prep$Phylum <- (rep(phylum$Phylum, 9))
  
  # Add in Total Rel Abund
  phylum.prep$Relative_Abundance[1:nrow(phylum)] <- phylum$RA_3715
  phylum.prep$Relative_Abundance[(nrow(phylum)+1):(nrow(phylum)*2)] <- phylum$RA_3717
  phylum.prep$Relative_Abundance[((nrow(phylum)*2)+1):(nrow(phylum)*3)] <- phylum$RA_3723
  phylum.prep$Relative_Abundance[((nrow(phylum)*3)+1):(nrow(phylum)*4)] <- phylum$RA_3733
  phylum.prep$Relative_Abundance[((nrow(phylum)*4)+1):(nrow(phylum)*5)] <- phylum$RA_3734
  phylum.prep$Relative_Abundance[((nrow(phylum)*5)+1):(nrow(phylum)*6)] <- phylum$RA_3744
  phylum.prep$Relative_Abundance[((nrow(phylum)*6)+1):(nrow(phylum)*7)] <- phylum$RA_3772
  phylum.prep$Relative_Abundance[((nrow(phylum)*7)+1):(nrow(phylum)*8)] <- phylum$RA_3773
  phylum.prep$Relative_Abundance[((nrow(phylum)*8)+1):(nrow(phylum)*9)] <- phylum$RA_3775
  
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
    summarize(Mean = mean(Relative_Abundance),
              SD = sd(Relative_Abundance),
              SE = se(Relative_Abundance))
  
  # Replace NA's in read column with 0
  phylum.sum$Mean <- replace_na(phylum.sum$Mean, replace=0)
  phylum.sum$SD <- replace_na(phylum.sum$SD, replace=0)
  phylum.sum$SE <- replace_na(phylum.sum$SE, replace=0)

  return(phylum.sum)  
}
