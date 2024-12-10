'''
Created on 2024/12/01

@author: kotaro
'''

import streamlit as st
import requests
import os
import random
from st_supabase_connection import SupabaseConnection

# Supabaseとの接続情報
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# アプリケーションのメイン
st.title("Nanikiru?")

# Superbaseからクイズデータを取得
# Initialize Supabase connection.
conn = st.connection(name="supabase", type=SupabaseConnection, url=SUPABASE_URL, key=SUPABASE_KEY)

# Pythonクライエントを取得
supabase = conn.client

st.write(dir(conn))

def fetch_quiz():
    try: 
        # Perform query.
        response = supabase.table("nanikiru").select("*").execute()

        # レスポンスデータがあるとき
        if response.data:
            # ランダムに1問選ぶ
            quiz_data = random.choice(response.data)
            return quiz_data

        # レスポンスデータがないとき
        if not response.data: 
            st.error("クイズデータが見つかりません。")
            return None
        
    except Exception as e: 
        st.error(f"クイズデータの取得中にエラーが発生しました。{e}")
        return None

# クイズデータのオブジェクト生成
quiz = fetch_quiz()

if quiz: 
    # 自風、場風、ドラを表示
    st.write(f"自風: {quiz['your_wind']}/ 場風: {quiz['table_wind']}")
    st.write(f"ドラ: {quiz['dragon_normal']}")

    # 手牌を表示
    st.write("手牌: ")
    hand_tiles = quiz['hand'].split(",") # 1カラム1牌にするならここは変える!

    # 手牌を表示する列を生成
    hand_columns = st.columns(len(hand_tiles))
    for i, tile in enumerate(hand_tiles): 
        hand_tile_url = f"https://raw.githubusercontent.com/kotaroburrito/mahjong/master/images/{tile}.PNG"
        
        # 各列に牌の画像を配置
        with hand_columns: 
            st.image(hand_tile_url, width=20)

    # ツモを表示
    st.write("ツモ: ")
    zimo_tile_url = f"https://raw.githubusercontent.com/kotaroburrito/mahjong/master/images/{quiz['zimo']}.PNG"
    st.image(zimo_tile_url, width=20)

    # 答えを非表示にしておき、回答後に表示
    if st.button("答えを見る"): 
        correct_tile_url = f"https://raw.githubusercontent.com/kotaroburrito/mahjong/master/images/{quiz['correct_tile']}.PNG"
        st.write("正解: ")
        st.image(correct_tile_url, width=50)
        st.write(f"解説: {quiz['explanation']}")



