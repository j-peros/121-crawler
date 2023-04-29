from maxWordCount import *
from ics_subdomains import icsSubdomains
from unique import Unique


with open("reports.txt", "w") as report:
    report.write(f"1. The number of unique pages found is: {Unique.url_counter}",)
    report.write(f"2. The maximum number of words overall the webpages crawled is: {maxWordCount.maxWords}\n")
    report.write("""4. Here is a list of all the subdomains found in the ics.uci.edu domain in alphabetical order, 
                along with the number of unique pages detected in each subdomain:\n""")
    for key, value in icsSubdomains.subdomainDict.items():
        report.write(f"{key}, {value}\n")
report.close()
