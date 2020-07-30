# All scripts here written by Andrew Steinberger: https://github.com/asteinberger9/seq_scripts

### Simper
simper.pretty = function(x, metrics, interesting, perc_cutoff, low_cutoff, low_val, output_name){
  library(vegan)
  #handling otu tables for taxa levels
  save=list(0)
  if(grepl("Otu", colnames(x)[1])!=TRUE){
    #converts output from A.Neumann Taxonomy script
    save=list(58)
    x=as.data.frame(t(x))
    orig_names=colnames(x)
    new_names=list()
    l=1
    for(n in colnames(x)){
      ifelse((l<10), (colnames(x)[l]=c(paste0('Otu000',c(l)))), (colnames(x)[l]=c(paste0('Otu00',c(l))))) 
      new_names=append(new_names, colnames(x)[l])
      l=l+1
    }
    orig_names=as.data.frame(orig_names, row.names = as.character(new_names))
  }
  #running simper
  for(variables in interesting){
    test_1=with(metrics, simper(x, metrics[[variables]]))
    #parsing through simper output, saving desired info to table
    for(name in names(test_1)){
      testmx=matrix(ncol=length(interesting))
      testmx=cbind(test_1[[name]]$ord,test_1[[name]]$cusum)
      sorted=testmx[order(testmx[,1]),]
      sorted=cbind(sorted,test_1[[name]]$species)
      sorted=sorted[order(sorted[,2]),]
      t=matrix(sorted[sorted[,2]<=perc_cutoff,],ncol=3)
      i=nrow(t)
      #converting percents to percent of whole
      while(i>1){
        t[i,2]=as.character(as.numeric(t[i,2])-as.numeric(t[i-1,2]))
        i=i-1
      }
      t[,1]=name
      write.table(t,file=paste(output_name,'_simper.csv',sep=""), append=TRUE, sep=",", col.names = FALSE)
    }}
  y=read.table(paste(output_name,'_simper.csv',sep=""), header=FALSE,sep=",",fill = TRUE,row.names = NULL)
  file.remove(paste(output_name,'_simper.csv',sep = ""))
  y=y[-c(1)]
  colnames(y) = c("Comparison", "SIMPER", "OTU")
  #removing results lower than low cutoff
  if(low_cutoff=='y'){
    y=y[!(as.numeric(as.character(y$SIMPER))<low_val),]
  }
  #prevents changing of colnames if OTU table
  if(58 %in% save){
    y$OTU=orig_names[match(y$OTU, rownames(orig_names)),1]
  }
  write.csv(y,file=paste(output_name,'_clean_simper.csv', sep=''))
}


