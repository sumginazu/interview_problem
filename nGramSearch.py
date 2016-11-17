import DatabaseManager as db

num_books = 0
inv_index_token2book = {} #there's certainly a better name for this
book_info = {} #title/author/filename
book_inv = {} #book id -> inverted index
author_books = {} #author -> book ids

def loadData():
    db.loadDatabase()
    num_books = db.num_books
    inv_index_token2book = db.inv_index_token2book
    book_info = db.book_info
    book_inv = db.book_inv
    author_books = db.author_books

def matchNGram(ngram):
    #ngram: list of tokens
    return None
