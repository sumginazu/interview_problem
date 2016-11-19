import string
import random as r
import nltk
from nltk import word_tokenize, sent_tokenize

BOOK_DIRECTORY = "test_books/"
BOOK_START = "*** START OF"# THE PROJECT GUTENBERG EBOOK"
BOOK_END   = "*** END OF"# THE PROJECT GUTENBERG EBOOK"
BOOK_TITLE = "Title: "
BOOK_AUTHOR = "Author: "
LINES_MAX, LINES_MIN = 20, 5 #assumption: books have at least 20 lines
CORRUPTION_RATIO = 0.1 #is this reasonable?
CORRUPT_TOKEN = "XXXXXX"

def generateNoisySample(raw, noise=True):
    #returns an incomplete, noisy sample of the given book, plus title/author
    #assuming standard Project Gutenberg formatting

    #Get the next line after the start string
    startidx = string.find(raw, '\n', string.find(raw, BOOK_START)) + 1
    #Get the index of the end string
    endidx = string.find(raw, BOOK_END)

    header = raw[:startidx].strip()
    book = raw[startidx:endidx].strip()
    book_sents = sent_tokenize(book)
    
    #extract metadata
    titleidx = string.find(header, BOOK_TITLE) + len(BOOK_TITLE)
    titleend = string.find(header, '\n', titleidx)
    title = header[titleidx:titleend].strip()
    authoridx = string.find(header, BOOK_AUTHOR) + len(BOOK_AUTHOR)
    authorend = string.find(header, '\n', authoridx)
    author = header[authoridx:authorend].strip()
    
    #select a random sequence of sentences, then convert to tokens
    nlines = len(book_sents)
    sample_nlines = r.randint(LINES_MIN, LINES_MAX)
    sample_idx = r.randint(0, nlines-sample_nlines-1)
    sample_lines = book_sents[sample_idx:sample_idx+sample_nlines]

    if noise:
        #corrupt random tokens
        #this probably isn't realistic corruption, but it will do
        sample_tokens = word_tokenize(' '.join(sample_lines))
        ntokens = len(sample_tokens)
        ncorruptions = int(CORRUPTION_RATIO * ntokens) + 1
        for i in xrange(ncorruptions):
            sample_tokens[r.randint(0, ntokens-1)] = CORRUPT_TOKEN
        sample_tokens = ' '.join(sample_tokens) #sloppy, but it'll do
    else:
        sample_tokens = ' '.join(sample_lines)
    return [sample_tokens, title, author]


if __name__ == '__main__':
    f = open(BOOK_DIRECTORY + "1342.txt", 'r')
    raw = f.read()
    f.close()
    print generateNoisySample(raw)
