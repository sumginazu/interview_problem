import string
import random as r

BOOK_DIRECTORY = "test_books/"
BOOK_START = "*** START OF"# THE PROJECT GUTENBERG EBOOK"
BOOK_END   = "*** END OF"# THE PROJECT GUTENBERG EBOOK"
BOOK_TITLE = "Title: "
BOOK_AUTHOR = "Author: "
LINES_MAX, LINES_MIN = 20, 5 #assumption: books have at least 20 lines
CORRUPTION_RATIO = 0.1 #is this reasonable?
CORRUPT_TOKEN = "XXXXXX"

def generateNoisySample(filename):
    #returns an incomplete, noisy sample of the given book, plus title/author
    #assuming standard Project Gutenberg formatting
    
    f = open(filename, 'r')
    raw = f.read()
    f.close()

    #Get the next line after the start string
    startidx = string.find(raw, '\n', string.find(raw, BOOK_START)) + 1
    #Get the index of the end string
    endidx = string.find(raw, BOOK_END)

    header = raw[:startidx].strip()
    book = raw[startidx:endidx].strip()
    book_lines = book.split('\n')

    #extract metadata
    titleidx = string.find(header, BOOK_TITLE) + len(BOOK_TITLE)
    titleend = string.find(header, '\n', titleidx)
    title = header[titleidx:titleend].strip()
    authoridx = string.find(header, BOOK_AUTHOR) + len(BOOK_AUTHOR)
    authorend = string.find(header, '\n', authoridx)
    author = header[authoridx:authorend].strip()
    
    #select a random sequence of lines, then convert to tokens
    #TODO use nltk to remove stopwords / better tokenizing
    nlines = len(book_lines)
    sample_nlines = r.randint(LINES_MIN, LINES_MAX)
    sample_idx = r.randint(0, nlines-sample_nlines-1)
    sample_lines = book_lines[sample_idx:sample_idx+sample_nlines]
    sample_tokens = '\n'.join(sample_lines).split()

    #corrupt random tokens
    #this probably isn't realistic corruption, but it will do
    ntokens = len(sample_tokens)
    ncorruptions = int(CORRUPTION_RATIO * ntokens) + 1
    for i in xrange(ncorruptions):
        sample_tokens[r.randint(0, ntokens-1)] = CORRUPT_TOKEN

    #discards line info, but that won't affect our model    
    return [' '.join(sample_tokens), title, author]


if __name__ == '__main__':
    print generateNoisySample(BOOK_DIRECTORY + "158.txt")
