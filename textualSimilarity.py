import hashlib

class simHash():
    # tokenDict = {"token": [0, "hashValue"]}
    # The token dict is of the form where the key is the token from the tokenLst, and the
    # value is a list of 2 elements. On index 0, we have the frequency/weight of the token, and
    # on index 1 we have the hashEncoding corresponding to the token. 
    tokenDict = dict()
    simHashSet = set()
    
    
    def tokenDictionaryMapper(self, tokenLst: list) -> None:
    # This method takes the tokenLst as an attribute, and updates the tokenDict with the frequency/weight of 
    # the tokens in the tokenLst. It also updates the binaryHash value of the tokens.
        for token in tokenLst:
            try:
                # update the weight if token already in tokenDict.
                self.tokenDict[token][0] += 1
            except KeyError:
                # otherwise, create a new entry of the token in the tokenDict.
                self.tokenDict[token] = [1, ""]
    
        for key in self.tokenDict.keys():
            # First, we hash ever token using sha256 and hexdigest from the hashlib library. We then convert
            # the hexadecimal into an integer and then only consider the first 8 digits for simiplicity.
            # Reference to converting string to 32 bit hex number: https://stackoverflow.com/a/42089311
            # binaryHash = bin(int(hashlib.blake2b(digest_size = 32).hexdigest(), 16))
            binaryHash = bin(int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16))[2:34]
            
            # Then, convert the hex into a binary number using built-in bin(). Finally, update
            # the hashvalue as a binary in the tokenDict.
            self.tokenDict[key][1] = binaryHash
    
    @classmethod
    def simHashFingerprint(cls) -> int:
        # This method returns the fingerprint of the entire webpage.
        vector = []
        for index in range(32):
            number = 0
            # Iterate over all the tokens in tokenDict.
            for key in cls.tokenDict.keys():
                # Use simhashing technique to find an integer value to append to the length 8 list.
                if cls.tokenDict[key][1][index] == "1": number += cls.tokenDict[key][0]
                else: number -= cls.tokenDict[key][0]
            vector.append(number)
        # Declare the fingerprint string
        cls.tokenDict = dict()
        fingerPrint = ""
        for num in vector:
            # Iterate over the vector with 8 integers. Re-convert into binary
            # depending on the modularity of the number. 
            if num < 0: fingerPrint += "0"
            else: fingerPrint += "1"
        return fingerPrint
    
    
    def similarityChecker(self, simhash1: str, simhash2: str) -> bool:
        similarityIndex = 0
        thresholdLevel = 0.96875
        for index in range(len(simhash1)):
            # Find the similarityIndex given simhashes of 2 different webpages.
            if simhash1[index] == simhash2[index]: similarityIndex += 1
        # return a boolean value relative to the threshold value.
        similarityRatio = similarityIndex/32
        if similarityRatio >= thresholdLevel: return True
        else: return False
        