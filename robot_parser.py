import urllib.request
import io
import os
from urllib.parse import urlparse
class Robot_Parse:
    robots_dict = {} #key of unique domains and mapped to a list of disallowed links
    """
    The Robot_Parse class is used primarily
    for reading and parsing robots.txt files
    """
    def __init__(self, url):
        """
        Initializer takes in a url and sees if the url
        contains robots.txt in the path. If it does, then calling
        insert_robots function will not be necessary. Otherwise, we need to call insert_robots.
        """
        self.url = url #change the url depending if the url has a robots.txt in the path
        self.disallow_crawl = [] #list of links to not crawl
        self.allow_crawl = [] # list of links to crawl
        if self.url[-10:] != "robots.txt": # condition to see if it ends with robots.txt
            self.insert_robots()
            self.url_copy = url #url without the robots.txt
        else:
            self.url_copy = url[:-10]
        
    def insert_robots(self) -> None:
        """
        This function gets called if a url passed in Robot_Parse
        does not contain Robots.txt at the end of the path
        """
        if self.url[-1] == "/":
            self.url += "robots.txt"
        else:
            self.url += "/robots.txt"

    def robots_request(self) -> None:
        """
        This function makes a request to access the weblink
        that contains the robots.txt file
        """
        web_request = urllib.request.urlopen(self.url, data=None)
        self.data = io.TextIOWrapper(web_request, encoding='utf-8')
        
    def robots_read(self) -> None:
        """
        This function reads the robots.txt file
        and concatenates what links are disallowed and allowed
        as a re expression. This can be used to match such
        expressions with other links.
        """
        ast_replace = "\S*" # used to replace the asterix character
        crawl_mode = False # Used to only look at user-agent: *
        
        for lines in self.data: #loop through the robots.txt file
            insert_line = "" #save re expression string
            if lines.startswith("User-agent: *") or lines.startswith("User-Agent: *"):
                crawl_mode = True #turned to true once we reach the info about our crawler
            if crawl_mode and lines.startswith("Disallow: /"):
                line = lines[10:].rstrip() #get rid of the "Disallow" /"
                for char in line:
                    if char == "*":
                        insert_line += ast_replace #replace the asterix with our re expression
                    else:
                        insert_line += char #include the char
                #add the link to the disallowed list
                if (line[-1] == "$"): #$ means that the expression must be at the end of the path
                    #expression so that this matches the subpath only at the end
                    self.disallow_crawl.append(self.url_copy + "(" + insert_line[:-1] + ")$")
                else:
                    self.disallow_crawl.append(self.url_copy + insert_line)

            if crawl_mode and lines.startswith("Allow: /"):
                line = lines[7:].rstrip() #get rid of the "Disallow" /"
                for char in line:
                    if char == "*":
                        insert_line += ast_replace #replace the asterix with our re expression
                    else:
                        insert_line += char #include the char
                #add the link to the disallowed list
                if (line[-1] == "$"): #$ means that the expression must be at the end of the path
                    #expression so that this matches the subpath only at the end
                    self.allow_crawl.append(self.url_copy + "(" + insert_line[:-1] + ")$")
                else:
                    self.allow_crawl.append(self.url_copy + insert_line)
    
            if crawl_mode and lines == "\n": #done parsing
                break
        
    def original_url(self) -> str:
        #returns the original link without the robots.txt
        return self.url_copy
     

    def disallow_crawl_links(self) -> list:
        #returns a list of links that denies crawling
        return self.disallow_crawl

    def allow_crawl_links(self) -> list:
        # returns a list of links that allows crawling
        return self.allow_crawl

    def sep_root_domain(self) -> str:
        # This function separates the link to only return the scheme and domain
        parse_link = urlparse(self.url_copy)
        return os.path.join(parse_link.scheme + ":", parse_link.netloc)
    
    def check_existing_links(self):
        

def matching_robots(link: str) -> bool:
    parse_robots = Robot_Parse(link)
    parse_robots.robots_request()
    parse_robots.robots_read()

if __name__ == "__main__":
    
    

    