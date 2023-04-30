from maxWordCount import *
from ics_subdomains import icsSubdomains
from unique import Unique
import scraper

def create_report() -> None:
    """
    This function creates a report to answer the 4 questions from Assignment 2.
    The call to the function is in launch.py. After crawling, this function will
    be called
    """
    with open("reports.txt", "w") as report:
        # writing the number of unique pages
        report.write(f"1. The number of unique pages found is: {Unique.url_counter}\n")
        # writing the maximum number of words from the crawled webpages
        report.write(f"2. The maximum number of words overall the webpages crawled is: {maxWordCount.maxWords}\n")
        report.write(f"And the url with these max words is: {maxWordCount.longestURL}.\n")
        # writing the 50 most common words besides stop words
        fiftyCommonLst = scraper.top_words()
        report.write(f"3. The 50 most common words across all webpages crawled are:\n")
        for index in range(len(fiftyCommonLst)):
            report.write(f"{index}. {fiftyCommonLst[index]}, frequency = {scraper.word_counter(fiftyCommonLst[index])}.\n")
        # writing the pair of subdomains and number of unique pages detected
        report.write("""4. Here is a list of all the subdomains found in the ics.uci.edu domain in alphabetical order, 
                    along with the number of unique pages detected in each subdomain:\n""")
        for key, value in icsSubdomains.subdomainDict.items():
            report.write(f"{key}, {value}\n")
    report.close()
