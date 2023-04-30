import urllib.robotparser
from urllib.parse import urlparse
from usp.tree import sitemap_tree_for_homepage
class Robot_Parse:
    def __init__(self, url):
        """
        Initializer takes in a url and sees if the url
        contains robots.txt in the path. If it does, then calling
        insert_robots function will not be necessary. Otherwise, we need to call insert_robots.
        """
        self.url = self.sep_root_domain(url) #change the url depending if the url has a robots.txt in the path
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

    def original_url(self) -> str:
        #returns the original link without the robots.txt
        return self.url_copy

    def robots_url(self) -> str:
        return self.url

    def sep_root_domain(self, given_url: str) -> str:
        # This function separates the link to only return the scheme and domain
        parse_link = urlparse(given_url)
        return parse_link.scheme + "://" + parse_link.netloc

def matching_robots(link: str) -> bool:
    call_parser = Robot_Parse(link)
    rp = urllib.robotparser.RobotFileParser()
    site_map(rp)
    rp.set_url(call_parser.robots_url())
    return rp.can_fetch("*", link)


if __name__ == "__main__":
    pass
    
   
    