#!usr/bin/python
# encoding=utf-8
# coding=utf-8
import nltk.corpus
import nltk.tokenize
import nltk.stem
import nltk.tag
import string
import time
import csv,cStringIO,codecs
import jieba
from predict import init_api,make_prediction
from snownlp import SnowNLP

"""Main Activity to answer question for user"""
# TODO:improve the Machine Learning Model by user feedback.

# Get default English stopwords and extend with punctuation
stopwords = [u')', u'(', u'／', u'，', u'。', u'、', u'；', u'：', u'？', u'「', u'」']
stopwords.extend(string.punctuation)
YES = ['y','ye','yes']
NO = ['n','no']
WORD = ['掉了','弄丟']

# List the feature that matched for each question.
def list_feature(question,features,features_pinyin,api,mydict,synonyms,synonyms_pinyin,DBG):
    start_time = time.time()
    tokens_b = [token.strip(string.punctuation) for token in jieba.cut(question) if (token.strip(string.punctuation) not in stopwords)]
    print ','.join(tokens_b)
    tokens_c = [] #for spell check
    last_match = 0 #for spell check

    f = [0]*len(features)
    f_demo  = []
    for token in tokens_b:
        print '',token
        index = tokens_b.index(token)

        if token in features:
            f[features.index(token)]=1
            f_demo.append(token)
            print '',index,last_match
            if index > last_match:
                tokens_c.append(''.join(tokens_b[last_match:index]))
                last_match=index+1

        #Start check for synonyms
        for key, texts in synonyms.items():
        #for token in tokens_b:
            if f[key] == 0:
                if token in texts:
                    f[key]=1
                    f_demo.append(token)
                    print '',index,last_match
                    if index > last_match:
                        tokens_c.append(''.join(tokens_b[last_match:index]))
                        last_match=index+1

        if index == len(tokens_b)-1 and token not in f_demo:
            tokens_c.append(''.join(tokens_b[last_match:index+1]))

    #Doing spell check.
    print 'robin',(',').join(tokens_c)
    for token in tokens_c:
        s = SnowNLP(SnowNLP(token).han).pinyin
        print s
        s_check=[]
        #features length from 2~4
        for i in range(1,4):
            s_check+=([('').join(s[j:j+i+1]) for j in range(len(s)-1) if j+i < len(s)])
        print s_check
        for spell in s_check:
            if spell in features_pinyin:
                f[features_pinyin.index(spell)]=1
                f_demo.append(features[features_pinyin.index(spell)])
            for key, texts in synonyms_pinyin.items():
                if f[key] == 0:
                    if spell in texts:
                        f[key]=1
                        f_demo.append(synonyms[key][0])

    #print f_demo,'for "',question,'"'
    #if DBG:
    #    print f
    if DBG:
        #print 'Matched :',(',').join(tokens_b)
        print 'Matched :',(',').join(f_demo)
    #    elapsed_time = time.time() - start_time
    #    print 'Execution local time : %.3f' % (elapsed_time)
"""
    label,stats = make_prediction(api,f)
    if DBG:
        elapsed_time = time.time() - start_time
        #print 'Execution total time : %.3f' % (elapsed_time)

        if label not in mydict:
            print "Sorry, I don't understand your question."
        else:
            print '='*80
            print 'You are asking :',mydict[label]
            print '='*80
            for stat in stats:
                if float(stat['score']) > 0.1 and float(stat['score'])<1:
                    print mydict[stat['label']],'score :',stat['score']

        #Check matching result.
        match = raw_input("Does this question match?(y/n) ")
        result = []
        result.append([label,question.decode('utf-8')])
        #print result
        if match.lower()in YES:
            with open('result_right.csv','a') as file:
                w = UnicodeWriter(file)
                w.writerows(result)
        #TODO dealt with wrong guess
    #return f
"""
# Setting up the features for later matching.
def init():

    #Read the question database
    mydict = {}
    with open('raw_question_chinese.csv', mode='r') as file:
        #reader = csv.reader(file)
        reader = UnicodeReader(file)
        mydict = {rows[0]:rows[1] for rows in reader}
    file.close()

    #Read the question database
    synonyms = {}
    with open('synonyms.csv', mode='r') as file:
        reader = UnicodeReader(file)
        synonyms = {int(float(rows[0])):rows[1:] for rows in reader}
    file.close()

    features = []
    with open('question_chinese.csv', mode='r') as file:
        reader = UnicodeReader(file)
        for row in reader:
            features = row[1:]
            break
    file.close()
    #print '\nfeatures are',features

    features_pinyin = []
    for feature in features:
        #Translate feature into Simple Chinese then get how to spell it.
        s = ''.join(SnowNLP(SnowNLP(feature).han).pinyin)
        print feature,s
        features_pinyin.append(s)

    synonyms_pinyin={}
    for key, texts in synonyms.items():
        synonyms_pinyin[key] = [''.join(SnowNLP(SnowNLP(text).han).pinyin) for text in texts]

    return mydict,synonyms,synonyms_pinyin,features,features_pinyin

def main():
    jieba.load_userdict('bankdict.txt')
    for word in WORD:
        jieba.add_word(word)
    mydict,synonyms,synonyms_pinyin,features,features_pinyin = init()
    api = init_api()

    #print mydict
    print ("\n").join(mydict.values())
    #print synonyms
    #for list in synonyms.values():
    #    print (",").join(list)

    #Make a predicition in initial stage so the later predicitions will be faster by 10x
    list_feature(mydict['20'],features,features_pinyin,api,mydict,synonyms,synonyms_pinyin,False)
    #for q in mydict.values():
    #    list_feature(q,features,api,mydict,synonyms,False)

    #Start answering question
    while True:
        question = raw_input("\nAsk me a question : ")
        if question == 'exit':
            break
        list_feature(question.replace(' ',''),features,features_pinyin,api,mydict,synonyms,synonyms_pinyin,True)

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

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
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
