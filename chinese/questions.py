#!usr/bin/python
# encoding=utf-8
# coding=utf-8

"""Main Activity to answer question for user."""

import codecs
import csv
import cStringIO
import jieba
import string
import sys
import time
import os.path
from snownlp import SnowNLP
from svmutil import *
from nltk.metrics.distance import edit_distance

# Set stopwords and extend with punctuation
stopwords = [u')', u'(', u'／', u'，', u'。', u'、', u'；', u'：', u'？', u'「', u'」']
stopwords.extend(string.punctuation)
YES = ['y', 'ye', 'yes']
NO = ['n', 'no']

def correct(spell,features):
    """
    Calculate distance between two pinyin.
    It will lower the accuraty now, might be used it in the future.
    """
    for feature_pinyin in features:
        if edit_distance(spell, feature_pinyin) / float(len(feature_pinyin)) < 0.25:
            print '%s similiar to %s' % (spell, feature_pinyin)
            return True
    return False

def list_feature(question, init_value, m, DBG):
    """List the feature that matched for each question."""
    mydict,synonyms,synonyms_pinyin,features,features_pinyin = init_value
    start_time = time.time()
    # Cut question into tokens and strip stopwords.
    tokens_b = [token.strip(string.punctuation) for token in jieba.cut(question) if (token.strip(string.punctuation) not in stopwords)]
    tokens_c = []   #for spell check
    last_match = 0  #for spell check
    f = {}  # Record the features this question match.
    f_demo  = []
    for token in tokens_b:
        index = tokens_b.index(token)

        # Check for features
        if token in features:
            f[features.index(token)]=1
            f_demo.append(token)
            if index > last_match:
                # Add words not match into tokens_c for spell check.
                tokens_c.append(''.join(tokens_b[last_match:index]))
                #if DBG:    print ','.join(tokens_c)
            last_match=index+1
        else:
            # Check for synonyms
            for key, texts in synonyms.items():
                if key not in f and token in texts:
                    f[key]=1
                    f_demo.append(token)
                    if index > last_match:
                        tokens_c.append(''.join(tokens_b[last_match:index]))
                    last_match=index+1

        if index == len(tokens_b)-1 and token not in f_demo:
            tokens_c.append(''.join(tokens_b[last_match:index+1]))

    # Spell check.
    #print 'robin', (',').join(tokens_c)
    if tokens_c:
        for token in tokens_c:
            s = SnowNLP(SnowNLP(token).han).pinyin
            s_check=[]
            # Features length from 2~4
            # ex: 'abcde' => 'ab','abc','abcd','bc','bcd','bcde'...
            for i in range(1,4):
                s_check += ([('').join(s[j:j+i+1]) for j in range(len(s)-1) if j+i < len(s)])
            for spell in s_check:
                if spell in features_pinyin:
                    f[features_pinyin.index(spell)]=1
                    f_demo.append(features[features_pinyin.index(spell)])
                for key, texts in synonyms_pinyin.items():
                    if key not in f:
                        if spell in texts:
                            f[key]=1
                            f_demo.append(synonyms[key][0])

    p_label, p_acc, p_val = svm_predict([0], [f], m, '-b 1 -q')

    if DBG:
        print f
        print 'Matched :',(',').join(f_demo)

        elapsed_time = time.time() - start_time
        print 'Execution time : %.3f' % (elapsed_time)
        for i in range(len(p_val[0])):
            if p_val[0][i] > 0.025:
                print i+1, mydict[i+1], p_val[0][i]

        print '='*70
        print 'You are asking :', mydict[p_label[0]]
        print '='*70

        # Check matching result for improving.
        match = raw_input("Does this question match?(y/n) ")
        result = []
        result.append([str(int(p_label[0])),question.decode('utf-8')])
        #print result
        if match.lower() in YES:
            with open('result_right.csv','a') as file:
                w = UnicodeWriter(file)
                w.writerows(result)

        #TODO Dealt with wrong guess.
    return mydict[p_label[0]]

def get_model():
    """Load Machine Learning model if exist, create one if not."""
    if not os.path.exists('question_chinese.model'):
        y, x = svm_read_problem('question_chinese1')
        m = svm_train(y, x, '-c 32.0 -g 0.0078125 -b 1')
        svm_save_model('question_chinese.model', m)
        return m
    else:
        m = svm_load_model('question_chinese.model')
        #y, x = svm_read_problem('question_chinese1')
        #print y,x
        #p_label, p_acc, p_val = svm_predict(y, x, m)
        #print p_label,p_acc
        return m

def init():
    """Set up the features for later matching."""
    # Load dictionary for banking.
    jieba.load_userdict('bankdict.txt')

    # Read the question database.
    mydict = {}
    with open('raw_question_chinese.csv') as file:
        reader = UnicodeReader(file)
        mydict = {float(rows[0]):rows[1] for rows in reader}

    # Read the synonyms database.
    synonyms = {}
    with open('synonyms.csv') as file:
        reader = UnicodeReader(file)
        synonyms = {int(float(rows[0]))+1 : rows[1:] for rows in reader}

    # Load indexes which we use to classify questions.
    features = []
    with open('question_chinese.csv') as file:
        reader = UnicodeReader(file)
        for row in reader:
            features = row[:]
            break

    # Process feature by NLP to know how to spell it.
    # And use it for spell check later.
    features_pinyin = [''.join(SnowNLP(SnowNLP(feature).han).pinyin) for feature in features]

    synonyms_pinyin = {}
    for key, texts in synonyms.items():
        synonyms_pinyin[key] = [''.join(SnowNLP(SnowNLP(text).han).pinyin) for text in texts]

    return mydict, synonyms, synonyms_pinyin, features, features_pinyin

def main():
    #mydict,synonyms,synonyms_pinyin,features,features_pinyin = init()
    init_value = init()
    mydict = init_value[0]
    m = get_model()

    # Make a predicition to check system status OK.
    list_feature(mydict[20],init_value,m,False)

    # Start answering questions.
    while True:
        question = raw_input("\nAsk me a question : ")
        if question == 'exit':
            break
        list_feature(question.replace(' ',''),init_value,m,True)

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        """next() -> unicode
        This function reads and returns the next line as a Unicode string.
        """
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        """writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        """
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__ == '__main__':
    main()
