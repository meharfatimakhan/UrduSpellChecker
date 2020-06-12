# Urdu Spell Checker

This code implements an Urdu Spell Checker using Noisy Channel Model.

### Train Bigram Model

1.	The corpus from ‘jang.txt’ is read into a dictionary. Each index of this dictionary stores each sentence in the corpus.

2.	The sentences in the dictionary are tokenized and read into a list. The length of the list is calculated and stored, and Counter is applied on the list which generates all unigrams in ‘jang.txt’.

3.	Bigrams are identified through the list above and are stored in a bigram list. After this, Counter is applied on said list which generates all bigrams in ‘jang.txt’.

4.	After bigram and unigram count is calculated, probabilities for each bigram is calculated and stored in a dictionary. The probabilities are computed with this formula:

```
biwordCount(word[0] | word[1]) / unigramCount(word[0])
```


### Find Candidate Words

1.	The corpus from ‘jang_errors.txt’ is read into a dictionary. Each index of this dictionary stores each sentence in the corpus. This corpus contains error words.

2.	The dictionary of words from ‘wordlist.txt’ is read and stored in a list. Then a Counter is applied on the list and maintains count of each word in the dictionary.

3.	The error words in ‘jang_errors.txt’ are identified by checking whether they exist in ‘wordlist.txt’ or not. Their position i.e., sentence number (row value) and word location (column value) are saved. These error words are stored in a dictionary.

4.	Candidates of each error word are computed, and bigrams are made with words that are next and previous to the error word. If the next and previous words do not exist in ‘wordlist.txt’ then they are added there.

5.	All these new bigrams are added to the list of previous bigrams, and a Counter is applied on them. The bigrams (which are not present in the previous bigram list) are assigned a probability of zero.

6.	Probability is calculated for the entire list of bigrams and add-1 smoothing is applied to eliminate the zero probabilities. The smoothed probabilities are computed with this formula below. Then these biword probabilities are read into a file.


```
(newbiwordCount(word[0] | word[1]) + 1) /(unigramCount(word[0]) + lengthOf(‘jang.txt’))
```


### Ranking Candidate Words

1.	The corpus from ‘jang_nonerrors.txt’ is read into a dictionary. Each index of this dictionary stores each sentence in the corpus. This corpus contains corrected words.

2.	The accurate location of each word in ‘jang_nonerrors.txt’ i.e., sentence number (row value) and word location (column value) are computed and stored in a dictionary as keys.

3.	Probabilities of the candidate words generated for the error word are calculated. They are computed by multiplying the next and previous bigrams of the error word together. These probabilities are stored in a dictionary for each error word and then this dictionary is sorted in reverse order. 

4.	The top 10 words in the dictionary are selected. If any of the 10 words exists in ‘jang_nonerrors.txt’ at that precise location then a ‘YES’ is generated. Otherwise, it is a ‘NO’
