EXAMPLE_WORDLIST = ['azotised', 'bawdiest', 'dystocia',
                    'geotaxis', 'iceboats', 'oxidates',
                    'oxyacids', 'sweatbox', 'tideways']
EXAMPLE_LETTERS = ['w', 'g', 'd', 'a', 's', 'x', 'z', 'c', 
                   'y', 't', 'e', 'i', 'o', 'b']


from sets import Set

def scrabble(wordlist, letters):
    result = []
    letterSet = Set(letters)    

    for word in wordlist:
        wordSet = Set(word)
        if wordSet & letterSet == wordSet:
            result.append(word)

    return result

if __name__ == "__main__":
    print scrabble(EXAMPLE_WORDLIST, EXAMPLE_LETTERS)




