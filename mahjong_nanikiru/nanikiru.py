'''
Created on 2024/12/01

@author: kotaro
'''

import streamlit as st
import requests
import os
import random
from st_supabase_connection import SupabaseConnection

# 牌のサイズ
PAI_WIDTH = 20

# 牌の画像URLベース
PAI_URL = os.getenv("PAI_URL")
PNG = ".PNG"

# 手牌表示用のCSSレイアウト定義
st.markdown("""
<style>
.hand-container {
    display: flex;
    justify-content: center;
    gap: 0px /* 牌の間の余白を0にする */
    }

.hand-container img {
    margin: 0 /* 各画像の余白をなくす */
    padding: 0;
    }
</style>
""", unsafe_allow_html=True
)

hand_html = "<div class='hand-container'>"

# 回答ボタンの文言
SHOW_ANSWER_BUTTON = "答えを見る"

# Supabaseとの接続情報
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase connection.
conn = st.connection(name="supabase", type=SupabaseConnection, url=SUPABASE_URL, key=SUPABASE_KEY)

# Pythonクライエントを取得
supabase = conn.client

# クイズデータ取得メソッド
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

# 出題メソッド
def show_quiz():
    # クイズデータの各要素を取得
    dragon_normal = quiz['dragon_normal']
    dragon_normal_url = f"{PAI_URL}{dragon_normal}{PNG}"

    your_wind = quiz['your_wind']
    your_wind_url = f"{PAI_URL}{your_wind}{PNG}"

    table_wind = quiz['table_wind']
    table_wind_url = f"{PAI_URL}{table_wind}{PNG}"

    hand = [tile.strip() for tile in quiz['hand'].split(",")]
    hand_tile_url = [f"{PAI_URL}{tile}{PNG}" for tile in hand]

    zimo = quiz['zimo']
    zimo_tile_url = f"{PAI_URL}{zimo}{PNG}"

    # 自風、場風、ドラを表示
    st.write("自風: ")
    st.image(your_wind_url, width=PAI_WIDTH)

    st.write("場風: ")
    st.image(table_wind_url, width=PAI_WIDTH)

    st.write(f"ドラ: ")
    st.image(dragon_normal_url, width=PAI_WIDTH)

    # 手牌を表示
    st.write("手牌: ")

    # 手牌を表示する列を生成
    hand_columns = st.columns(len(hand))
    for url in hand_tile_url: 
        hand_html += f"<img src='{url}' width='{PATH_WIDTH}'>"
        st.markdown(hand_html, unsafe_allow_html=True)
        
        # 各列に牌の画像を配置
        with hand_columns[i]: 
            st.image(url, width=PAI_WIDTH)
            
    # ツモを表示
    st.write("ツモ: ")
    st.image(zimo_tile_url, width=PAI_WIDTH)

    return

# 回答表示メソッド
def show_answer():
    # 回答データの各要素を取得
    correct_tile = quiz['correct_tile']
    correct_tile_url = f"{PAI_URL}{correct_tile}{PNG}"
    explanation = quiz['explanation']

    st.write("正解: ")
    st.image(correct_tile_url, width=PAI_WIDTH)
    st.write(f"解説: {explanation}")

    return


# アプリケーションのメイン
st.title("Nanikiru?")

# クイズデータのオブジェクト生成
quiz = fetch_quiz()

# クイズデータが取得できた場合
if quiz: 
    show_quiz()
    
    # 回答表示ボタンが押された場合
    if st.button(SHOW_ANSWER_BUTTON): 
        show_answer()

