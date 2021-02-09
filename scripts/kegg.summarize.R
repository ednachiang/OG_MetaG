# Input paths
countPath = 'KEGG/musicc_outputs/KEGG_MUSiCC_all4.tab'
classPath = 'KEGG/KOID_Pathway_Classifications.csv'
samples = c("3715", "3717", "3723", "3733", "3734", "3744",
            "3772", "3773", "3775")

# Load input files
counts <- read.table(countPath, row.names = 1, sep = "\t")
classifications <- read.csv(classPath)

### Category 1 ###
# Create empty dataframe for cat1 data
cat1.df <- data.frame(matrix(nrow = length(unique(classifications[,1])), ncol = 9))
rownames(cat1.df) <- unique(classifications[,1])
colnames(cat1.df) <- samples
cat1.df[is.na(cat1.df)] <- 0

# Fill cat1.df
for(i in 1:length(unique(classifications[,1]))){
  cat1.name <- unique(classifications[,1])[i]
  match <- which(classifications[,1] == (cat1.name))
  koid.match <- classifications$KOID[match]
  
  rowToFill <- which(rownames(cat1.df) == cat1.name)
  
  for(j in 1:length(koid.match)){
    koid <- koid.match[j]
    newRowNum <- which(rownames(counts) == koid)

    if(dim(counts[newRowNum,])[1] > 0){
      cat1.df[rowToFill,] <- cat1.df[rowToFill,] + counts[newRowNum,]
    }
  }
}

### Category 2 ###
# Create empty dataframe for cat2 data
cat2.df <- data.frame(matrix(nrow = length(unique(classifications[,2])), ncol = 10))
rownames(cat2.df) <- unique(classifications[,2])
colnames(cat2.df) <- c(samples, "Cat1")
cat2.df[is.na(cat2.df)] <- 0

# Fill cat2.df
for(x in 1:length(unique(classifications[,2]))){
  cat2.name <- unique(classifications[,2])[x]
  match <- which(classifications[,2] == (cat2.name))
  koid.match <- classifications$KOID[match]
  
  rowToFill <- which(rownames(cat2.df) == cat2.name)
  
  cat2.df$Cat1[rowToFill] <- classifications[match[1],1]
  
  for(y in 1:length(koid.match)){
    koid <- koid.match[y]
    newRowNum <- which(rownames(counts) == koid)
    
    if(dim(counts[newRowNum,])[1] > 0){
      cat2.df[rowToFill,1:9] <- cat2.df[rowToFill,1:9] + counts[newRowNum,]
    }
  }
}



### Pathway ###
# Create empty dataframe for pathway data
path.df <- data.frame(matrix(nrow = length(unique(classifications[,3])), ncol = 11))
rownames(path.df) <- unique(classifications[,3])
colnames(path.df) <- c(samples, "Cat1", "Cat2")
path.df[is.na(path.df)] <- 0

# Fill path.df
for(x in 1:length(unique(classifications[,3]))){
  path.name <- unique(classifications[,3])[x]
  match <- which(classifications[,3] == (path.name))
  koid.match <- classifications$KOID[match]
  
  rowToFill <- which(rownames(path.df) == path.name)
  
  path.df$Cat1[rowToFill] <- classifications[match[1],1]
  path.df$Cat2[rowToFill] <- classifications[match[1],2]
  
  for(y in 1:length(koid.match)){
    koid <- koid.match[y]
    newRowNum <- which(rownames(counts) == koid)
    
    if(dim(counts[newRowNum,])[1] > 0){
      path.df[rowToFill,1:9] <- path.df[rowToFill,1:9] + counts[newRowNum,]
    }
  }
}

# Save outputs
#write.csv(cat1.df, file = "KEGG/musicc_outputs/test4/cat1.csv")
#write.csv(cat2.df, file = "KEGG/musicc_outputs/test4/cat2.csv")
#write.csv(path.df, file = "KEGG/musicc_outputs/test4/path.csv")
