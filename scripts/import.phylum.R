# x = This is your folder where all of your kaiju tables are located
# USE ' ' AROUND BOTH X!!!

import.phylum <- function(x,y) {
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
    

    return(phylum)  
}
