# interview_problem
Solution to the interview question.

##Comments

My solution for part a) doesn't involve machine learning - it uses inverse indexing to match ngrams in the sample and target texts. I knew supervised learning wouldn't be appropriate here due to the massive number of potential labels, and for the same reason I wasn't too keen on using a simple unsupervised learning technique like k-means (though there might be another more appropriate method I don't know about.) This sounded more like a search problem than a classification problem, so that's what I did.

My solution for part b) is not great - it's an overly simple Naive Bayes classifier. It really needs more data, but I'm not sure how well it would perform even with that data - I think the issue is that my features are intended for uncorrupted samples (or perhaps just larger samples). I got inspiration for these features by researching author detection, but I don't recall seeing any sources that dealt with potential noise in the data.

I got my training/testing data from Project Gutenberg. I couldn't figure out how to download large amounts of books from them (the instructions I followed didn't seem to work) so I just manually downloaded a small handful. My training corpus has 8 texts total from 3 authors, and my training corpus has 3 texts total from the same 3 authors.

Running 'python partATest.py' and 'python partBTest.py' should run the tests I made. NLTK is required.

##Additional questions
#1. Is your system scalable w.r.t. size of your dataset? If not, how would address the scalability (in terms of algorithms, infrastructure, or both)? Would you be able to sketch Spark/MapReduce code for performing some of the necessary computations (would be a big plus!) ?

It's relatively scalabale - my solution for part a) is based on an indexing system I learned about in my search engines class, and is easily applicable to distributed systems. My model for part b) desperately needs more data, and the only limitation in terms of training data is how many features we can hold at once to train with (and there are even ways around that.) Obviously if we were to scale this out it would require some reworking, probably in another language, but the design itself is fairly scalable.

In terms of map-reduce: that shouldn't be hard, as most operations done are on books or snippets of text and therefore can easily accomplished via a map. For example, with a function creating the inverse indexes for each book, we can map that out to an arbitary number of books and then reduce that to a single datastructure (or perhaps multiple distributed ones). Getting the token -> books containing said token dictionary from a single reduce is kind of a bottleneck but still within reason. Similarly, feature calculation is made easy with maps. If you want me to give more specifics on how I'd sketch out this mapreduce code, I'd be happy to elaborate.

#2. How could you figure out which are the most informative features for each of the tasks above?

I didn't use any features for part a), but for part b) I print out these features while testing. (NLTK does it for me!) This involves estimating the entropy of each feature/class pair and using that to determine which feature has the highest expected information gain associated with it.

#3. In general, how would you assess the performances of your system?

I'm not a fan of using accuracy to measure performance in general, but here I think it's the most telling metric of how my models are doing. In both cases the problem involves multiclass classification, so precision/relevance aren't quite relevant.