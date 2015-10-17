#!usr/bin/python
# encoding=utf-8
# coding=utf-8
import nltk.corpus
import nltk.tokenize
import nltk.stem
import nltk.tag
import string
import jieba
import cStringIO,codecs,csv
"""Output .cvs file for Machine Learning model training"""

# Get default English stopwords and extend with punctuation
stopwords = [u'／', u'，', u'。', u'、', u'；', u'：', u'？', u'「', u'」']
stopwords.extend(string.punctuation)


#List the feature that matched for each question.
def list_feature(question,features):
    #load special word for bank
    jieba.load_userdict('bankdict.txt')
    tokens_b = [token.strip(string.punctuation) for token in jieba.cut_for_search(question) if (token.strip(string.punctuation) not in stopwords)]
    #print (',').join(tokens_b)

    f = [0]*len(features)
    f_demo  = []
    for token in tokens_b:
        if token in features:
            f[features.index(token)]=1
            f_demo.append(token)
    print (',').join(f_demo),'for "',question,'"'
    #print f
    return f

# Output csv file
def output_csv():
    features = []
    with open('feature_chinese_fix.csv','r') as file:
        reader = UnicodeReader(file)
        for row in reader:
            for token in row:
                if token not in features:
                    features.append(token)
    #print features
    #print (',').join(features)
    feature1 = list(features)
    feature1.insert(0,'class')
    feature_final = []
    feature_final.append(feature1)
    output = []
    #output.append(feature1)

    with open('raw_question_chinese.csv', mode='r') as file:
        for row in csv.reader(file):
            question = row[1]
            f = list_feature(question,features)
            f.insert(0,row[0])
            output.append(f)
    file.close()
    with open('question_chinese.csv', mode='w') as file:
        w = UnicodeWriter(file)
        w.writerows(feature_final)
        w = csv.writer(file)
        w.writerows(output)
    file.close()

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
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
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

# Setting up the features for later matching.
def init():
    features = []
    #load special word for bank
    jieba.load_userdict('bankdict.txt')
    with open('raw_question_chinese.csv', mode='r') as file:
        for row in csv.reader(file):  
            question = row[1]
            #test = jieba.cut_for_search(question)
            #print(", ".join(test))
            tokens_a = [token.strip(string.punctuation) for token in jieba.cut_for_search(question) if (token.strip(string.punctuation) not in stopwords)]
            """
            for token in tokens_a:
                if token not in features:
                    features.append(token)
            """
            features.append(tokens_a)
    file.close()
    with open('feature_chinese.csv','w') as file:
        w = UnicodeWriter(file)
        w.writerows(features)
    file.close()
    #print (",".join(features))
    #print features
    #return features

def main():
    #init()
    output_csv()

if __name__ == '__main__':
    main()
