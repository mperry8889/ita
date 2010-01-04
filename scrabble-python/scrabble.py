#!/usr/bin/python

# provide the intersection of two lists, allowing for 
# duplicate items
def intersect(word, letters): 
    
    # generate a dict of {letter: times used} for both the
    # word and letters inputs
    wordDict = {}
    letterDict = {}
    for letter in word:
        try:
            wordDict[letter] += 1
        except KeyError:
            wordDict[letter] = 1

    for letter in letters:
        try:
            letterDict[letter] += 1
        except KeyError:
            letterDict[letter] = 1

    # generate a mapping of all letters, and the number of occurances
    # of each. 
    all = {}
    for i in letterDict.iterkeys():
        all[i] = 0
    for j in wordDict.iterkeys():
        all[j] = 0

    for letter in all:
        try:
            # if the letter is used more times in the available
            # letters than in the word, then it's ok to use
            if letterDict[letter] >= wordDict[letter]:
                all[letter] = wordDict[letter]
           
            # otherwise it's not, so discard it
            else:
                all[letter] = 0
        except KeyError:
            pass

    # generate the return array
    result = []
    for letter in all:
        for i in range(all[letter]):
            result.append(letter)
    
    return result
    

def scrabble(wordlist, letters):
    result = []

    # for each word in the list, calculate the intersection
    # between the set of letters in the word and the set of
    # given letters.  note this can't use python's Set features
    # because python Sets require elements to be unique
    for word in wordlist:
        if sorted(intersect(word, letters)) == sorted(word):
            result.append(word)

    # calculate the longest match
    longest_match = 0
    for i in result:
        longest_match = max(longest_match, len(i))

    # ... and return
    return [i for i in result if len(i) == longest_match]


if __name__ == "__main__":
    import sys

    letters = sys.argv[2:]
    file = sys.argv[1]

    words = []

    fp = open(file)
    while 1:
        line = fp.readline()
        if line == "":
            break

        words.append(line.rstrip())

    matches = scrabble(words, letters)
    print matches

