import nltk
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer(ignore_stopwords=False)

training_data = []

training_data.append({'class': 'reservation de salle de réunion', 'sentence': 'Je voudrais reserver une salle'})
training_data.append({'class': 'reservation de salle de réunion', 'sentence': "Serait t'il possible de reserver une salle pour aujourd'hui de 10h à 12h?"})
training_data.append({'class': 'reservation de salle de réunion', 'sentence': 'Reserve moi une salle'})
training_data.append({'class': 'reservation de salle de réunion', 'sentence': 'Reserve moi une salle de réunion de 16h à 17h'})
training_data.append({'class': 'reservation de salle de réunion', 'sentence': "Y'a t'il une salle de réunion libre entre 11h à 11h30"})
training_data.append({'class': 'reservation de salle de réunion', 'sentence': 'reserve une sale de reunion'})

training_data.append({'class': "reservation d'un billet de train", 'sentence': 'Je voudrais un billet de train'})
training_data.append({'class': "reservation d'un billet de train", 'sentence': 'Reserve moi un billet de train'})

training_data.append({'class': "salutation", 'sentence': 'Hello'})
training_data.append({'class': "salutation", 'sentence': 'Bonjour'})
training_data.append({'class': "salutation", 'sentence': 'Bonjour Chatbot'})

# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []



stopwords = ['de']



#print(class_words)

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in stopwords: #stopwords a implementer
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])
#print("______")
# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
#print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
#print ("Class words: %s" % class_words)


# calculate a score for a given class
def calculate_class_score(sentence, class_name, show_details=False):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with same weight
            score += 1

            if show_details:
                print("   match: %s" % stemmer.stem(word.lower()))
    return score



# we can now calculate a score for a new sentence
sentence = "Reserve moi un billet de train"

# now we can find the class with the highest score
#for c in class_words.keys():
#    print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))

# calculate a score for a given class taking into account word commonality
def calculate_class_score(sentence, class_name, show_details=False):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score



# return the class with highest score for sentence
def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score(sentence, c, show_details=True)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, high_score

value = ['un', 'une', 'plusieurs', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', '1', '2','3',"4",'5','6','7']

def extract_value(sentence):
    for word in nltk.word_tokenize(sentence):
        if word in value:
            return word
    return None

#print(classify('Reserve moi une salle de réunion'))
#print(extract_value('Reserve moi deux billet de train'))

print('__________')