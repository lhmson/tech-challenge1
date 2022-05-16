
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from word2number import w2n
from typing import List
import string

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

AGGREGATION_OPS = ('max', 'min', 'count', 'sum', 'avg')
UNIT_OPS = ('-', '+', "*", '/')
WHERE_OPS = ('not', 'between', '=', '>', '<', '>=', '<=', '!=', 'in', 'like', 'is', 'exists')
CLAUSE_KEYWORDS = ('select', 'from', 'where', 'group', 'order', 'limit', 'intersect', 'union', 'except')
JOIN_KEYWORDS = ('join', 'on', 'as')
COND_OPS = ('and', 'or')
SQL_OPS = ('intersect', 'union', 'except')
ORDER_OPS = ('desc', 'asc')
TABLE_TYPE = {
    'sql': "sql",
    'table_unit': "table_unit",
}

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def handle_agg_ops(arr: List[str]) -> List[str]:
    """
    Handle aggregation operations.
    """
    for i, tok in enumerate(arr):
        if tok in AGGREGATION_OPS:
            arr.insert(i+1, '(')
            arr.insert(i+3, ')')
            break
    return arr

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def remove_whitespace(text):
    return  " ".join(text.split())
 
def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    filtered_text = " ".join(filtered_text)
    return filtered_text

def stem_words(text):
    word_tokens = word_tokenize(text)
    stems = [stemmer.stem(word) for word in word_tokens]
    stems = " ".join(stems)
    return stems

def lemmatize_words(text):
    word_tokens = word_tokenize(text)
    # provide context i.e. part-of-speech
    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in word_tokens]
    lemmas = " ".join(lemmas)
    return lemmas

def handle_short_question(ques, sql):
    ques = ques.split(' ')
    if len(ques) < 5:
        indexToRemove = sql.index('where')
        sql = sql[0:indexToRemove]
    return sql

def text2int(textnum, numwords={}):
    """
    Converts string of length n with numbers written in letters into actual numbers of same length

    Args:
        textnum [Str] : string
        numwords [Dictionary]: dictonary of keywords that replaces text with numbers
    Returns:
        curstring [Str]: corrected string
    """
    if not numwords:
        units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)

    ordinal_words = {'first':1, 'second':2, 'third':3, 'fourth':4, 'fifth':5, 'sixth':6, 'seventh':7, 'eighth':8, 'ninth':9, 'tenth':10, 'twelfth':12}
    ordinal_endings = [('ieth', 'y')]
    zero_trailing = {'hundred': 100, 'thousand':1000, 'million':1000000, 'billion':1000000000, 'trillion':1000000000000}

    # TODO: this breaks joined words like right-handed. What was the purpose?
    #textnum = textnum.replace('-', ' ')

    current = result = 0
    curstring = ""
    onnumber = False
    num_tokens=len(textnum.split())
    tokens=textnum.split()
    for word in tokens:
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
        elif word in zero_trailing:
            current = current * zero_trailing[word]
            result += current
            current = 0
            onnumber = True
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                if onnumber:
                    curstring += repr(result + current) + " "
                if num_tokens-1 == tokens.index(word):
                    curstring += word + ""  
                else:  
                    curstring += word + " "
                result = current = 0
                onnumber = False
            else:
                scale, increment = numwords[word]

                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True

    if onnumber:
        curstring += repr(result + current)

    return curstring
