from html.parser import HTMLParser
import requests
import re

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.start_tag = ""
        self.end_tag = ""
        self.data = []

    def handle_starttag(self, tag, attrs):
        self.start_tag = tag

    def handle_endtag(self, tag):
        self.end_tag = tag

    def handle_data(self, data):
        if self.start_tag == self.end_tag and self.start_tag != "script":
            data = data.strip()
            data = re.sub("[(){}.,|>]", '', data)
            data = " ".join(data.split())
            if data:
                self.data.append(data)

# instantiate the parser and fed it some HTML
# parser = MyHTMLParser()
# parser.feed(requests.get("http://iqbalhossain.info").text)
# print(parser.data)