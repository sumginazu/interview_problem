from os import listdir
from os.path import isfile, join
import operator as op
import nGramSearch as ng
import Sample as sample
import random as r


BOOK_DIRECTORY = "test_books/"
N = 3 #ngram length
NUM_NGRAM_SAMPLES = 30 #number of ngram search iterations
MISS_THRESHOLD = 0.9 #track percent of ngrams not found in corpus

TEST_ITERS = 10 #samples per book

def testSample(s):
    #s is a noisy/incomplete sample from a book
    #returns the most likely book id

    s_tokens = s.split()

    potential_books = {}
    miss_ratio = 0
    for i in xrange(NUM_NGRAM_SAMPLES):
        #pick a random ngram
        idx = r.randint(0, len(s_tokens)-N-1)
        ngram = s_tokens[idx:idx+N]
        #tally up which books match
        matches = ng.matchNGram(ngram)
        if len(matches) == 0:
            miss_ratio += 1.0/NUM_NGRAM_SAMPLES
        for book_id in matches:
            if book_id in potential_books:
                potential_books[book_id] += 1
            else:
                potential_books[book_id] = 1

    if miss_ratio > MISS_THRESHOLD:
        return None
    rank = sorted(potential_books.items(), key=op.itemgetter(1))
    #print "Rank:", rank
    best = rank[-1][0]
    return best

if __name__ == '__main__':
    ng.loadData()
    books = [f for f in listdir(BOOK_DIRECTORY) if isfile(join(BOOK_DIRECTORY, f))]
    correct, incorrect = 0, 0
    for b in books:
        for i in xrange(TEST_ITERS):
            test = sample.generateNoisySample(BOOK_DIRECTORY + b)
            samp, title, author = test
            print "Testing:", title, "by", author
            best = testSample(samp)
            if best == None:
                print "Best match: none"
                incorrect += 1.0
            else:
                test_title, test_author, test_filename = ng.book_info[best]
                print "Best match:", test_title, "by", test_author 
                if test_title == title:
                    correct += 1.0
                else:
                    incorrect += 1.0
    print "Testing complete."
    print "Accuracy:", correct/(len(books)*TEST_ITERS)*100, "%"
                
