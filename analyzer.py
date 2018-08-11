import requests
import re
from bs4 import BeautifulSoup as bs
from collections import Counter
from textblob import TextBlob
from MyHTMLParser import MyHTMLParser

urls = []
visited = []
search_result = []


def crawl(url):
    parser = MyHTMLParser()
    html = requests.get(url)
    parser.feed(html.text)
    soup = bs(html.text, features="lxml")
    # text = soup.get_text()
    # text = re.sub("\n|\r|{|}|>>|\xa0", " ", text)
    # words = re.findall(r'\S+', c_res.text)
    # tb = TextBlob(text)
    # tags = [i for i in tb.tags if (i[1] == 'NN' and len(i[0]) > 3) or (i[1] == 'NNP' and len(i[0]) > 2) or
    #         (i[1] == 'JJ' and len(i[0]) > 3) or
    #         i[1] == 'JJR' or i[1] == 'VBN']
    # text = ' '.join([i[0] for i in tags if 'google' not in i[0]])
    #
    # find links
    links = [a['href'] for a in soup.find_all('a', href=True)]
    links = check_link(url, links)
    links = [fix_link_path(urls[0], i) for i in links]
    urls.extend(links)

    search_result.append({"url": url, "links": links,
                          "hashtags": parser.hashtags, "keywords": parser.metakeywords, "data": parser.data})
    
    # added visited link
    visited.append(url)
    # pop links from old list
    urls.pop(0)
    
    if len(visited) < 2:
        print("visited: " + str(len(visited)) + " links")
        crawl(urls[0])
    else:
        return


def check_link(parent_url, links):
    skip_link_with_words = [".pdf", ".jpeg", ".jpg", ".png", ".mp3", "#", "github", "mailto"]
    skip_links = set([i.strip("/") for i in links for j in skip_link_with_words if j in i or parent_url == i.strip("/")])
    skip_links = list(set(links) - skip_links)
    return skip_links


def search_keywords(keywords, words):
    res = dict(Counter([i for i in keywords for j in words if i.lower() in j.lower()]))
    return res


def fix_link_path(parant_url, url_to_fix):
    if "http://" in url_to_fix or "https://" in url_to_fix:
        return url_to_fix
    else:
        return parant_url + "/" + url_to_fix


urls.append("http://www.iqbalhossain.info")
crawl(urls[0])
print(search_result)
