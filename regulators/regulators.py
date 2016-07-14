import requests
import re

targetGenes = [    'ackA',    'ahpC',    'ahpF',    'ald',    'alsD',    'ansA',    'ansB',    'arsC',    'citB',    'citG',    'citZ',    'clpC',    'clpE',    'clpP',    'comQ',    'comX',    'ctaA',    'ctc',    'ctsR',    'cysC',    'cysH',    'cysK',    'cysP',    'degU',    'dfrA',    'dnaA',    'dnaN',    'etfB',    'fabD',    'fabG',    'folB',    'folC',    'folK',    'fur',    'glyA',    'groEL',    'groES',    'gtaB',    'guaA',    'guaD',    'hemA',    'hemC',    'hemL',    'hemX',    'hemZ',    'hisC',    'hrcA',    'icd',    'ilvC',    'infB',    'iolS',    'lmrA',    'lmrB',    'lytA',    'lytC',    'mcsA',    'mcsB',    'mdh',    'mecA',    'menD',    'mraY',    'mtn',    'nadE',    'nusA',    'odhB',    'opuAA',    'pabA',    'pabB',    'pabC',    'pbpD',    'pbuX',    'pheS',    'pheT',    'plsX',    'pta',    'ptsG',    'pucA',    'pucB',    'pucL',    'pucR',    'purA',    'purB',    'purC',    'purD',    'purE',    'purF',    'purH',    'purK',    'purL',    'purM',    'purN',    'purQ',    'purS',    'purT',    'pyrAA',    'pyrAB',    'pyrB',    'pyrC',    'pyrD',    'pyrE',    'pyrF',    'pyrK',    'pyrP',    'pyrR',    'rbsB',    'ribA',    'ribD',    'ribE',    'ribH',    'rsbS',    'rsbT',    'rsbU',    'rsbV',    'rsbW',    'rsbX',    'sat',    'sbp',    'secA',    'sigB',    'sinR',    'smc',    'spoVE',    'tagA',    'tagB',    'tagD',    'tagE',    'tagF',    'thyB',    'trpA',    'tyrA',    'xpt',    'xylA',    'yaaB',    'yacK',    'yazB',    'yazC',    'ycdA',    'ycdH',    'ycdI',    'yceA',    'yceC',    'yceD',    'yfkH',    'yfkI',    'yfkJ',    'yhaG',    'yhcL',    'yjbC',    'yjbD',    'yjeA',    'ykuJ',    'ykuK',    'ykuL',    'ykuN',    'ykuO',    'ykuP',    'ykzF',    'ylnD',    'ylnE',    'ylnF',    'ylpC',    'ylxM',    'ylxP',    'ylxQ',    'ylxR',    'ylxS',    'ylxW',    'ylxX',    'yoeB',    'yqcK',    'yrhA',    'yrhB',    'yrhC',    'yrrT',    'yrxA',    'ytrE',    'ytrF',    'yvaZ',    'yvbA',    'yvgQ',    'yvgR',    'yxeK',    'yxeL',    'yxeM',    'yxeN',    'yxeO',    'yxeP',    'yxxG']
#targetGenes = [   'yhaG' ]

out = open("subtiwiki-regulators.csv","w")
out.write('target,regulation,gene1,gene2,gene3,gene4,pubmed\n')

sectionPattern = re.compile("<h3>Regulatory mechanism</h3>("
                    "("  "[^<]*"  "</?(a|li)[^>]*>"  ")*"
                    "[^<]*"
        ")(<h3>|<h2>)",re.DOTALL | re.IGNORECASE)


for target in targetGenes:

    page = requests.get('http://www.subtiwiki.uni-goettingen.de/bank/index.php?gene=' + target)
    text = page.text;
    sectionResult = sectionPattern.search(text)

    if not (sectionResult is None):
        sectionText = sectionResult.group(1)
        rowPattern = re.compile("<li>(" 
                "("  "[^<]*"  "</?a[^>]*>"  ")*"
                "[^<]*"
            ")</li>")
        rows = [x[0] for x in rowPattern.findall(sectionText)]
    
        if len(rows) == 0 :
            out.write(target + ",nothing,,,,,\n")
        else:
            genePattern = re.compile(r'index\.php\?(gene|title)=([^"]*)"')
            repressPattern = re.compile("repress|inhibit")
            activatePattern = re.compile("activat")
            pubmedPattern = re.compile(r'https?://www\.ncbi\.nlm\.nih\.gov/pubmed/[0-9]*')

            for row in rows:
                nonUniqueGenes = [x[1][:1].lower() + x[1][1:] for x in genePattern.findall(row)] #lowercasing the first letter of all matches (the first index is the match index)
                genes = [e for i, e in enumerate(nonUniqueGenes)  if nonUniqueGenes.index(e) == i]   #filter out duplicates but keep order
                if repressPattern.search(row):
                    if activatePattern.search(row):
                        effect = "mixed"
                    else:
                        effect = "repression"
                else :
                    if activatePattern.search(row):
                        effect = "activation"
                    else:
                        effect = "?"

                out.write(target + "," + effect)

                for i in range(0,4):
                    out.write(',')
                    if len(genes) > i:
                        out.write(genes[i])
                
                out.write(',')
                pubmedRefs = pubmedPattern.findall(row) 
                out.write(";".join(pubmedRefs))
                out.write('\n')
    else:
        out.write(target + ", no-section\n")


out.close()