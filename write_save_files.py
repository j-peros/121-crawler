import ics_subdomains
import unique
import maxWordCount

def shutting_down() -> None:
    """ Saves files of all data in case of restart """
    with open("unique_save.txt", "w") as f:
        f.write(f"{unique.url_counter}\n")
        f.writelines(unique.url_set)
    with open("maxWordCount_save.txt", "w") as f:
        f.write(f"{maxWordCount.maxWords}\n{maxWordCount.longestURL}")
    with open("frequency.txt", "w") as f:
        pass
    ics_subdomains.icsSubdomains.write_to_file()
        

def restarting_crawler() -> None:
    """ Adds data back in case of restart. """
    with open("unique_save.txt", "r") as f:
        unique.url_counter = int(f.readline())
        for link in f:
            unique.url_set.add(link)
    with open("maxWordCount_save.txt", "r") as f:
        maxWordCount.maxWords = int(f.readline())
        maxWordCount.longestURL = f.readline()
    with open("frequency.txt", "r") as f:
        for line in f:
            pass
    ics_subdomains.icsSubdomains.read_from_file()