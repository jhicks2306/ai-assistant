from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Initialize the WordNet Lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to lemmatize each word in a sentence
def lemmatize_sentence(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)
    # Lemmatize each word and join them back into a sentence
    lemmatized_sentence = ' '.join([lemmatizer.lemmatize(word.lower()) for word in words])
    return lemmatized_sentence