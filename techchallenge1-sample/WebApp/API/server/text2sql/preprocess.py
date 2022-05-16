
from typing import List, Tuple
from word2number import w2n
from .utils import *

def default_preprocessing(schema: str, question: str, sql:str="") -> Tuple[str]:
    # For dataset builder
    schema = handle_schema(schema)
    question = handle_question(question)
    sql = handle_sql(sql)
    if sql == "":
        return schema, question

    else:
        return schema, question, sql

def handle_schema(schema: str) -> str:
    """
    Handle schema.
    """
    schema = ", ".join(schema).upper()
    return schema

def handle_question(question: str) -> str:
    """
    Handle question.
    """
    question = question.lower()
    question = remove_punctuation(question)
    question = remove_whitespace(question)
    question = text2int(question)
    # question = remove_stopwords(question)
    # question = stem_words(question)
    question = lemmatize_words(question)

    # question = " ".join(question)
    
    print(question)
    return question

def handle_sql(sql: str) -> str:
    """
    Handle sql.
    """
    sql = sql.upper()
    return sql

