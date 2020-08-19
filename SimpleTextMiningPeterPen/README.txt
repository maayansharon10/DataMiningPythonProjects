Problem 3 (Text Mining ).
In this problem I download the book "Peter Pen" from Project Gutenberg https://www.gutenberg.org
all answers and output in output folder
ex:
(b) Tokenize the text. Count occurrences for each token. 
Plot the results (y axis: frequency, logarithmic scale. x axis: rank, logarithmic scale; in other words, the tokens are sorted along the x-axis so that the
frequencies are decreasing, axes are in logscale). 
Also print a list of the top 20 tokens (separate from the plot). 
(c) Repeat (b) after removing stopwords.
(d) Repeat (b) after removing stopwords and stemming the text. 
(e) Run POS-tagging on the original text. 
Extract all the adj+noun phrases. For this exercise, we will define it as one or more adjectives, followed by one or more nouns, including proper nouns (the longest
such sequence). 
For example – delicious peanut butter cookies, oval office. 
Repeat (b) using adj+noun phrases as tokens (that is, count occurrences of each adj+noun phrase, print the top 20 phrases and
plot the log-log graph of counts). 
(f) Show one example sentence where POS tagging made a mistake (explain). 
(g) Create a Tag cloud (word cloud) of proper nouns (NNP, NNPS) (see output file)
but you can use anything. Does it correspond to what you know about the book? 
(h) Write a regular expression to find the set of all strings with two consecutive repeated words, with
potential punctuation between them (e.g., “well well”, “so so”, and “no, no”). Run on your text and report any found.