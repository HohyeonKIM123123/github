# 크롤링 전략 기반 실제 구동 코드 (네이버 블로그)
# 필요한 패키지: selenium, beautifulsoup4, requests, json
# pip install selenium beautifulsoup4 requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

# =========================
# 2. 분석 로직 (데이터 전처리 + 의미 추출)
# =========================
# 필요한 패키지: pandas konlpy soynlp emoji
# pip install pandas konlpy soynlp emoji

import re
import pandas as pd
from konlpy.tag import Okt
from soynlp.normalizer import repeat_normalize
import emoji

# --- 2.1 텍스트 정제 ---
def clean_text(text):
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^\w\s가-힣"\'·]', ' ', text)
    text = repeat_normalize(text, num_repeats=2)
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    okt = Okt()
    tokens = okt.morphs(text)
    tokens = [t for t in tokens if t not in stopwords]
    return ' '.join(tokens)

def split_sentences(text):
    return re.split(r'[.!?\n]', text)

# --- 2.2 엔티티 추출 ---
def extract_age(text):
    age_patterns = [
        (r'(20|스무|이십)[대살]', '20-29'),
        (r'(30|서른|삼십)[대살]', '30-39'),
        (r'(95|1995)년생', '25-29'),
        (r'(29)살', '25-29'),
    ]
    for pat, group in age_patterns:
        if re.search(pat, text):
            return group
    return None

def extract_job(text):
    job_dict = ['간호사', '의사', '개발자', '학생', '마케터', '교사', '디자이너']
    for job in job_dict:
        if job in text:
            return job
    return None

def extract_book(text):
    m = re.search(r'“([^”]+)”|"([^"]+)"|‘([^’]+)’|\'([^\']+)\'', text)
    if m:
        return m.group(1) or m.group(2) or m.group(3) or m.group(4)
    return None

# --- 2.3 도서 매칭 & 정규화 ---
def normalize_book_title(title):
    if not title:
        return None
    title = title.replace('나는 ', '').replace('로 ', '')
    return title.strip()

def enrich_book_meta(title):
    return {
        'isbn': None,
        'author': None,
        'publisher': None,
        'image': None
    }

# --- 2.4 감성 분석 ---
def analyze_sentiment(text):
    if '위로' in text or '좋았다' in text or '감동' in text:
        return 'positive'
    if '별로' in text or '실망' in text or '아쉬웠다' in text:
        return 'negative'
    return 'neutral'

# --- 2.5 데이터 모델화 ---
def to_datamodel(row):
    return {
        "age_group": row.get('age_group'),
        "job": row.get('job'),
        "book": row.get('book'),
        "sentiment": row.get('sentiment'),
        "platform": row.get('platform'),
        "date": row.get('date'),
    }

def process_data(raw_data):
    processed = []
    for item in raw_data:
        text = clean_text(item['raw_text'])
        sents = split_sentences(text)
        for sent in sents:
            if not sent.strip():
                continue
            age = extract_age(sent)
            job = extract_job(sent)
            book = extract_book(sent)
            book_norm = normalize_book_title(book)
            sentiment = analyze_sentiment(sent)
            meta = enrich_book_meta(book_norm)
            processed.append({
                "age_group": age,
                "job": job,
                "book": book_norm,
                "sentiment": sentiment,
                "platform": item.get('platform'),
                "date": item.get('timestamp'),
            })
    return processed

if __name__ == "__main__":
    with open('naver_blog_results.json', encoding='utf-8') as f:
        raw_data = json.load(f)
    processed = process_data(raw_data)
    with open('naver_blog_processed.json', 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 전처리/분석 완료: {len(processed)}건 저장")