### Kruskal-Wallis for Simper
kruskal.pretty = function(otu, metrics, csv, interesting, output_name, taxonomy){
  library(vegan)
  library(dplyr)
  if(grepl("Otu", colnames(otu)[1])!=TRUE){
    #converts output from A.Neuman Taxonomy script
    otu=as.data.frame(t(otu))
  }
  #changing csv$X to rownames to allow proper splitting of comparisons
  csv$X=as.integer(rownames(csv))
  L=list()
  R=list()
  mean_L=c()
  sd_L=c()
  mean_R=c()
  sd_R=c()
  L_mean=c()
  R_mean=c()
  L_sd=c()
  R_sd=c()
  krusk=c()
  tax=c()
  L_abund=c()
  R_abund=c()
  L_abund_sd=c()
  R_abund_sd=c()
  abund=as.matrix(otu)
  abund=abund/rowSums(abund)
  for(b in levels(csv$Comparison)){
    otu_list=dplyr::filter(csv, Comparison==b) #saves otu list for current comparison
    for(i in csv$X){
      if(as.character(csv$Comparison[i])==b){  ##splitting comparisons so can call individually for table generation
        splt=as.data.frame(matrix(unlist(strsplit(as.character(csv$Comparison[i]),'_')), nrow=1, byrow=T))
        cola=as.character(splt[1,1])
        colb=as.character(splt[1,2])
        break
      }
    }
    #saving topic containing var of interest (cola/colb) (less memory intensive)
    for(topic in interesting){
      #preventing crash if there is only one topic in interesting
      if(is.null(levels(metrics[[topic]]))==TRUE){
        topic1=topic
        break
      }
      for(sbtpic in levels(metrics[[topic]])){
        if(sbtpic==cola){
          topic1=topic
          break
        }
      } 
    }
    #iterate thru rows in tpics of intrst til matches cola and colb, generates otu and metrics tbl  ##!Processing can be reduced!##
    for(rowe1 in metrics[[topic1]]){
      for(rowe2 in metrics[[topic1]]){ 
        if(rowe1==cola & rowe2==colb){ 
          listbact=otu[c(metrics[[topic1]]==cola|metrics[[topic1]]==colb),]
          listmet=metrics[c(metrics[[topic1]]==cola|metrics[[topic1]]==colb),]
          break
        }
      }
    }
    #collecting differential abundances
    sample_L=row.names(subset(metrics, metrics[[topic1]] == c(cola)))
    sample_R=row.names(subset(metrics, metrics[[topic1]] == c(colb)))
    #collecting abund values, perform/save mean and stdev calculations
    for(otus in otu_list$OTU){
      for(sample in sample_L){
        L=append(L,abund[sample,otus])
        mean_L[[otus]]=mean(as.numeric(L))
        sd_L[[otus]]=sd(as.numeric(L))
      }
      for(sample in sample_R){
        R=append(R,abund[sample,otus])
        mean_R[[otus]]=mean(as.numeric(R))
        sd_R[[otus]]=sd(as.numeric(R))
      }
      L=list()
      R=list()
    }
    #runs kruskal.test for each otu in simper csv, stores as list, also stores abundances
    for(otus in otu_list$OTU){
      result=kruskal.test(listbact[[otus]]~listmet[[topic1]])
      krusk=append(krusk, result$p.value)
      #stores taxonomic classification for each otu as list
      if(missing(taxonomy)){
        tax=append(tax, c("NA"))
      } else {
        tax=append(tax, as.character(taxonomy[otus, "Taxonomy"]))
      }
      L_mean=append(L_mean, as.character(mean_L[[otus]]))
      R_mean=append(R_mean, as.character(mean_R[[otus]]))
      L_sd=append(L_sd, as.character(sd_L[[otus]]))
      R_sd=append(R_sd, as.character(sd_R[[otus]]))
      
    }
  }
  #adjusted p-values for multiple comparisons
  fdr=p.adjust(krusk, method='fdr')
  #order csv to match 'krusk'/'fdr' list, add p.val, add taxonomy, re-ord to match orig csv, write to csv
  o_csv=dplyr::arrange(csv, Comparison)
  o_csv[,5]=krusk
  o_csv[,6]=fdr
  o_csv[,7]=tax
  o_csv[,8]=L_mean
  o_csv[,9]=L_sd
  o_csv[,10]=R_mean
  o_csv[,11]=R_sd
  o_csv=dplyr::arrange(o_csv, X)
  colnames(o_csv)[which(names(o_csv) == "V5")] <- "krusk_p.val" #changes column header
  colnames(o_csv)[which(names(o_csv) == "V6")] <- "fdr_krusk_p.val"
  colnames(o_csv)[which(names(o_csv) == "V7")] <- "Taxonomy"
  colnames(o_csv)[which(names(o_csv) == "V8")] <- "Left mean abund"
  colnames(o_csv)[which(names(o_csv) == "V9")] <- "Left stdev"
  colnames(o_csv)[which(names(o_csv) == "V10")] <- "Right mean abund"
  colnames(o_csv)[which(names(o_csv) == "V11")] <- "Right stdev"
  o_csv[,1]=NULL
  write.csv(o_csv, file=paste(output_name,"_krusk_simper.csv", sep=""))
}