import urllib.request
import io
import re

class Robot_Parse:
    def __init__(self, url):
        self.url_copy = url
        self.url = url
        self.made_request = False
        self.no_crawl = []
        self.can_crawl = []
        if self.url[-10:] == "robots.txt":
            self.inserted_robots = True
            self.url_copy = self.url_copy[:-11]
        else:
            self.inserted_robots = False

    def insert_robots(self):
        self.inserted_robots = True
        if self.url[-1] != "/":
            self.url += "robots.txt"
        else:
            self.url += "/robots.txt"

    def robots_request(self):
        self.made_request = True
        web_request = urllib.request.urlopen(self.url, data=None)
        self.data = io.TextIOWrapper(web_request, encoding='utf-8')
        
    def robots_read(self):
        crawl_mode = False
        for lines in self.data:
            if lines.startswith("User-agent: *") or lines.startswith("User-Agent: *"):
                crawl_mode = True
            if crawl_mode and lines.startswith("Disallow: /"):
                self.no_crawl.append(self.url_copy + lines[10:].rstrip())
            if crawl_mode and lines.startswith("Allow: /"):
                self.can_crawl.append(self.url_copy + lines[10:].rstrip())
            if crawl_mode and lines == "\n":
                break
        
    def original_url(self):
        return self.url_copy

    def no_crawl_links(self):
        return self.no_crawl

    def can_crawl_links(self):
        return self.can_crawl
if __name__ == "__main__":
    save = Robot_Parse("https://www.reddit.com/robots.txt")
    save.robots_request()
    save.robots_read()
    print(save.can_crawl_links())
    