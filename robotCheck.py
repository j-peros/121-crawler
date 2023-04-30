import urllib.robotparser

class RobotCheck:

    robotFileParser = {} # key(str -> domain) : value(RobotFileParser)

    @classmethod
    def checkURL(cls, scheme:str, domain:str, url:str) -> bool:
        """ Checks the robots.txt file. If it exists, check if the URL can be checked. If DNE, return True (can be crawled)"""
        if domain not in cls.robotFileParser:
            cls.robotFileParser[domain] = {"rp": urllib.robotparser.RobotFileParser(), "been_checked": False} # been_checked: if sitemap checked, rp: robotparser
            try:
                cls.robotFileParser[domain]["rp"].set_url(scheme + "://" + domain + "/robots.txt")
                cls.robotFileParser[domain]["rp"].read()
                return cls.robotFileParser[domain]["rp"].can_fetch("IR US23 80908952, 51317074, 49766190, 90722907", url)
            except Exception as E: # connection error, robots.txt DNE (we can crawl)
                cls.robotFileParser[domain]["rp"] = None
                return True
        
        else: # we already have the robots.txt
            return cls.robotFileParser[domain]["rp"] is None or cls.robotFileParser[domain]["rp"].can_fetch("IR US23 80908952, 51317074, 49766190, 90722907", url)
            # domain exists and does not have a robots.txt (None) OR robots.txt allows us to fetch URL
    
    @classmethod
    def get_sitemap(cls, domain:str) -> list:
        """ Returns the sitemap iff the site is valid and has not returned the sitemaps before"""
        if cls.robotFileParser[domain]["rp"] is None or cls.robotFileParser[domain]["been_checked"]:
            return [] # no robots.txt (None) or has already been checked
        else:
            cls.robotFileParser[domain]["been_checked"] = True # now it has been checked
            sitemaps = cls.robotFileParser[domain]["rp"].site_maps()
            return sitemaps if sitemaps is not None else []
