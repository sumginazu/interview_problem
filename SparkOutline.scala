#I haven't tried to run/test this - please forgive any syntax errors
#and let me know if anything is unclear. It's been a while since I've
#coded anything in Scala.

#################

#stream of books -> database
#for simplicity, I'm assuming that our corpus is labeled already,
#that a bookID -> author/title/etc index is already available, 
#and that book_data is a collection of tuples of the form (bookID, rawtext)

val tokenized = book_data.map((bookID, rawtext) => (bookID, tokenize(rawtext))

val book_tokens_with_index = tokenized.map((bookID, tokens) => (bookID, zipWithIndex(tokens).groupBy(_._1))

val tokens_to_bookID = tokenized.flatMap((bookID, tokens) => tokens.distinct().map(tok => (tok, bookID)))
    		       		.groupByKey()

#persist book_tokens_with_index, tokens_to_bookID and reuse as needed

#################

#collection of ngrams -> collection of books that could contain those ngrams
#for simplicity, assume n is 3
#and that ngrams is a collection of tuples of the form (ngramID, (tok1, tok2, tok3))
#also assume that the list of bookIDs for a given token can fit in memory

def ngramList(ngramID: Long, tok1: String, tok2: String, tok3: String): List[(String, Long)] = {
    #I'm sure a function for this exists already 
    List((tok1, ngramID),
    	 (tok2, ngramID),
	 (tok3, ngramID))
}
def search(bookList: List[(Long, Map[String, Traversable[(String, Int)]])], tok1: String, ... ): List[(Long, Int)] = {
    #each element of bookList is a (bookID, invIdx) tuple.
    #we can use these to find any/all existing matches in each book.
    #from there, we can output a list of books and some value representing
    #the presence of this ngram in each book.
}
val potential_books = ngrams.flatMap((ngramID, (tok1, tok2, tok3)) => ngramList(ngramID, tok1, tok2, tok3))
    		      	    .join(tokens_to_bookID)
			    .map((tok, (ngramID, bookIDs)) => (ngramID, bookIDs))
			    .groupByKey()
			    .map((ngramID, listOfListsOfBooks) => (ngramID, intersectionAll(listOfListsOfBooks)))
			    .flatMap((ngramID, books) => books.map(book => (book, ngramID)))
			    .join(book_tokens_with_index)
			    .map((bookID, (ngramID, tokenDict)) => (ngramID, (bookID, tokenDict))
			    .groupByKey()
			    .join(ngrams)
			    .map((ngramID, (bookList, (tok1, tok2, tok3))) => (ngramID, search(bookList, tok1, tok2, tok3)))
			    .groupByKey()

#potential_books is a collection of (ngramID, List[(bookID, score)]) tuples.
#from here, we can map/reduce our way into a collection of (passageID, List[(bookID, score)]) tuples,
#allowing us to identify the best matching book per passage.

#there's plenty of room for improvement - the first groupByKey() in the assignment to potential_books
#(and the following map()) can be replaced by a reduceByKey().
#also, the 3rd groupByKey() is aggregating several indexes into a single node.
#I'm not certain there's a good way around that, but I could potentially change
#book_tokens_with_index so that it used (bookID, token) keys, increasing the granularity of the join.
			    



