# -- Ex3_practical part:  --------------------------------------------------
#   submitted by: Maayan Sharon & Imri Dror

# -- Imports ---------------------------------------------------------------
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt
import re

# -- Functions---------------------------------------------------------------

def list_to_count(lst):
    """
    function: making a counter of unique appearances of objects in list
    :param lst: any list
    :return: a dictionary with objects as keys and appearances counter as value
    """
    token_dic = dict()
    for w in lst:
        val = token_dic.get(w)
        if val:
            token_dic[w] = val + 1
        else:
            token_dic[w] = 1
    return token_dic


def list_to_count_fixed(lst):
    """
    function: making a counter of unique appearances (ignoring dots in the
    end of a word)  of objects in list
    :param lst: any list
    :return: a dictionary with objects as keys and appearances counter as value
    """
    token_dic = dict()
    for w in lst:
         if w[-1] == ".":
            new_w = w[:-1]
            val = token_dic.get(new_w)
            if val:
                token_dic[new_w] = val + 1
            else:
                token_dic[new_w] = 1
         else:
            val = token_dic.get(w)
            if val:
                token_dic[w] = val + 1
            else:
                token_dic[w] = 1
    return token_dic


def plt_dic(row_dic, name):
    """
    function: making a log-log sorted plot and top appearing words.
    :param row_dic: unsorted dic of tokens and appearances.
    :output: a plot and consule print of top 20 appearances.
    """
    sorted_dic = {k: v for k, v in sorted(row_dic.items(), key=lambda item: item[
        1],reverse=True)}
    print("top freq words - " + name)
    print(list(sorted_dic.items())[:20])
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(sorted_dic.keys(),sorted_dic.values(), s=10, c='b', marker="s")
    ax1.set_yscale('symlog')
    ax1.set_xscale('symlog')
    plt.xlabel("words")
    plt.ylabel("freq")
    plt.title(name + "Freq of words")
    plt.show()


def wordcloud_pos(lst_pos):
    """
    function: takes all tokens identified as NNP or NNPS and appends
        it to a new txt file for using the word cloud web algorithm
        at: https://www.wordclouds.com/
    :param lst_pos: list of pos tagged words.
    :output: text file.
    """
    with open("wordcloud.txt", "w") as out_file:
        pos_kinds = ["NNP","NNPS"]
        for token in lst_pos:
            if token[1] in pos_kinds:
                out_file.write(token[0]+ " ")
        out_file.close()


def find_sentence(word_pos_lst):
    """
    function: sorting function by POS with the following logics:
    # find an adj
    # if next is adj - keep looking for adj or noun
    # else if next is noun - mark valid = true, keep looking for noun
    # found something is not noun - append to list
    # else keep find adj
    :param word_pos_lst: list of pos tagged words.
    :return: sentence_list - all relevant sentences to the logics.
    """
    adj = "JJ"
    noun = "NN"
    sentence_list = []
    len_lst = len(word_pos_lst)
    word_counter = 0
    sent_valid = False
    sent_done = False  # found a valid sentence and it's complete
    while word_counter != len_lst:  # as long we still have words in story

        if word_pos_lst[word_counter][1] == adj:  # found adj
            cur_sent = word_pos_lst[word_counter][0]  # add adj to cur sen
            word_counter += 1
            while word_counter != len_lst:  # keep looking for adj or noun
                if adj in word_pos_lst[word_counter][1] and not sent_valid:
                    # found adj
                    cur_sent = cur_sent + " " + word_pos_lst[word_counter][0]
                    word_counter += 1
                elif noun in word_pos_lst[word_counter][1]:  # found noun
                    cur_sent = cur_sent + " " + word_pos_lst[word_counter][0]
                    sent_valid = True
                    word_counter += 1
                else:  # not a noun or adj
                    if sent_valid is True:
                        sentence_list.append(cur_sent)
                    word_counter += 1
                    sent_valid = False
                    break  # sentence is not valid, look for a new adj
        else:
            word_counter += 1
    return sentence_list

# -- Main --------------------------------------------------------------------


# input file to string:
text = str()
with open('Peter_Pan.txt', "r", encoding="utf-8") as file:
    for line in file:
        text += line + " "
    file.close()

# basic tokenizing
tokens = word_tokenize(text.lower())
dict_basic = list_to_count(tokens)
print("number of tokens - basic: " + str(len(dict_basic)))
plt_dic(dict_basic, "basic tokens: ")

# tokenize without stopwords
stop = set(stopwords.words('english'))
# unused: stop.update(["[","]","(",")",'”', '“',"."])
#         explanation: potential insert to stopwords.
tokens_no_stop = [i for i in word_tokenize(text.lower()) if i not in stop]
dict_no_stop = list_to_count_fixed(tokens_no_stop)
print("number of tokens - no stopwords: " + str(len(dict_no_stop)))
plt_dic(dict_no_stop, "no stopwords tokens: ")

# tokenize stemmed
ps = nltk.stem.PorterStemmer()
tokens_stemm = [ps.stem(i) for i in word_tokenize(text.lower()) if i not in stop]
dict_stemm = list_to_count_fixed(tokens_stemm)
print("number of tokens - stemm: " + str(len(dict_stemm)))
plt_dic(dict_stemm, "stemm tokens: ")

# pos tokenize :
token_pos = nltk.pos_tag(tokens)
print(token_pos)
# output file for wordcloud making online
wordcloud_pos(token_pos)


# find adj +noun and concat to a sentence and plot it
sentence_lst = find_sentence(token_pos)
dict_sent = list_to_count(sentence_lst)
print("\n the list of all tokenized adj+noun sentences after POS : \n")
print(sentence_lst)
print("counter of all sentence appirences: "+str(dict_sent))
print("number of tokens - sentence: " + str(len(sentence_lst)))
plt_dic(dict_sent, "sentence: ")


# regular expression finding:
cons_lst = re.findall(r'\b(\w+)(\s|\W+)\1+\b',text)
print(cons_lst)
double_words =[]
for tup in cons_lst:
    double_words.append(tup[0])
print("these are the words:")  # find all words
print(double_words)
print("length of this list: ",len(double_words))

double_set = set(double_words)  # find unique words
print("those are the words without duplications:" + str(double_set))
print(len(double_set))

