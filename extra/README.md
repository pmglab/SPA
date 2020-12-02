# Extra scripts for SPA
## Preprocess GWAS summary statistics file for SPA
Command: `python preprocessGWAS.py [options]`

Options:
```
--gwas GWAS      Input GWAS summary statistics file path
--out OUT        Output GWAS summary statistics file path
--chr CHR        chromosome number column name
--pos POS        base pair position column name
--pvalue PVALUE  P value column name
```

example: `python preprocessGWAS.py --gwas examples/gwas.sum.gz --out spa.gwas.sum.gz --chr chr_col --pos pos_col --pvalue p_col`

