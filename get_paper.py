import arxiv
import csv
import pandas as pd
import os
import yaml
import datetime

def au_search(author):
  search = arxiv.Search(query ='au:"'+author+'"',max_results = 1,sort_by = arxiv.SortCriterion.SubmittedDate)
  return search

def writecsv(name,s_id,au,p_date,title):
    with open(name,"a",newline='') as f: 
        writer = csv.writer(f) 
        writer.writerow([s_id,au,p_date,title])

def readcsv(name):
    df = pd.read_csv(name, encoding="SHIFT_JIS")
    df_list = df["s_id"]
    id_list = df_list.tolist()
    return id_list

def get_author(name):
    df = pd.read_csv(name, encoding="SHIFT_JIS")
    df_list = df["author"]
    au_list = df_list.tolist()
    return au_list

def get_paper(dir_path):
    
    author_path=dir_path+"/author.csv"
    author_list = get_author(author_path)
    
    database =dir_path + "/database_blue_arXiv.csv"
    
    au_l = []
    pdate_l = []
    title_l = []
    url_l = []
    
    try:
        readcsv(database)
    except FileNotFoundError:
        print("mk",database)
        writecsv(database,"s_id","author","publish_date","title")
    
    for au in author_list:
      search = au_search(au)
    
      for result in search.results():
        s_id = result.get_short_id()
        p_date = result.published
        title = result.title
        url = result.pdf_url
    
        id_list = readcsv(database)
        
        if s_id in id_list:
            pass
        
        else:
            writecsv(database,s_id,au,p_date,title)
            au_l.append(au)
            pdate_l.append(p_date)
            title_l.append(title)
            url_l.append(url)
    return au_l,pdate_l,title_l,url_l
        

