from profanity_filter import ProfanityFilter
import spacy
from spellchecker import SpellChecker
import re

#https://pypi.org/project/profanity-filter/

nlp = spacy.load('en_core_web_sm')


# wird gerade nicht benutzt
def convert_text(text_input):
    profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse spacy Language (optional)
    #ProfanityFilter.extra_profane_word_dictionaries = {'en': {'food', 'orange'}}
    #nlp = spacy.load('en_core_web_sm')

    text = spell_check(text_input)

    
    doc = nlp(text)
    return doc



# Hier wird der Anteil an anstößigen Wörtern geprüft und zurückgegeben
def check_profanity_portion(text):
    
    number_words = 0
    number_profane_words = 0

    # Hier werden die Wörter zuerst korrigiert 

    for token in text:
        number_words += 1
        if token._.is_profane:
            number_profane_words += 1


    #print((number_profane_words / number_words))
    return (number_profane_words / number_words) > 0.15


def spell_check(text):
    

    tokens = re.split(' ',text)
    
    spell = SpellChecker()
    mistakes = spell.unknown(tokens)
    
    for index in range(len(tokens)):

        if tokens[index] in mistakes:
            tokens[index] = spell.correction(tokens[index])

    return ' '.join(tokens)


# Nur diese Methode wird außerhalb aufgerufen und greift aus die anderen in dieser Datei zu
def check_and_censor(text_input):

  
    # Spacy und profanity filter
    nlp = spacy.load('en_core_web_sm')
    profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse spacy Language (optional)
    nlp.add_pipe(profanity_filter.spacy_component, last=True)

    text = spell_check(text_input)

    clean_input = profanity_filter.censor(text)

    text = nlp(text)
    

    if text._.is_profane == False:  
        return text_input

    if check_profanity_portion(text):
        return True

    else:
        #profanity_filter.custom_profane_word_dictionaries = {'en': {'food', 'tasteful'}}
        #clean_input = profanity_filter.censor(text)
        return clean_input


