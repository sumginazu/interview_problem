import DatabaseManager as db

num_books = 0
inv_index_token2book = {} #there's certainly a better name for this
book_info = {} #title/author/filename
book_inv = {} #book id -> inverted index
author_books = {} #author -> book ids

def loadData():
    global num_books, inv_index_token2book
    global book_info, book_inv, author_books
    db.loadDatabase()
    num_books = db.num_books
    inv_index_token2book = db.inv_index_token2book
    book_info = db.book_info
    book_inv = db.book_inv
    author_books = db.author_books

def tokenLookup(tok):
    #helper function to safely access dict
    if tok in inv_index_token2book:
        return inv_index_token2book[tok]
    else:
        return []
        
def matchNGram(ngram):
    #ngram: list of tokens
    #returns a list of books that contain the given n-gram

    #get all books that contain every word in the ngram
    book_ids = set(tokenLookup(ngram[0]))
    for tok in ngram[1:]:
        book_ids &= set(tokenLookup(tok))

    #iterate through these books, noting those which contain this n-gram
    #(or, if desired, a fuzzy approximation, not implemented here)
    matches = []
    for book in book_ids:
        inv_idxs = [book_inv[book][tok] for tok in ngram]
        #idx_iter contains pointers we can advance along the inverted indexes.
        idx_point = [0 for tok in ngram]
        more = True #is there more to search?
        while more:
            #check to see if the current token locations represent an n-gram
            idxs = [inv_idxs[i][idx_point[i]] for i in xrange(len(ngram))]
            if all([idxs[i+1] - idxs[i] == 1 for i in xrange(len(ngram)-1)]):
                #if all the indices are sequential, we have a match
                matches.append(book)
                break
            else:
                #otherwise, we advance the pointer to the lowest index
                lowest_val = min(idxs)
                for i in xrange(len(ngram)):
                    if idxs[i] == lowest_val:
                        idx_point[i] += 1
                    #check to avoid going out of bounds
                    if idx_point[i] >= len(inv_idxs[i]):
                        more = False
                        break
    return matches

    
        
if __name__ == '__main__':
    loadData()
    matched_books = matchNGram(["campaign", "brought", "honours"])
    print [book_info[b] for b in matched_books]
    
