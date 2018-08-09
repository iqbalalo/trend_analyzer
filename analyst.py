import requests
import re
from bs4 import BeautifulSoup as bs
from collections import Counter
from textblob import TextBlob

keywords_to_skip = [",", "img", '']
skip_link_with_words = [".pdf", ".jpeg", ".jpg", ".png", ".mp3", "#", "github", "mailto"]
links = ["http://www.iqbalhossain.info"]
visited = []
search_result = []

def crawl(url):
    print(url)
    html = requests.get(url)
    soup = bs(html.text, features="lxml")
    text = soup.get_text()
    text = re.sub("\n|\r|{|}|>>|\xa0", " ", text)
    # words = re.findall(r'\S+', c_res.text)
    tb = TextBlob(text)
    tags = [i for i in tb.tags if (i[1] == 'NN' and len(i[0]) > 3) or (i[1] == 'NNP' and len(i[0]) > 2) or
            (i[1] == 'JJ' and len(i[0]) > 3) or
            i[1] == 'JJR' or i[1] == 'VBN']
    text = ' '.join([i[0] for i in tags if 'google' not in i[0]])

    # find links
    tmp_links = [a['href'] for a in soup.find_all('a', href=True)]

    # remove skip links from founded links
    skip_links = set([i for i in tmp_links for j in skip_link_with_words if j in i])
    skip_links = list(set(tmp_links) - skip_links)

    # Recheck problamatic link
    skip_links = [fix_link_path(links[0], i) for i in skip_links]

    # add to links list
    links.extend(skip_links)
    if text:
        search_result.append({"link": url, "result": text})
    
    # added visited link
    visited.append(url)

    # pop links from old list
    links.pop(0)

    if len(visited) < 3:
        print("visited: " + str(len(visited)) + " links")
        crawl(links[0])
    else:
        return


def search_keywords(keywords, words):
    res = dict(Counter([i for i in keywords for j in words if i.lower() in j.lower()]))
    return res


def fix_link_path(parant_url, url_to_fix):
    if "http://" in url_to_fix or "https://" in url_to_fix:
        return url_to_fix
    else:
        return parant_url + "/" + url_to_fix


crawl(links[0])
print(links, search_result)
