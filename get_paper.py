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

## 以下改良中

def get_paper_sub():

    config = get_config()
    subject = config['subject']
    keywords = config['keywords']
    score_threshold = float(config['score_threshold'])

    day_before_yesterday = datetime.datetime.today() - datetime.timedelta(days=2)
    day_before_yesterday_str = day_before_yesterday.strftime('%Y%m%d')
    # datetime format YYYYMMDDHHMMSS
    arxiv_query = f'({subject}) AND ' \
                  f'submittedDate:' \
                  f'[{day_before_yesterday_str}000000 TO {day_before_yesterday_str}235959]'
    articles = arxiv.query(query=arxiv_query,
                           max_results=1000,
                           sort_by='submittedDate',
                           iterative=False)
    results = search_keyword(articles, keywords, score_threshold)

    return results

def calc_score(abst: str, keywords: dict) -> (float, list):
    sum_score = 0.0
    hit_keywords = []

    for word in keywords.keys():
        score = keywords[word]
        if word.lower() in abst.lower():
            sum_score += score
            hit_keywords.append(word)
    return sum_score, hit_keywords


def search_keyword(
        articles: list, keywords: dict, score_threshold: float
        ) -> list:
    results = []

    for article in articles:
        url = article['arxiv_url']
        title = article['title']
        abstract = article['summary']
        score, keywords = calc_score(abstract, keywords)
        if (score != 0) and (score >= score_threshold):
            result = Result(
                    url=url, title=title, abstract=abstract,
                    score=score, words=keywords)
            results.append(result)
    return results


def get_config() -> dict:
    file_abs_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_abs_path)
    config_path = f'{file_dir}/config.yaml' # file dir
    with open(config_path, 'r') as yml:
        config = yaml.load(yml)
    return config

        

