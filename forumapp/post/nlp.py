from profanity_filter import ProfanityFilter
import spacy

#https://pypi.org/project/profanity-filter/

nlp = spacy.load('en_core_web_sm')

def convert_text(input):
    profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse spacy Language (optional)
    #ProfanityFilter.extra_profane_word_dictionaries = {'en': {'food', 'orange'}}
    #nlp = spacy.load('en_core_web_sm')
    doc = nlp(input)
    return doc




# Hier wird der Anteil an anstößigen Wörtern geprüft und zurückgegeben
def check_profanity_portion(text):
    
    number_words = 0
    number_profane_words = 0

    for token in text:
        number_words += 1
        if token._.is_profane:
            number_profane_words += 1


    print((number_profane_words / number_words))
    return (number_profane_words / number_words) > 0.15



# Nur diese Methode wird außerhalb aufgerufen und greift aus die anderen in dieser Datei zu
def check_and_censor(input):

  
    # Spacy und profanity filter
    nlp = spacy.load('en_core_web_sm')
    profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse spacy Language (optional)
    nlp.add_pipe(profanity_filter.spacy_component, last=True)

    clean_input = profanity_filter.censor(input)

    text = nlp(input)
    


    if text._.is_profane == False:
        
        print("no sensitive text")
        return input

    if check_profanity_portion(text):

        print("too sensitive")
        return True

    else:
        profanity_filter.custom_profane_word_dictionaries = {'en': {'food', 'tasteful'}}
        print("geringer anteil")
        #clean_input = profanity_filter.censor(input)
        return clean_input


input = 'We need better food in the cafeteria. The food right now is too expensive and rarely tasteful. Shit Fuck'

print(check_and_censor(input))