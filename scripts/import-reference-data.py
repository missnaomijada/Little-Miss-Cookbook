"""Rebuild reference data from local Open Recipe Archive and USDA SR Legacy CSV downloads.
Usage: python scripts/import-reference-data.py ARCHIVE_DIR USDA_CSV_DIR
No generated variants: counts refer to source records; modern tutorials stay separate.
"""
import csv,gzip,json,re,sys,subprocess,hashlib
from pathlib import Path
from collections import Counter
archive,usda=map(Path,sys.argv[1:3]); out=Path(__file__).resolve().parents[1]/'data';out.mkdir(exist_ok=True)
def gz(name,data):
 raw=json.dumps(data,ensure_ascii=False,separators=(',',':')).encode();(out/(name+'.json.gz')).write_bytes(gzip.compress(raw,mtime=0))
def csvrows(name):return list(csv.DictReader((usda/(name+'.csv')).open()))
allergy=re.compile(r'\b(almonds?|nuts?|peanuts?|walnuts?|hazelnuts?|cashews?|pecans?|pistachios?|macadamias?|marzipan|praline|bananas?|plantains?)\b',re.I)
rows=[];seen=set(); omitted=0
for p in sorted(archive.glob('collections/*/recipes.jsonl')):
 for line in p.open():
  r=json.loads(line);key=(r['collection'],r['slug'])
  if key in seen:continue
  seen.add(key)
  if r.get('license')!='public-domain' or not r.get('body') or not r.get('source_url'):omitted+=1;continue
  rows.append(r)
index=[]
for k in range(0,len(rows),500):
 chunk=rows[k:k+500];num=k//500
 gz('archive-'+str(num),chunk)
 for j,r in enumerate(chunk):index.append([num,j,r['title'],r['collection'],r['culture'],r['source_year'],bool(allergy.search(r['title']+' '+r['body']))])
gz('archive-index',index)
cats={r['id']:r['description'] for r in csvrows('food_category')}
foods={r['fdc_id']:{'id':r['fdc_id'],'title':r['description'],'category':cats.get(r['food_category_id'],'Other'),'nutrients':{}} for r in csvrows('food')}
selected={'1008':'Energy (kcal)','1003':'Protein (g)','1004':'Fat (g)','1005':'Carbohydrate (g)','1079':'Fibre (g)','1093':'Sodium (mg)'}
for r in csvrows('food_nutrient'):
 if r['fdc_id'] in foods and r['nutrient_id'] in selected and r['amount']!='':foods[r['fdc_id']]['nutrients'][selected[r['nutrient_id']]]=float(r['amount'])
gz('foods',list(foods.values()))
manifest={'archiveRecords':len(rows),'foodRecords':len(foods),'modernRecipes':len(json.loads((out.parent/'recipes-data.js').read_text().split('=',1)[1].strip().rstrip(';'))),'techniqueLessons':14,'collections':dict(Counter(r['collection'] for r in rows)),'foodCategories':dict(Counter(r['category'] for r in foods.values())),'sourceArchiveCommit':subprocess.check_output(['git','-C',str(archive),'rev-parse','HEAD'],text=True).strip(),'archiveSource':'https://github.com/AdamBouhmad/open-recipe-archive','foodSource':'https://fdc.nal.usda.gov/download-datasets/','foodRelease':'SR Legacy April 2018','importDate':'2026-10-01','omittedArchiveRecords':omitted,'countsNote':'Source records, including historical variants and separate raw/cooked food forms. Not counts of distinct ingredients, tested recipes or modern lessons.'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'archive':len(rows),'foods':len(foods),'compressedBytes':sum(p.stat().st_size for p in out.glob('*.gz')),'files':len(list(out.glob('*')))}))
