### Calculate standard error
se <- function(x){
  sd(x)/sqrt(length(x))
}

### Steal legend
g_legend <- function(a.gplot){
  tmp <- ggplot_gtable(ggplot_build(a.gplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)}

### Adjustment for DESeq
gm_mean = function(x, na.rm=TRUE){
  exp(sum(log(x[x > 0]), na.rm=na.rm) / length(x))
}

### DESeq2
deSEQ <- function(data, valuetest, cutoff = 0, alpha = 0.05){
  data_pruned <- prune_taxa(taxa_sums(data) > cutoff, data)
  de_data <- phyloseq_to_deseq2(data_pruned, valuetest)
  de_data2 <- DESeq(de_data, test="Wald", fitType="local")
  res_data <- results(de_data2, cooksCutoff = FALSE, pAdjustMethod = "BH")
  sig_data <- res_data[which(res_data$padj < alpha), ]
  sigtab_sherm <- cbind(as(sig_data, "data.frame"), as(tax_table(data_pruned)[rownames(sig_data), ], "matrix"))
}



# ### DESeq2
# Use this version is data has too many 0's (meaning the code above will result in an error)
# deSEQ <- function(data, valuetest, cutoff = 0, alpha = 0.05){
#   data_pruned <- prune_taxa(taxa_sums(data) > cutoff, data)
#   de_data <- phyloseq_to_deseq2(data_pruned, valuetest)
#   de_data_gm <- apply(counts(de_data), 1, gm_mean)
#   de_data_gm_esf <- estimateSizeFactors(de_data, geoMeans=de_data_gm)
#   de_data2 <- DESeq(de_data_gm_esf, test="Wald", fitType="local")
#   res_data <- results(de_data2, cooksCutoff = FALSE, pAdjustMethod = "BH")
#   sig_data <- res_data[which(res_data$padj < alpha), ]
#   sigtab_sherm <- cbind(as(sig_data, "data.frame"), as(tax_table(data_pruned)[rownames(sig_data), ], "matrix"))
# }



### NMDS Ellipses
veganCovEllipse <- function(cov, center = c(0, 0), scale = 1, npoints = 100) {
  theta <- (0:npoints) * 2 * pi/npoints
  Circle <- cbind(cos(theta), sin(theta))
  t(center + scale * t(Circle %*% chol(cov)))
}
