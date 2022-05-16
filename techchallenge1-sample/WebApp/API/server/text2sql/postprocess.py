from nltk import word_tokenize
from .utils import *

import nltk
nltk.download('punkt')

import re

def tokenize(string):
    string = str(string)
    string = string.replace("\'", "\"")
    quote_idxs = [idx for idx, char in enumerate(string) if char == '"']
    assert len(quote_idxs) % 2 == 0, "Unexpected quote"

    # keep string value as token
    vals = {}
    for i in range(len(quote_idxs)-1, -1, -2):
        qidx1 = quote_idxs[i-1]
        qidx2 = quote_idxs[i]
        val = string[qidx1: qidx2+1]
        key = "__val_{}_{}__".format(qidx1, qidx2)
        string = string[:qidx1] + key + string[qidx2+1:]
        vals[key] = val

    toks = [word.lower() for word in word_tokenize(string)]
    # replace with string value token
    for i in range(len(toks)):
        if toks[i] in vals:
            toks[i] = vals[toks[i]]

    # find if there exists !=, >=, <=
    eq_idxs = [idx for idx, tok in enumerate(toks) if tok == "="]
    eq_idxs.reverse()
    prefix = ('!', '>', '<')
    for eq_idx in eq_idxs:
        pre_tok = toks[eq_idx-1]
        if pre_tok in prefix:
            toks = toks[:eq_idx-1] + [pre_tok + "="] + toks[eq_idx+1: ]

    # for word in toks:
    #     if any(letter in ['\'','\"'] for letter in word):
    #         word = re.sub('!@#$%^&*?<>;', '', word)
    #         print(word)
    return toks



def default_postprocessing(sql: str, ques: str) -> str:
    print('post process', sql)
    sql = sql.split('|')[-1]
    sql = sql.replace('_FIELD', '').lower()
    sql = tokenize(sql)
    sql = handle_agg_ops(sql)
    sql = handle_short_question(ques, sql)
    sql = " ".join(sql)
    sql = remove_whitespace(sql)
    return sql