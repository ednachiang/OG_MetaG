# Functions by Madison Cox and Kim Dill-Mcfarland (https://github.com/kdillmcfarland/micro_ecol)

# Implementation: 
# pairwise.adonis(matrix, meta$x, sim.method="bray", p.adjust.m="fdr", strat = meta$y)
# pairwise.adonis.stratified(matrix, meta$x, sim.method="bray", p.adjust.m="fdr")

# Kim's function
pairwise.adonis <- function(x,factors, sim.method, p.adjust.m){
  library(vegan)
  co = as.matrix(combn(unique(factors),2))
  pairs = c()
  F.Model =c()
  R2 = c()
  p.value = c()
    
  for(elem in 1:ncol(co)){
    ad = adonis(x[factors %in% c(as.character(co[1,elem]),as.character(co[2,elem])),] ~ 
                  factors[factors %in% c(as.character(co[1,elem]),as.character(co[2,elem]))] , method =sim.method, permutations=99999);
    pairs = c(pairs,paste(co[1,elem],'vs',co[2,elem]));
    F.Model =c(F.Model,ad$aov.tab[1,4]);
    R2 = c(R2,ad$aov.tab[1,5]);
    p.value = c(p.value,ad$aov.tab[1,6])}
  
  p.adjusted = p.adjust(p.value,method=p.adjust.m)
  pairw.res = data.frame(pairs,F.Model,R2,p.value,p.adjusted)
  return(pairw.res)
  }

# Kim's function STRATIFIED
pairwise.adonis.stratified <- function(x,factors, strat, sim.method, p.adjust.m){
  library(vegan)
  co = as.matrix(combn(unique(factors),2))
  pairs = c()
  F.Model =c()
  R2 = c()
  p.value = c()
  
  for(elem in 1:ncol(co)){
    ad = adonis(x[factors %in% c(as.character(co[1,elem]),as.character(co[2,elem])),] ~ 
                  factors[factors %in% c(as.character(co[1,elem]),as.character(co[2,elem]))] , method =sim.method, permutations = 99999, strata=strat[factors %in% c(as.character(co[1,elem]),as.character(co[2,elem]))]);
    pairs = c(pairs,paste(co[1,elem],'vs',co[2,elem]));
    F.Model =c(F.Model,ad$aov.tab[1,4]);
    R2 = c(R2,ad$aov.tab[1,5]);
    p.value = c(p.value,ad$aov.tab[1,6])}
  
  p.adjusted = p.adjust(p.value,method=p.adjust.m)
  pairw.res = data.frame(pairs,F.Model,R2,p.value,p.adjusted)
  return(pairw.res)
  }