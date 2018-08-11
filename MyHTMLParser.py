from html.parser import HTMLParser
import re

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.start_tag = ""
        self.end_tag = ""
        self.data = []
        self.hashtags = []
        self.metakeywords = []

    def handle_starttag(self, tag, attrs):
        self.start_tag = tag
        if tag == "meta":
            if len(attrs)>=2 and 'keyword' in attrs[0] and 'content' in attrs[1]:
                keys = self.clean_data(attrs[1][1])
                self.metakeywords.extend(keys.split())
        
    def handle_endtag(self, tag):
        self.end_tag = tag

    def handle_data(self, data):
        if self.start_tag == self.end_tag and self.start_tag != "script":
            data = self.clean_data(data)
            tags = re.findall("(#[A-Za-z0-9_-]+)", data)
            if tags:
                self.hashtags.extend(tags)
            if data:
                self.data.append(data)
    
    def clean_data(self, data):
        data = data.strip()
        data = re.sub("[(){}.,|>'+*~]", '', data)
        data = re.sub(r'"', '', data)
        data = re.sub("([0-9-]+)", '', data)
        data = " ".join(data.split())
        return data