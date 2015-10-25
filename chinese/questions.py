#!usr/bin/python
# encoding=utf-8
# coding=utf-8
import nltk.corpus
import nltk.tokenize
import nltk.stem
import nltk.tag
import string
import csv,cStringIO,codecs
import jieba
from svmutil import *
import os.path

"""Main Activity to answer question for user"""
# TODO:improve the Machine Learning Model by user feedback.

mydict = {} #question database

stopwords = [u'／', u'，', u'。', u'、', u'；', u'：', u'？', u'「', u'」']
stopwords.extend(string.punctuation)

# List the feature that matched for each question.
def list_feature(question,features,m,mydict,DBG):
    jieba.load_userdict('bankdict.txt')
    tokens_b = [token.strip(string.punctuation) for token in jieba.cut_for_search(question) if (token.strip(string.punctuation) not in stopwords)]
    f = {}
    #f_demo  = []
    for token in tokens_b:
        if token in features:
            f[features.index(token)+1]=1
            #f_demo.append(token)
    #print f_demo,'for "',question,'"'
    print f
    if DBG:
        print 'Matched :',(',').join(tokens_b)

    #x0, max_idx = gen_svm_nodearray({1:1, 3:1})
    #x0, max_idx = gen_svm_nodearray(f)
    y, x = [0], [{4:1, 26:1, 27:1}]
    p_label, p_acc, p_val = svm_predict(y,x,m)
    if p_label not in mydict:
        print "Sorry, I don't understand your question."
    else:
        if DBG:
            print 'You are asking :',mydict[p_label]
    #return f

#Get libsvm model.
def get_model():
    if not os.path.exists('question_chinese.model'):
        y, x = svm_read_problem('question_chinese1')
        m = svm_train(y, x, '-c 512.0 -g 0.0078125')
        #svm_save_model('question_chinese.model', m)
        return m
    else:
        m = svm_load_model('question_chinese.model')
        y, x = svm_read_problem('question_chinese')
        print y,x
        p_label, p_acc, p_val = svm_predict(y, x, m)
        print p_label,p_acc
        return m

# Setting up the features for later matching.
def init():
    features = []
    with open('question_chinese.csv', mode='r') as file:
        reader = UnicodeReader(file)
        for row in reader:
            features = row[1:]
            break
    file.close()
    #print '\nfeatures are',features
    return features

def main():
    features = init()
    m=get_model()
    #Read the question database
    with open('raw_question_chinese.csv', mode='r') as file:
        reader = csv.reader(file)
        mydict = {float(rows[0]):rows[1] for rows in reader}
    file.close()
    #print mydict
    print ("\n").join(mydict.values())

    list_feature(mydict[20],features,m,mydict,False)
    #Start answering question
    #while True:
    #    question = raw_input("\nAsk me a question : ")
    #    list_feature(question.replace(' ',''),features,m,mydict,True)

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
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

if __name__ == '__main__':
    main()
