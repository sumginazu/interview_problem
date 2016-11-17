from os import listdir
from os.path import isfile, join
import string
import io
import json

DATABASE_FILE = "Gutenberg.db"
BOOK_DIRECTORY = "test_books/"
BOOK_START = "*** START OF"# THE PROJECT GUTENBERG EBOOK"
BOOK_END   = "*** END OF"# THE PROJECT GUTENBERG EBOOK"
BOOK_TITLE = "Title: "
BOOK_AUTHOR = "Author: "

num_books = 0
inv_index_token2book = {} #there's certainly a better name for this
book_info = {} #title/author/filename
book_inv = {} #book id -> inverted index
author_books = {} #author -> book ids

def parseGutenbergBook(filename):
    #assuming standard Project Gutenberg formatting
    global num_books, inv_index_token2book
    global book_info, book_inv, author_books

    f = open(filename, 'r')
    raw = f.read()
    f.close()
        
    book_id = str(num_books)
    num_books += 1

    #Get the next line after the start string
    startidx = string.find(raw, '\n', string.find(raw, BOOK_START)) + 1
    #Get the index of the end string
    endidx = string.find(raw, BOOK_END)

    header = raw[:startidx].strip()
    book = raw[startidx:endidx].strip()

    #extract metadata
    titleidx = string.find(header, BOOK_TITLE) + len(BOOK_TITLE)
    titleend = string.find(header, '\n', titleidx)
    title = header[titleidx:titleend].strip()
    authoridx = string.find(header, BOOK_AUTHOR) + len(BOOK_AUTHOR)
    authorend = string.find(header, '\n', authoridx)
    author = header[authoridx:authorend].strip()

    #construct inverted index for this book
    inv_index = {}
    book_tokens = book.split()
    #TODO remove stopwords, punctuation?
    for i, tok in enumerate(book_tokens):
        tok = tok.lower()
        if tok in inv_index:
            inv_index[tok].append(i)
        else:
            inv_index[tok] = [i]
    #populate global dictionaries
    for tok in inv_index:
        if tok in inv_index_token2book:
            inv_index_token2book[tok].append(book_id)
        else:
            inv_index_token2book[tok] = [book_id]
    book_info[book_id] = [title, author]
    book_inv[book_id] = inv_index
    if author in author_books:
        author_books[author].append(book_id)
    else:
        author_books[author] = [book_id]

    return

def writeToDatabase(filename=DATABASE_FILE):
    global num_books, inv_index_token2book
    global book_info, book_inv, author_books
    collect = [num_books,
               inv_index_token2book,
               book_info,
               book_inv,
               author_books]
    with open(filename, "w") as f:
        data = json.dump(collect, f)

def ascii_encode_dict(data): #this sucks
    return dict((a.encode('ascii'),b) for (a,b) in data.items())
        
def loadDatabase(filename=DATABASE_FILE):
    global num_books, inv_index_token2book
    global book_info, book_inv, author_books
    with open(filename, "r") as f:
        collect = json.load(f, object_hook=ascii_encode_dict)
        num_books = collect[0]
        inv_index_token2book = collect[1]
        book_info = collect[2]
        book_inv = collect[3]
        author_books = collect[4]
        
def test():
    parseGutenbergBook("test_books/84.txt")

if __name__ == "__main__":
    books = [f for f in listdir(BOOK_DIRECTORY) if isfile(join(BOOK_DIRECTORY, f))]
    for b in books:
        parseGutenbergBook(BOOK_DIRECTORY + b)
    print book_inv['0'].keys()[:5]
    print book_inv['0'].values()[:5]
    print "------------"
    writeToDatabase(DATABASE_FILE)
    print "Write complete."
    loadDatabase(DATABASE_FILE)
    print "Load complete."
    print book_inv['0'].keys()[:5]
    print book_inv['0'].values()[:5]
        


