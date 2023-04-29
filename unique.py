import ics_subdomains

class Unique:
    """
    Unique objects helps determine unique urls,
    ignoring the fragmented parts of the url, and
    counts the number of unique urls.
    """
    url_set = set()
    url_counter = 0
    delete = 0
    """
    Initializer will set up a url set container
    that stores all the unique urls and initialize the
    unique url counter to 0.
    """

    @classmethod
    def remove_fragment(cls, url:str):
        """
        The function remove_fragment loops through a given url and
        will remove the fragment that is at the end of the
        url. This function will run O(N), as it goes through every
        character of the url.
        """
        no_fragment = True #boolean value that switches if a fragment is reached
        new_url = "" #url to return as it will be unique
        for c in url: #loops through url O(N) time
            if no_fragment:
                if 35 == ord(c): #determines the # which is a sign of a fragment
                    no_fragment = False #makes it false to prevent adding fragment characters
                else:
                    new_url += c #increment every character before the fragment
       
        if new_url not in cls.url_set: #increments the unique url counter if not in container
            cls.url_counter += 1
            ics_subdomains.icsSubdomains.addToSubdomain(new_url) # count number of new domains found
        
        cls.url_set.add(new_url) #adds the unique url to the set
        
        return new_url

if __name__ == "__main__":
    pass