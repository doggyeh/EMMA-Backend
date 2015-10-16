import nltk.corpus
import nltk.tokenize
import nltk.stem
import nltk.tag
import string
import csv

"""Output .cvs file for Machine Learning model training"""

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)

# Create tokenizer and stemmer
tokenizer = nltk.tokenize.TreebankWordTokenizer()
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

# List the feature that matched for each question.
def list_feature(question,features):
    pos_b = nltk.pos_tag(tokenizer.tokenize(question))
    tokens_b = [token.lower().strip(string.punctuation) for token, pos in pos_b if (token.lower().strip(string.punctuation) not in stopwords)]
    stems_b = [lemmatizer.lemmatize(token) for token in tokens_b if len(token) > 0]

    f = [0]*len(features)
    f_demo  = []
    for stem in stems_b:
        if stem in features:
            f[features.index(stem)]=1
            f_demo.append(stem)
    print f_demo,'for "',question,'"'
    #print f
    return f

# Output csv file
def output_csv(features):
    feature1 = list(features)
    feature1.insert(0,'class')
    output = []
    output.append(feature1)

    with open('raw_question.csv', mode='r') as file:
        for row in csv.reader(file):
            question = row[1]
            f = list_feature(question,features)
            f.insert(0,row[0])
            output.append(f)
    file.close()

    with open('question.csv', mode='w') as file:
        w = csv.writer(file)
        w.writerows(output)
    file.close()

# Setting up the features for later matching.
def init():
    features = []
    with open('raw_question.csv', mode='r') as file:
        for row in csv.reader(file):  
            question = row[1]
            pos_a = nltk.pos_tag(tokenizer.tokenize(question))
            tokens_a = [token.lower().strip(string.punctuation) for token, pos in pos_a if (token.lower().strip(string.punctuation) not in stopwords)]
            stems_a = [lemmatizer.lemmatize(token) for token in tokens_a if len(token) > 0]
            for stem in stems_a:
                if stem not in features:
                    features.append(stem)
    file.close()
    print '\nfeatures are',features
    return features

def main():
    features = init()
    output_csv(features)

if __name__ == '__main__':
    main()
