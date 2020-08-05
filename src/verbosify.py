import random
import re
from nltk.corpus import wordnet
from nltk import pos_tag

# -- Helper functions for verbosify -- #
MISSPELLINGS = {'im': "I'm", "i'm": "I'm", 'Im': "I'm", 'i': 'I'}
WHITELIST = [['a', 'an', 'the'],
             ['I', 'me', 'ur boy', 'me, myself and I', 'yours truly'],
             ['you', 'thou', 'thoust'],
             ['will', 'shall', 'shalt'],
             ["I'm", 'I am', 'ur boy is'],
             ["can't", 'cannot', 'unable', 'shant'],
             ["shouldn't", 'shant', "shalln't"],
             ["you're", 'you are']]

def get_word_list(input_sentence):
    l = []
    temp = [v for v in re.split('(\W)', input_sentence) if v != '']
    
    i = 0
    while i < len(temp):
        if temp[i] in ["'", '’'] and i > 0 and i < len(temp)-1:
            # check possessive
            if temp[i+1] == 's': l.append("'s")
            # check contraction
            elif temp[i-1] != ' ' and temp[i+1] != ' ': l[-1] += "'" + temp[i+1]
            
            i += 2
        else:
            l.append(temp[i])
            i += 1
    
    return l
            

def get_synonym(word, pos):
    synsets = wordnet.synsets(word)
    synonyms = []

    # loop through all synsets
    for synset in synsets:
        # don't check synset if wrong part of speech
        if synset.name().split('.')[1] not in pos: continue

        # loop through each synonym
        for synonym in synset.lemmas():
            synonym = synonym.name()
            if synonym != word and synonym not in synonyms: synonyms.append(synonym)
    
    # no unique synonyms?
    if not synsets or not synonyms: return word
    # otherwise, choose random synonym
    return random.choice(synonyms).replace('_', ' ')

def get_whitelist_synonym(word):
    # get the correct set
    for synonyms in WHITELIST:
        if word in synonyms: break

    return random.choice(synonyms) # return random synonym

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'): return 'as'
    elif treebank_tag.startswith('V'): return 'v'
    elif treebank_tag.startswith('N'): return 'n'
    elif treebank_tag.startswith('R'): return 'r'
    else: return ''


# -- main verbosify function -- #
def verbosify(input_sentence):
    new_sentence = ''

    # go through every word
    for word, pos in pos_tag(get_word_list(input_sentence)):
        # punctuation/whitespace/possessive, whitelist, whitelist misspellings, normal word
        if re.match(r'[^\w]', word) or word == "'s": new_sentence += word
        elif any([word in s for s in WHITELIST]): new_sentence += get_whitelist_synonym(word)
        elif word in MISSPELLINGS: new_sentence += get_whitelist_synonym(MISSPELLINGS[word])
        else: new_sentence += get_synonym(word, get_wordnet_pos(pos))

    # return the sentence
    return new_sentence