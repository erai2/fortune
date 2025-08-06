import json, os
from .db_utils import load_json, save_json

DB_PATH = './data/terminology.json'

def load_terms():
    return load_json(DB_PATH)

def save_terms(data):
    save_json(DB_PATH, data)

def search_term(keyword):
    terms = load_terms()
    return [t for t in terms if keyword in t['Term'] or keyword in t['Meaning']]

# CSV→JSON 변환, 유사어 탐색, 통합검색 등