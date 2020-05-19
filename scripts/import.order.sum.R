# x = This is your folder where all of your kaiju tables are located
# y = These are the variables you want to group by
# USE ' ' AROUND BOTH X & Y!!!

import.order.sum <- function(x) {
  n <- as.numeric(length(list.files(x)))
  # Initialize output dataframe
  order <- data.frame(matrix(ncol=2, nrow=368))
    # nrow is based on (# species - 1) in sample 3715 because this is the first sample used to populate the dataframe
    # nrow will change as we populate the dataframe with all samples
    # The -1 is because we combined reads assigned to "unclassified" and "cannot be assigned to a (non-viral) species" (aka not classified at species level, but classified at a higher taxonomic level)
  colnames(order) <- c("Order", "Reads_3715")
    # I'll populate the dataframe sample-by-sample, so I'm only naming the colnames for the first sample
  
  for (i in 1:n) {
    filename <- list.files(x)[i]
    id <- substr(filename, 1,4)
      # Pull out squirrel ID
    wd <- paste0(x,"/",filename)
      # Path to each csv file
    df <- assign(paste0("order.", id), read.table(wd, sep="\t", header=T))
      # Save each tsv file as a dataframe
    df <- separate(df, col=taxon_name, int=c("Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Empty"), sep=";", remove=T)
      # Separate taxon name by ";" to split into taxonomic levels
      # Last 3 rows will have missing pieces because these are Viruses + unclassified seq's
    df <- df[,-1:-2]
      # Remove columns 1 & 2 (file path, relative abundance (we'll recalculate RA))
    df <- df[,-2]
      # Remove second column (taxon id)
    df <- df[,-3:-4]
      # Remove phylum, class, order, family, genus cols
      # Keeping domain col because that has unclassified + viruses
    df <- df[,-4:-7]
      # remove empty col after order
    df$Order[which(df$Domain == "Viruses")] <- "Viruses"
    # Fill family col for viruses
    df$Order[which(df$Domain == "unclassified")] <- "Unclassified"
    # Fill family col for unclassified
    df$reads[which(df$Domain == "unclassified")] <- df$reads[which(df$Domain == "cannot be assigned to a (non-viral) order")] + df$reads[which(df$Domain == "unclassified")]
    df <- df[-which(df$Domain == "cannot be assigned to a (non-viral) order"),]
    df <- df[,-2]
    # Remove domain col
    
    if (i < 2){
      # Fill in output dataframe with 3715 info
      order$Order <- df$Order
      order$Reads_3715 <- df$reads
    } else {
      colnames(df) <- c(paste0("Reads_",id),"Order")
        # Rename relative abundance and read columns for inclusion in output dataframe
      order <- full_join(order, df, by=c("Order"))
        # This joins the output dataframe and sample dataframe by matching order col
    }
  }
  
  # Replace NA's in read column with 0  
  order$Reads_3715 <- replace_na(order$Reads_3715, replace=0)
  order$Reads_3717 <- replace_na(order$Reads_3717, replace=0)
  order$Reads_3723 <- replace_na(order$Reads_3723, replace=0)
  order$Reads_3733 <- replace_na(order$Reads_3733, replace=0)
  order$Reads_3734 <- replace_na(order$Reads_3734, replace=0)
  order$Reads_3744 <- replace_na(order$Reads_3744, replace=0)
  order$Reads_3772 <- replace_na(order$Reads_3772, replace=0)
  order$Reads_3773 <- replace_na(order$Reads_3773, replace=0)
  order$Reads_3775 <- replace_na(order$Reads_3775, replace=0)
  
  # Recalculate relative abundances (RA) (divided by all reads)
  order$RA_3715 <- as.numeric((order$Reads_3715/ (sum(order$Reads_3715)) *100))
  order$RA_3717 <- as.numeric((order$Reads_3717/ (sum(order$Reads_3717)) *100))
  order$RA_3723 <- as.numeric((order$Reads_3723/ (sum(order$Reads_3723)) *100))
  order$RA_3733 <- as.numeric((order$Reads_3733/ (sum(order$Reads_3733)) *100))
  order$RA_3734 <- as.numeric((order$Reads_3734/ (sum(order$Reads_3734)) *100))
  order$RA_3744 <- as.numeric((order$Reads_3744/ (sum(order$Reads_3744)) *100))
  order$RA_3772 <- as.numeric((order$Reads_3772/ (sum(order$Reads_3772)) *100))
  order$RA_3773 <- as.numeric((order$Reads_3773/ (sum(order$Reads_3773)) *100))
  order$RA_3775 <- as.numeric((order$Reads_3775/ (sum(order$Reads_3775)) *100))

  
  # Create new dataframe to prepare for summary
  order.prep <- data.frame(matrix(ncol=6, nrow=(nrow(order)*9)))
  colnames(order.prep) <- c("Order", "Relative_Abundance", "Sample", "Season", "Sex", "Diet")
  order.prep$Phylum <- rep(order$Phylum, 9)
  order.prep$Class <- rep(order$Class, 9)
  order.prep$Order <- rep(order$Order, 9)
  
  # Add in Total Rel Abund
  order.prep$Relative_Abundance[1:nrow(order)] <- order$RA_3715
  order.prep$Relative_Abundance[(nrow(order)+1):(nrow(order)*2)] <- order$RA_3717
  order.prep$Relative_Abundance[((nrow(order)*2)+1):(nrow(order)*3)] <- order$RA_3723
  order.prep$Relative_Abundance[((nrow(order)*3)+1):(nrow(order)*4)] <- order$RA_3733
  order.prep$Relative_Abundance[((nrow(order)*4)+1):(nrow(order)*5)] <- order$RA_3734
  order.prep$Relative_Abundance[((nrow(order)*5)+1):(nrow(order)*6)] <- order$RA_3744
  order.prep$Relative_Abundance[((nrow(order)*6)+1):(nrow(order)*7)] <- order$RA_3772
  order.prep$Relative_Abundance[((nrow(order)*7)+1):(nrow(order)*8)] <- order$RA_3773
  order.prep$Relative_Abundance[((nrow(order)*8)+1):(nrow(order)*9)] <- order$RA_3775
 
  # Add in Sample
  order.prep$Sample[1:nrow(order)] <- rep("3715", nrow(order))
  order.prep$Sample[(nrow(order)+1):(nrow(order)*2)] <- rep("3717", nrow(order))
  order.prep$Sample[((nrow(order)*2)+1):(nrow(order)*3)] <- rep("3723", nrow(order))
  order.prep$Sample[((nrow(order)*3)+1):(nrow(order)*4)] <- rep("3733", nrow(order))
  order.prep$Sample[((nrow(order)*4)+1):(nrow(order)*5)] <- rep("3734", nrow(order))
  order.prep$Sample[((nrow(order)*5)+1):(nrow(order)*6)] <- rep("3744", nrow(order))
  order.prep$Sample[((nrow(order)*6)+1):(nrow(order)*7)] <- rep("3772", nrow(order))
  order.prep$Sample[((nrow(order)*7)+1):(nrow(order)*8)] <- rep("3773", nrow(order))
  order.prep$Sample[((nrow(order)*8)+1):(nrow(order)*9)] <- rep("3775", nrow(order))
  
  # Add in Season
  order.prep$Season[1:nrow(order)] <- rep("Summer", nrow(order))
  order.prep$Season[(nrow(order)+1):(nrow(order)*2)] <- rep("Summer", nrow(order))
  order.prep$Season[((nrow(order)*2)+1):(nrow(order)*3)] <- rep("Winter", nrow(order))
  order.prep$Season[((nrow(order)*3)+1):(nrow(order)*4)] <- rep("Winter", nrow(order))
  order.prep$Season[((nrow(order)*4)+1):(nrow(order)*5)] <- rep("Spring", nrow(order))
  order.prep$Season[((nrow(order)*5)+1):(nrow(order)*6)] <- rep("Summer", nrow(order))
  order.prep$Season[((nrow(order)*6)+1):(nrow(order)*7)] <- rep("Winter", nrow(order))
  order.prep$Season[((nrow(order)*7)+1):(nrow(order)*8)] <- rep("Spring", nrow(order))
  order.prep$Season[((nrow(order)*8)+1):(nrow(order)*9)] <- rep("Spring", nrow(order))
  order.prep$Season <- ordered(order.prep$Season, levels=c("Summer", "Winter", "Spring"))

  # Add in Sex
  order.prep$Sex[1:nrow(order)] <- rep("Female", nrow(order))
  order.prep$Sex[(nrow(order)+1):(nrow(order)*2)] <- rep("Female", nrow(order))
  order.prep$Sex[((nrow(order)*2)+1):(nrow(order)*3)] <- rep("Male", nrow(order))
  order.prep$Sex[((nrow(order)*3)+1):(nrow(order)*4)] <- rep("Female", nrow(order))
  order.prep$Sex[((nrow(order)*4)+1):(nrow(order)*5)] <- rep("Male", nrow(order))
  order.prep$Sex[((nrow(order)*5)+1):(nrow(order)*6)] <- rep("Male", nrow(order))
  order.prep$Sex[((nrow(order)*6)+1):(nrow(order)*7)] <- rep("Male", nrow(order))
  order.prep$Sex[((nrow(order)*7)+1):(nrow(order)*8)] <- rep("Female", nrow(order))
  order.prep$Sex[((nrow(order)*8)+1):(nrow(order)*9)] <- rep("Male", nrow(order))
  
  # Add in Diet
  order.prep$Diet[1:nrow(order)] <- rep("Feeding", nrow(order))
  order.prep$Diet[(nrow(order)+1):(nrow(order)*2)] <- rep("Feeding", nrow(order))
  order.prep$Diet[((nrow(order)*2)+1):(nrow(order)*3)] <- rep("Fasting", nrow(order))
  order.prep$Diet[((nrow(order)*3)+1):(nrow(order)*4)] <- rep("Fasting", nrow(order))
  order.prep$Diet[((nrow(order)*4)+1):(nrow(order)*5)] <- rep("Feeding", nrow(order))
  order.prep$Diet[((nrow(order)*5)+1):(nrow(order)*6)] <- rep("Feeding", nrow(order))
  order.prep$Diet[((nrow(order)*6)+1):(nrow(order)*7)] <- rep("Fasting", nrow(order))
  order.prep$Diet[((nrow(order)*7)+1):(nrow(order)*8)] <- rep("Feeding", nrow(order))
  order.prep$Diet[((nrow(order)*8)+1):(nrow(order)*9)] <- rep("Feeding", nrow(order))
  
  # Summarize dataframe
 order.sum <- order.prep %>%
    group_by(Season, Order) %>%
    summarize(Mean = mean(Relative_Abundance),
              SD = sd(Relative_Abundance),
              SE = se(Relative_Abundance))
  
 # Replace NA's in read column with 0
 order.sum$Mean <- replace_na(order.sum$Mean, replace=0)
 order.sum$SD <- replace_na(order.sum$SD, replace=0)
 order.sum$SE <- replace_na(order.sum$SE, replace=0)
 
  return(order.sum)  
}