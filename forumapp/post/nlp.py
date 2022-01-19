import re
import spacy
from profanity_filter import ProfanityFilter
from spellchecker import SpellChecker

#https://pypi.org/project/profanity-filter/

nlp = spacy.load('en_core_web_sm')


# Converts input for further nlp processing
def convert_text(text_input):
    profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse spacy Language (optional)
    text = spell_check(text_input)
    doc = nlp(text)
    return doc


# Checks for portion of offensive words
def check_profanity_portion(text):
    
    number_words = 0
    number_profane_words = 0

    for token in text:
        number_words += 1
        if token._.is_profane:
            number_profane_words += 1


    return (number_profane_words / number_words) > 0.15


# Checks and replaces spelling mistakes
def spell_check(text):
    
    tokens = re.split(' ',text)
    
    spell = SpellChecker()
    mistakes = spell.unknown(tokens)
    
    for index in range(len(tokens)):

        if tokens[index] in mistakes:
            tokens[index] = spell.correction(tokens[index])

    return ' '.join(tokens)


def check_and_censor(text_input):
    '''Check and replace offensive language.
    
    Keywords arguments:
    text -- corrected text_input
    clean_input -- cleaned text 
    
    '''
  
    # Spacy pipeline
    nlp = spacy.load('en_core_web_sm')
    profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse spacy Language (optional)
    nlp.add_pipe(profanity_filter.spacy_component, last=True)

    # Spellchecker and profanityfilter
    text = spell_check(text_input)
    clean_input = profanity_filter.censor(text)

    text = nlp(text)
    
    # If there is no offensive content at all, the input is returned
    if text._.is_profane == False:  
        return text_input
    if check_profanity_portion(text):
        return True
    else:
        return clean_input

