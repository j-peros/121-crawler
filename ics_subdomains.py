import re
from urllib.parse import urlparse
import json
# for tracking question #4

class icsSubdomains:

    subdomainDict = {} # key: directory -> val: counter

    @classmethod
    def addToSubdomain(cls, link:str) -> None:
        """ If a subdomain exists and has not been found before, add it to this dictionary. If it has been found, increment the counter for that subdomain. """
        link = urlparse(link)
        path_subdomain = re.sub("\/[^\/]*$", "", link.path)
        subdomain = link.netloc + path_subdomain + '/'

        # Strips the page, and returns [site]/[most recent directory]"""
        # i.e. www.ics.uci.edu.com/about/us -> www.ics.uci.edu.com/about/
        if link.scheme in set(["http", "https"]) and re.match('\S*.ics.uci.edu$', link.netloc):    
            try:
                cls.subdomainDict[subdomain] += 1
            except KeyError: # directory does not exist
                cls.subdomainDict[subdomain] = 1
        

    @classmethod
    def write_to_file(cls, filename = "subdomain_dictionary") -> None: # Prep for restart
        assert type(filename) is str # name should be a string
        filename += ".json"
        with open(filename, "w") as f:
            json.dump(cls.subdomainDict, f)

    @classmethod
    def read_from_file(cls, filename = "subdomain_dictionary") -> None: # Restart
        assert type(filename) is str 
        filename += ".json"
        with open(filename, "r") as f:
            cls.subdomainDict = json.load(f)