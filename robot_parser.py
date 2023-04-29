import urllib.request, io, os, re
from urllib.parse import urlparse
class Robot_Parse:
    robots_dis = {} #key of unique domains and mapped to a list of disallowed links
    robots_all = {}
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
        self.url = self.sep_root_domain(url) #change the url depending if the url has a robots.txt in the path
        self.disallow_crawl = [] #list of links to not crawl
        self.allow_crawl = [] # list of links to crawl
        self.url_copy = self.url #url without the robots.txt
        self.insert_robots()

        
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
        ast_replace = "(\S*)" # used to replace the asterix character
        crawl_mode = False # Used to only look at user-agent: *
        
        for lines in self.data: #loop through the robots.txt file
            insert_line = "" #save re expression string
            if lines.startswith("User-agent: *") or lines.startswith("User-Agent: *"):
                crawl_mode = True #turned to true once we reach the info about our crawler
            if crawl_mode and lines.startswith("Disallow: /"):
                for char in lines[11:].rstrip():
                    if char == "*":
                        insert_line += ast_replace #replace the asterix with our re expression
                    elif char == ".":
                        insert_line += "[.]"
                    elif char == "?":
                        insert_line += "[?]"
                    elif char == "^":
                        insert_line += "[^]"
                    else:
                        insert_line += char #include the char
                #add the link to the disallowed list
                if (lines.rstrip()[-1] == "$"): #$ means that the expression must be at the end of the path
                    #expression so that this matches the subpath only at the end
                    self.disallow_crawl.append(os.path.join(self.url_copy, "(" + insert_line[:-1] + ")$"))
                else:
                    self.disallow_crawl.append(os.path.join(self.url_copy, insert_line))

            if crawl_mode and lines.startswith("Allow: /"):
                for char in lines[8:].rstrip():
                    if char == "*":
                        insert_line += ast_replace #replace the asterix with our re expression
                    elif char == ".":
                        insert_line += "[.]"
                    elif char == "?":
                        insert_line += "[?]"
                    elif char == "^":
                        insert_line += "[^]"
                    else:
                        insert_line += char #include the char
                #add the link to the disallowed list
                if (lines.rstrip()[-1] == "$"): #$ means that the expression must be at the end of the path
                    #expression so that this matches the subpath only at the end
                    self.allow_crawl.append(os.path.join(self.url_copy, "(" + insert_line[:-1] + ")$"))
                else:
                    self.allow_crawl.append(os.path.join(self.url_copy, insert_line))
    
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

    def sep_root_domain(self, given_url: str) -> str:
        # This function separates the link to only return the scheme and domain
        parse_link = urlparse(given_url)
        return parse_link.scheme + "://" + parse_link.netloc

def matching_robots(link: str) -> bool:
    call_parser = Robot_Parse(link)
    parser_disallow = disallowed(link, call_parser) #initiliazes the robot_parser class
    parser_allow = allowed(link, call_parser)

    if parser_disallow and not parser_allow:
        return False
    else:
        return True

def disallowed(link, parse_robots):
    root_url = parse_robots.sep_root_domain(link) #gets the root path
    if root_url in parse_robots.robots_dis.keys(): #determines if the root path already exists in dict
        for links in parse_robots.robots_dis[root_url]: #loops through the disallowed links
            if re.match(links, link): #matches the disallowed link to given link
                return True
    else:
        parse_robots.robots_request() #server creates a new request to the web
        parse_robots.robots_read() #reads the robots.txt file
        parse_robots.robots_dis[parse_robots] = parse_robots.disallow_crawl_links() #adds a disallowed list
        for links in parse_robots.disallow_crawl_links(): #loops through disallowed links
            if re.match(links, link): #sees if the disallowed link matches
                return True
    #no links that matches
    return False

def allowed(link, parse_robots):
    root_url = parse_robots.sep_root_domain(link) #gets the root path
    if root_url in parse_robots.robots_all.keys(): #determines if the root path already exists in dict
        for links in parse_robots.robots_all[root_url]: #loops through the allowed links
            if re.match(links, link) and links[-1] != "/": #matches the allowed link to given link
                return True
    else:
        parse_robots.robots_request() #server creates a new request to the web
        parse_robots.robots_read()#reads the robots.txt file
        parse_robots.robots_all[parse_robots] = parse_robots.allow_crawl_links() #adds a allowed list
        for links in parse_robots.allow_crawl_links(): #loops through allowed links
            if re.match(links, link) and links[-1] != "/": #sees if the allowed link matches
                return True
    #no links that matches
    return False
if __name__ == "__main__":
    pass
    
   
    