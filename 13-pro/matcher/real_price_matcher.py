import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def match_similar_transaction(room, real_transactions_df, n_matches=3):
    """
    매물 데이터와 실거래가 데이터를 비교하여 가장 유사한 실거래 데이터를 찾아 반환하는 함수입니다.
    
    :param room: 크롤링된 매물 데이터 (DataFrame 행)
    :param real_transactions_df: 실거래가 데이터 (DataFrame)
    :param n_matches: 유사한 실거래가를 몇 개 매칭할지 (기본값 3개)
    
    :return: 매칭된 실거래가 데이터
    """
    # 매물 데이터에서 면적과 가격 정보를 사용하여 실거래가를 매칭합니다.
    room_area = room['면적']
    room_price = int(room['보증금'].replace(',', '').replace('만원', '').strip())  # 보증금을 숫자형으로 변환
    
    # 실거래가 데이터에서 면적과 거래금액을 비교합니다.
    real_transactions_df = real_transactions_df.dropna(subset=['전용면적', '거래금액'])
    
    # 면적과 거래금액을 비교하여 유사도 측정 (여기서는 간단한 유클리디언 거리로 매칭)
    real_transactions_df['면적_diff'] = np.abs(real_transactions_df['전용면적'] - room_area)
    real_transactions_df['price_diff'] = np.abs(real_transactions_df['거래금액'] - room_price)
    
    # 두 값을 합산하여 가장 유사한 실거래가 선택
    real_transactions_df['total_diff'] = real_transactions_df['면적_diff'] + real_transactions_df['price_diff']
    
    # 유사도가 가장 높은 실거래가 n개를 반환
    matched_real = real_transactions_df.nsmallest(n_matches, 'total_diff')
    
    return matched_real