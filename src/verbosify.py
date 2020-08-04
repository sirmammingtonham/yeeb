import random
import re
from nltk.corpus import wordnet
from nltk import pos_tag

# -- Helper functions for verbosify -- #
WHITELIST = {'a/DT': ['an', 'the'],
                'an/DT': ['a', 'the'],
                'the/DT': ['a', 'an'],
                'I/PRP': ['ur boy', 'me, myself and I', 'yours truly'],
                'me/PRP': 'I/PRP',
                'you/PRP': ['thou', 'thoust'],
                'will/MD': ['shall', 'shalt']}

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

def get_whitelist_synonym(word, pos):
    synonyms = WHITELIST[word+'/'+pos]
    if isinstance(synonyms, list): return random.choice(synonyms + [word])
    else: return random.choice(WHITELIST[synonyms] + [word]) # reference to another entry

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
    for word, pos in pos_tag([v for v in re.split('(\W)', input_sentence) if v != '']):
        # punctuation/whitespace, the word 'I', whitelist, or normal word
        if re.match(r'[^\w]', word): new_sentence += word
        elif word.upper() == 'I': new_sentence += get_whitelist_synonym('I', 'PRP')
        elif word+'/'+pos in WHITELIST: new_sentence += get_whitelist_synonym(word, pos)
        else: new_sentence += get_synonym(word, get_wordnet_pos(pos))

    # return the sentence
    return new_sentence