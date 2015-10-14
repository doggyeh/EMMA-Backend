import nltk.corpus
import nltk.tokenize
import nltk.stem
import nltk.tag
import string

target_question = [
                    "How do I apply for a Citi Credit Card?",
                    "How long does the application process take?",
                    "How do I check the status of my application?",
                    "How do I save my application so I can return to it later?",
                    "If I save an application, how long will the application be held for?",
                    "What can I do if I delete or misplace the email I received containing my Application Reference Number?",
                    "How do I retrieve my saved application?",
                    "What is the document upload function?",
                    "Why do you need my documents?",
                    "How do I upload my documents?",
                    "What documents do I need to provide?",
                    "What can I do if I don't have the correct documentation?",
                    "What is maximum file size that I can upload?",
                    "Will I receive notification if any documents are missing?",
                    "What should I do if I have misplaced my Application Reference Number?",
                    "When are the annual fees and additional fees charged?",
                    "How does the interest-free period work?",
                    "If I upgrade my Citibank Rewards Credit Card, will my Rewards points be carried over?",
                   ]

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)

# Create tokenizer and stemmer
tokenizer = nltk.tokenize.TreebankWordTokenizer()
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

# List the feature that matched for each question.
def list_feature(question,features):
    pos_b = nltk.pos_tag(tokenizer.tokenize(question))
    tokens_b = [token.lower().strip(string.punctuation) for token, pos in pos_b if pos.startswith('N') and (token.lower().strip(string.punctuation) not in stopwords)]
    stems_b = [lemmatizer.lemmatize(token) for token in tokens_b if len(token) > 0]

    f = [0]*len(features)
    f_demo  = []
    for i in range(len(features)):
        if features[i] in stems_b:
            f[i]=1
            f_demo.append(features[i])
    print f_demo,'for',question
    # TODO: Send the features mapping result (f) to Google Predict API.

# Setting up the features all we got for later matching.
def init(questions):
    features = []
    for question in questions:
        pos_a = nltk.pos_tag(tokenizer.tokenize(question))
        tokens_a = [token.lower().strip(string.punctuation) for token, pos in pos_a if pos.startswith('N') and (token.lower().strip(string.punctuation) not in stopwords)]
        stems_a = [lemmatizer.lemmatize(token) for token in tokens_a if len(token) > 0]
        for stem in stems_a:
            features.append(stem)
    print 'features are',feautres
    return features

def main():
    print "target question =",target_question
    features = init(target_question)
    while True:
        question = raw_input("Ask me a question : ")
        list_feature(question,features)


if __name__ == '__main__':
    main()
"""
def get_wordnet_pos(pos_tag):
	if pos_tag[1].startswith('J'):
		return (pos_tag[0], wordnet.ADJ)
	elif pos_tag[1].startswith('V'):
		return (pos_tag[0], wordnet.VERB)
	elif pos_tag[1].startswith('N'):
		return (pos_tag[0], wordnet.NOUN)
	elif pos_tag[1].startswith('R'):
		return (pos_tag[0], wordnet.ADV)
	else:
		return (pos_tag[0], wordnet.NOUN)
"""
