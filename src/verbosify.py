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

def _get_synonym(word, pos):
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
    return random.choice(synonyms)

def _get_whitelist_synonym(word, pos):
    synonyms = WHITELIST[word+'/'+pos]
    if isinstance(synonyms, list): return random.choice(synonyms + [word])
    else: return random.choice(WHITELIST[synonyms] + [word]) # reference to another entry
    
def _join_sentence(word_list):
    new_sentence = ''
    
    for word in word_list:
        if re.match(r"[^\w\s]", word): new_sentence += word
        else: new_sentence += ' ' + word.replace('_', ' ')
            
    return new_sentence[1:]

def _get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'): return 'as'
    elif treebank_tag.startswith('V'): return 'v'
    elif treebank_tag.startswith('N'): return 'n'
    elif treebank_tag.startswith('R'): return 'r'
    else: return ''

# -- main verbosify function -- #
def _verbosify(input_sentence):
    word_list = []

    # go through every word    
    for word, pos in pos_tag(re.findall(r"\w+|[^\w\s]", input_sentence)):
        # punctuation, whitelist, or normal word
        if re.match(r"[^\w\s]", word): word_list.append(word)
        elif word+'/'+pos in WHITELIST: word_list.append(_get_whitelist_synonym(word, pos))
        else: word_list.append(_get_synonym(word, _get_wordnet_pos(pos)))

    # return the sentence
    return _join_sentence(word_list)