# @Date: 2020/11/11
# @Author: Xue Chao
# @Description: Python script for preprocessing the GWAS summary statistics
# to obtain the standardized input file for SPA web applications (http://pmglab.top/spa).

import gzip,argparse,re,time
import filetype as ft
## static log method
def log(content):
    content=time.strftime("%Y-%m-%d %H:%M:%S [INFO] ", time.localtime(time.time()))+ "%s"%(content)
    # wt = FF.getWriter(self.logPath, True)
    print(content,flush=True)

def getLineByPath(filePath):
    isGzip = True
    try:
        if str(ft.guess(filePath).extension) == "gz":
            isGzip = True
    except:
        isGzip = False
    if isGzip:
        reader = gzip.open(filePath, "r")
    else:
        reader = open(filePath, "r")
    while True:
        line = reader.readline()
        if not line:
            reader.close()
            break
        if isGzip:
            lineArr = line.decode().strip('\n')
        else:
            lineArr = line.strip('\n')
        yield lineArr

def get_standard_GWAS_file(gwas,out,chr,pos,pvalue):
    log('start process')
    br=getLineByPath(gwas)
    header=re.split('\s+',br.__next__())
    idxs=[header.index(x.strip()) for x in [chr,pos,pvalue]]
    bw=gzip.open(out,'w')
    bw.write(('\t'.join(['CHR','POS','PVALUE'])+'\n').encode())
    raw=0
    qc=0
    for line in br:
        raw+=1
        arr=re.split('\s+',line)
        tmp=[]
        for idx in idxs:
            tmp.append(arr[idx])
        try:
            float(tmp[2])
            int(tmp[1])
        except:
            continue
        qc+=1
        bw.write(('\t'.join(tmp)+'\n').encode())
    bw.close()
    log(f'raw GWAS summary statistics variant number: {raw}; remain: {qc}')
    log('finish')


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'Preprocess GWAS summary statistic file for SPA.'
    parser.add_argument('--gwas', help='Input GWAS summary statistics file path')
    parser.add_argument('--out', help='Output GWAS summary statistics file path')
    parser.add_argument('--chr', help='chromosome number column name')
    parser.add_argument('--pos', help='base pair position (hg19/GRCh37) column name')
    parser.add_argument('--pvalue', help='P value column name')
    get_standard_GWAS_file(args.gwas,args.out,args.chr,args.pos,args.pvalue)
