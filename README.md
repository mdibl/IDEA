# This repo is for the development of the Integrated Differential Expression Analyzer.

## RoadMap

### Overview: 
  
  A programmatic approach to go beyond p-value and log-foldchange limits on differential gene expression, by using known connections (in the explicit form of the STRING database) as a guided means of going beyond rigid thresholds, using stored biological information to reduce the likelihood of false positives.

### Inputs:

  Differential Expression Matrix: Tab-separated file, with informative column headers. We will work with DESeq2 output, but it is very possible that other programs such as edgeR or limma will also be of interest, so we will want to make the program robust for switching between these.
Initial threshold variables: (Probably best input as either json or yml). These are the “harsh thresholds” with which we typically filter a DE expression output. Typically, this will include at least (1) adjusted p-value (padj in DESeq2 output) and (2) estimated magnitude of change (log2foldchange in DESeq2), but could also include (3) the estimated error on the change estimate (l2fcSE in DESeq2) and (4) average expression level (baseMean in DESeq2).
Relaxed threshold variables: (also best as json or yml). These can include any of the variables used in the “initial threshold variables” (though likely not padj), with the addition of also the unadjusted p-value.

### Note 1: 

  We will likely want to come up with a means of defining the nature of the threshold, since it could be a one-sided test (<, >, <=, or >= for example), a two-sided test (x < a || x > b), or a test on a transformed variable (|x| < a, |x| >= b, log(x) > a.

### Note 2: 
  It is also probably worth our time to define some bounds to put on variables or the resulting size of the gene lists that are tested BEFORE any external requests for information are made. Sanity checks on the data, which can prevent ridiculous behavior. It’s always better the catch errors or typos early rather than late.

### Steps to be carried out in the main algorithm:

Open inputs (parameters and DE gene file). Make sure all sanity tests have been passed

Use initial thresholds to identify GS1: genes that pass the threshold. Extract the list of gene identifiers

Form a query for the String Database, and send GS1 to get all connected genes from the same organism in STRING (FOR NOW, take all connections => we may eventually want to filter based on the nature of the connection, such as predicted or verified, or different classes of supporting data)

Reduce the returned gene list to only unique new IDs (not part of GS1)

Intersect the returned unique list with the original DE gene file, and then further select those genes that pass the “relaxed threshold variables” and then add these genes to GS1 => GS2

Repeat steps 3 through 5, always advancing from GSn-1 to GSn, stopping when GSn == GSn-1 (and also to be safe have an alternative maximum number of queries). Keep track of the iteration number on which each gene is added to the list, as well

Return the final set of genes.
