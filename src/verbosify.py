import random
import re
import time
from nltk.corpus import wordnet
from nltk import pos_tag

import requests
from bs4 import BeautifulSoup

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


# get spot to break up message
def get_breakpoint(msg):
    i = 2000
    while i > 0 and msg[i] != ' ': i -= 1
    
    return 2000 if i == 0 else i

# util function for better isdigit
def isdigit(s):
    return s.isdigit() or s[1:].isdigit()

# util function for correct case (title, upper, lower)
def case_correction(word, syn):
    if word == 'I': return syn

    if word.istitle(): return syn.title()
    elif word.isupper(): return syn.upper()
    else: return syn.lower()


# -- verbosify core function -- #
def verbosify(input_sentence):
    new_sentence = ''

    # go through every word
    for word, pos in pos_tag(get_word_list(input_sentence)):
        # punctuation/whitespace/possessive, whitelist, whitelist misspellings, normal word
        if re.match(r'[^\w]', word) or word == "'s": to_add = word
        elif any([word in s for s in WHITELIST]): to_add = get_whitelist_synonym(word)
        elif word in MISSPELLINGS: to_add = get_whitelist_synonym(MISSPELLINGS[word])
        else: to_add = get_synonym(word, get_wordnet_pos(pos))

        new_sentence += case_correction(word, to_add)

    # return the sentence
    return new_sentence


# -- verbosify repetition -- #
async def verbosify_ception(ctx, input_sentence, num_times):
    # get previous message if applicable
    if input_sentence == 'that':
        msg_history = await ctx.channel.history(limit=2).flatten()
        input_sentence = msg_history[1].content
        print('previous sentence:', input_sentence)

    # edge cases
    if num_times == 0:
        await ctx.send(input_sentence)
        return
    elif num_times == 1:
        await ctx.send(verbosify(input_sentence))
        return

    # Run verbosify num_times number of times
    to_print = [round(num_times*(i/5)) for i in range(1,5)] # when to print progress
    max_char_count = False

    verbosified = verbosify(input_sentence)
    msg = await ctx.send('`[1]` ' + verbosified)
    
    for i in range(2, num_times):
        if len(verbosified) > 10000: break  # would go past 10 messages...
        new_verbosified = verbosify(verbosified)
        
        if len(new_verbosified) > 1990 and not max_char_count:
            time.sleep(1)
            await msg.edit(content='`[...]` ' + verbosified)
            max_char_count = True
        else:
            verbosified = new_verbosified

            if i in to_print and len(verbosified) < 1990:
                time.sleep(1)
                await msg.edit(content='`[{}]` {}'.format(i, verbosified))

    # Final output
    time.sleep(1)
    verbosified = verbosify(verbosified) # one last time
    
    if len(verbosified) <= 2000: await msg.edit(content=verbosified)
    else:
        first_output = True

        # keep looping until message is under 2000
        while len(verbosified) > 2000:
            bp = get_breakpoint(verbosified)

            if first_output:
                await msg.edit(content=verbosified[:bp])
                first_output = False
            else: await ctx.send(verbosified[:bp], delete_after=30)
            
            verbosified = verbosified[bp+1:]

        # send last message
        await ctx.send(verbosified, delete_after=30)




# -- START DEFINE -- #
def get_ud_data(word):
    r = requests.get("http://www.urbandictionary.com/define.php?term={}".format(word.replace('_', '%20')))
    soup = BeautifulSoup(r.content, "html.parser")

    if not soup.find("div",attrs={"class":"meaning"}): return [None,None]
    return (soup.find("div",attrs={"class":"meaning"}).text, [soup.find("div",attrs={"class":"example"}).text])

def get_nltk_data(word):
    syns = wordnet.synsets(word.replace(' ', '_'))
    if len(syns): return (syns[0].definition(), syns[0].examples())
    else: return [None,None]

# format output for bruh define
def fdefine(word, meaning, examples):
    if meaning is None: return fdefine('bruh', *get_ud_data('bruh'))

    output = '`' + word + ': ' + meaning + '`\n'
    if len(examples): output += '>>> _' + examples[0] + '_'

    return output.replace('&apos;', "'")

# main bruh define function
async def get_definition(ctx, args):
    word = ' '.join(args).lower()

    # use nltk if specified
    if args[0] is 'normal': return await ctx.send(fdefine(word, *get_nltk_data(word)))
    
    # use urban dictionary otherwise
    else: return await ctx.send(fdefine(word, *get_ud_data(word)))
