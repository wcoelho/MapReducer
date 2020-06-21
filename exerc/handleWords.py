import unicodedata

def fixAccents(text):
    # fix accents
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)

def removePonctuation(text):
    punctuations = '''!()[]{};:'",<>.?\@#$%^&*~`'''
    no_punct = ""
    # remove ponctuations
    for char in text:
        if char not in punctuations:
            no_punct = no_punct + char
    return no_punct