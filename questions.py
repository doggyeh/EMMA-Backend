import nltk.corpus
import nltk.tokenize
import nltk.stem
import nltk.tag
import string
import time
import csv
from predict import init_api,make_prediction

"""Main Activity to answer question for user"""
# TODO:improve the Machine Learning Model by user feedback.

mydict = {} #question database
sample_question = "How do I apply for a Citi Credit Card?"

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)

# Create tokenizer and stemmer
tokenizer = nltk.tokenize.TreebankWordTokenizer()
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

# List the feature that matched for each question.
def list_feature(question,features,api,mydict,DBG):
    start_time = time.time()
    pos_b = nltk.pos_tag(tokenizer.tokenize(question))
    tokens_b = [token.lower().strip(string.punctuation) for token, pos in pos_b if (token.lower().strip(string.punctuation) not in stopwords)]
    stems_b = [lemmatizer.lemmatize(token) for token in tokens_b if len(token) > 0]

    f = [0]*len(features)
    #f_demo  = []
    for stem in stems_b:
        if stem in features:
            f[features.index(stem)]=1
            #f_demo.append(stem)
    #print f_demo,'for "',question,'"'
    #print f
    elapsed_time = time.time() - start_time
    if DBG:
        print 'Execution local time : %.3f' % (elapsed_time)

    label = make_prediction(api,f)
    if DBG:
        print 'You are asking :',mydict[label]
    elapsed_time = time.time() - start_time
    if DBG:
        print 'Execution total time : %.3f' % (elapsed_time)
    #return f

# Setting up the features for later matching.
def init():
    features = []
    with open('question.csv', mode='r') as file:
        for row in csv.reader(file):  
            features = row[1:]
            break
    file.close()
    #print '\nfeatures are',features
    return features

def main():
    features = init()
    api = init_api()
    #Read the question database
    with open('raw_question.csv', mode='r') as file:
        reader = csv.reader(file)
        mydict = {rows[0]:rows[1] for rows in reader}
    file.close()
    print mydict
    #Make a predicition in initial stage so the later predicitions will be faster by 10x
    list_feature(sample_question,features,api,mydict,False)

    #Start answering question
    while True:
        question = raw_input("\nAsk me a question : ")
        list_feature(question,features,api,mydict,True)

if __name__ == '__main__':
    main()
