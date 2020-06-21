import mincemeat
import glob
import csv
import json

resultFile = '.\\result3.json'
responseFile = '.\\response3.txt'
text_files = glob.glob('.\\Trab2.3\\*')

def file_contents(file_name):
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

source = dict((file_name, file_contents(file_name)) for file_name in text_files)

def mapfn(k, v):
    from stopwords import allStopWords
    from handleWords import removePonctuation
    from handleWords import fixAccents
    for line in v.splitlines():     
        parts = line.split(':::')
        authors = parts[1].split('::')
        for author in authors:
            # Converting to UTF-8
            author = fixAccents(author)
            # Avoiding quotes in author name
            author = author.replace('"','\'')
            for word in parts[2].split():
                # Checking if not in stop words list
                if word.lower() not in allStopWords:
                    # Remove ponctuation
                    word = removePonctuation(word)
                    yield author,word.lower()


def reducefn(k, v):
    # Dictionary with list of words and total of each one  
    wordsList = {}
    for index, item in enumerate(v):
        total = 0
        if item in wordsList:     
            total = int(wordsList[item]) + 1
        else:
            total = 1
        wordsList[item] = total    
    return wordsList

s = mincemeat.Server()

s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password='changeme')

data = {}
data['authors'] = []

# Prepare Json object
items = {}
items['authors'] = []
for author, words in results.items():
    subitems = {}
    subitems['words'] = []
    for word, counter in words.items():
        subitems['words'].append({'counter': counter, 'word': word})    
    items['authors'].append({'name': author, 'words': subitems['words']})

# Write json to file
with open(resultFile, 'w') as f:
    print('Writing to file ' + resultFile + '...')
    json.dump(items, f, indent = 4)
print("File saved successfully!")
print("--------------------------------")

# Read result file and show specific values
print('Searching specific authors and words with biggest counter...')
print("--------------------------------")
with open(responseFile, 'w') as f:
    with open(resultFile) as jsonFile:
        jdata = json.load(jsonFile)
        for c in jdata['authors']:
            if(c['name'] in {'Grzegorz Rozenberg', 'Philip S. Yu'}):                
                # Getting biggest counter
                firstPlace = max(c['words'], key=lambda wd: wd['counter'])
                firstWords=[]
                firstCounter=firstPlace['counter']
                # Getting words with biggest counter
                for w in c['words']:
                    if w['counter'] == firstCounter:
                        firstWords.append(w['word'])
                        # Setting counter=0 to be ignored in second place list
                        w['counter'] = 0
                # Getting words with second biggest counter
                secondPlace = max(c['words'], key=lambda wd: wd['counter'])
                secondWords=[]
                secondCounter=secondPlace['counter']
                #nGetting words with second biggest counter
                for w in c['words']:
                    if w['counter'] == secondCounter:
                        secondWords.append(w['word'])
                # Writing exercice response
                print('Writing response for ' + c['name'] + ' to file...')
                print("--------------------------------")
                f.write('--------------------------------\n')
                f.write('Author: ' + c['name'] + ':\n')
                f.write('- Word(s) in first place: ')
                f.write(', '.join(firstWords))
                f.write(' => counter: ' + str(firstCounter) + '\n')
                f.write('- Word(s) in second place: ')
                f.write(', '.join(secondWords))
                f.write(' => counter: ' + str(secondCounter) + '\n')
print("--------------------------------")
print("Whole process executed sucessfully!")