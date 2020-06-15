import mincemeat
import glob
import csv
import json

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
            author = author.replace("\"","'")
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

results = s.run_server(password="changeme")

with open('.//result3.json', 'w') as f:
    totalItems = len(results.keys())
    counter = 1
    # Write in file with json format
    f.write("[")
    for author, item in results.items():
        separator=','
        # If last item, avoid adding ','
        if counter==totalItems:
            separator=''
        counter+=1
        f.write('{"author": "%s", "items": %s}%s\n' % (author, json.dumps(item), separator))
    f.write("]")

print("File saved successfully")

