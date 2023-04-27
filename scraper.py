import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from maxWordCount import *
from ics_subdomains import icsSubdomains
from low_text_info import low_textual_content
import unique

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    # maxWord object to keep track of maxWords over all the webpages.
    # tokenLst of all tokens of the current webpage being crawled.
    # Updates the maxWordCount if current webpage
    # has more words than the recorded maxWords.
    
    if resp.status >= 300 and resp.status < 400:
        pass
    if resp.status != 200 or resp.raw_response.content is None:
        return list()
    
    soup = BeautifulSoup(resp.raw_response.content, "html.parser")
    extracted_links = set()

    maxWord = maxWordCount()
    tokenLst = maxWord.tokenizer(soup)

    if not low_textual_content(tokenLst, soup.find_all()):
        return list() # this page has low textual content
    
    maxWord.updateURL(tokenLst, resp.url)
    extracted_links = set()
    for link in soup.find_all('a'):
        cur_url = link.get('href')
        if cur_url is None:
            continue
        extracted_links.add(cur_url[:cur_url.find('#')])
       
    return list(extracted_links)
        
def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        url = unique.Unique.remove_fragment(url) # remove fragment from url
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not re.match('\S*.ics.uci.edu$|\S*.cs.uci.edu$|\S*.informatics.uci.edu$|\S*.stat.uci.edu$', parsed.netloc):
            return False # \S* matches any character before, so we don't have to worry if www is there or not, and $ makes sure the domain ends after that
        icsSubdomains.addToSubdomain(parsed) # counts the found pages, rather than the crawled pages
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
