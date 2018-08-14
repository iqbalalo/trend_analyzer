import requests
from bs4 import BeautifulSoup as bs
from collections import Counter
from crawler.MyHTMLParser import MyHTMLParser
from sqlite import Sqlite
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify

# Initiate blueprint
crawler_blueprint = Blueprint('crawler', __name__, template_folder='templates', url_prefix="/crawl")


# Routes
@crawler_blueprint.route('/', methods=['GET'])
def get():
    urls = request.args.get('urls')
    cr = Crawler(urls)
    cr.crawl(urls[0])
    
    return render_template('home.html', his_records=data_from_his_server(), app_records=data_from_app_server())


class Crawler:
    
    def __init__(self, init_urls):
        urls = [init_urls]
        visited = []
        sq = Sqlite("trend_data.db")
        
    def crawl(self, url):
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
        links = self.check_link(url, links)
        links = [self.fix_link_path(self.urls[0], i) for i in links]
        self.urls.extend(links)
        
        # added visited link
        self.visited.append(url)
        # pop links from old list
        self.urls.pop(0)
        
        if len(self.visited) < 5:
            print("visited: " + str(len(self.visited)) + " links")
            data_str = "('%s','%s','%s','%s','%s','%s')" % (url, datetime.now().strftime("%Y-%m-%d %H:%M"), ', '.join(parser.metakeywords),
                                                            ', '.join(parser.hashtags), ', '.join(links), ' '.join(parser.data))
            res = self.sq.insert("data", data_str)
    
            if res is True:
                self.crawl(self.urls[0])
            else:
                print(res)
                return False
        else:
            return "Finished crawling.."
    
    def check_link(self, parent_url, links):
        skip_link_with_words = [".pdf", ".jpeg", ".jpg", ".png", ".mp3", "#", "github", "mailto"]
        skip_links = set([i.strip("/") for i in links for j in skip_link_with_words if j in i or parent_url == i.strip("/")])
        skip_links = list(set(links) - skip_links)
        return skip_links
    
    def search_keywords(self, keywords, words):
        res = dict(Counter([i for i in keywords for j in words if i.lower() in j.lower()]))
        return res
    
    def fix_link_path(self, parant_url, url_to_fix):
        if "http://" in url_to_fix or "https://" in url_to_fix:
            return url_to_fix
        elif "www." in url_to_fix and 'http' not in url_to_fix:
            return "http://" + url_to_fix
        else:
            return parant_url + "/" + url_to_fix
    
    def close_connection(self):
        self.sq.close_connection()