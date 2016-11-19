import AuthorStats
import Sample as sample
from os import listdir
from os.path import isfile, join
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

BOOK_DIRECTORY = "test_books/"
TEST_DIRECTORY = "test_books/holdout/"
NUM_SAMPLES = 20

if __name__ == '__main__':
    AuthorStats.loadData()

    train_data = []
    books = [f for f in listdir(BOOK_DIRECTORY) if isfile(join(BOOK_DIRECTORY, f))]
    for b in books:
        f = open(BOOK_DIRECTORY + b, 'r')
        raw = f.read()
        f.close()
        for i in xrange(NUM_SAMPLES):
            samp, title, author = sample.generateNoisySample(raw, noise)
            features = AuthorStats.calculateStats(samp)
            train_data.append((features, author))

    print "Training with", len(books)*NUM_SAMPLES, "samples."
    classifier = NaiveBayesClassifier.train(train_data)

    test_data = []
    test_books = [f for f in listdir(TEST_DIRECTORY) if isfile(join(TEST_DIRECTORY, f))]
    for b in test_books:
        f = open(TEST_DIRECTORY + b, 'r')
        raw = f.read()
        f.close()
        for i in xrange(NUM_SAMPLES):
            samp, title, author = sample.generateNoisySample(raw)
            features = AuthorStats.calculateStats(samp)
            test_data.append((features, author))

    print "Accuracy on", len(test_books)*NUM_SAMPLES, "test samples:", nltk.classify.accuracy(classifier, test_data)
    classifier.show_most_informative_features()
