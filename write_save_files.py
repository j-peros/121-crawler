from ics_subdomains import icsSubdomains
import unique
from maxWordCount import maxWordCount

class Counter:

    count = 0

    @classmethod
    def count_pages(cls):
        if cls.count < 10:
            cls.count += 1
            return False
        elif cls.count > 10:
            cls.count = 1 # restart
            return False
        else: # write after every 250 crawls
            save_to_file()
            cls.count += 1
            return True

def save_to_file() -> None:
    """ Saves files of all data in case of restart """
    print("\n\n This ran \n\n")
    with open("unique_save.txt", "w") as f:
        f.write(f"{unique.Unique.url_counter}\n")
        f.writelines(unique.Unique.url_set)
    with open("maxWordCount_save.txt", "w") as f:
        f.write(f"{maxWordCount.maxWords}\n{maxWordCount.longestURL}")
    icsSubdomains.write_to_file()
        

def restarting_crawler() -> None:
    """ Adds data back in case of restart. """
    with open("unique_save.txt", "r") as f:
        Unique.url_counter = int(f.readline())
        for link in f:
            Unique.url_set.add(link)
    with open("maxWordCount_save.txt", "r") as f:
        maxWordCount.maxWords = int(f.readline())
        maxWordCount.longestURL = f.readline()
    icsSubdomains.read_from_file()