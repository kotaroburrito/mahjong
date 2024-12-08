'''
Created on 2024/12/01

@author: kotaro
'''

import streamlit as st
import requests
import os
import random
from supabase import create_client, Client

# Supabaseとの接続情報
SUPABASE_URL = os.getenv("STREAMLIT_SUPABASE_URL")
SUPABASE_KEY = os.getenv("STREAMLIT_SUPABASE_KEY")

# 牌画像
TILE_BAI = os.getenv("BAI_URL")
TILE_FA = os.getenv("FA_URL")
TILE_ZHONG = os.getenv("BAI_ZHONG")

tiles = [
    f"{TILE_BAI}", 
    f"{TILE_FA}", 
    f"{TILE_ZHONG}"
]

st.image(tiles, caption=["白", "發", "中"], width=80)

# アプリケーションのメイン
st.title("Nanikiru?")

# Superbaseからクイズデータを取得
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_quiz():
    response = supabase.table("nanikiru").select("*").execute()
    
    # レスポンスエラーのチェック
    if response.error: 
        st.error(f"クイズデータの取得に失敗しました: {response.error.message}")
        return None

    # レスポンスデータの有無チェック
    if response.data:
        # ランダムに1問選ぶ
        quiz_data = random.choice(response.data)
        return quiz_data
    
    else: 
        st.error("クイズデータの取得に失敗しました。")
        return None

# クイズデータのオブジェクト生成
quiz = fetch_quiz()

if quiz: 
    # 自風、場風、ドラを表示
    st.write(f"自風: {quiz['your_wind']}/ 場風: {quiz['table_wind']}")
    st.write(f"ドラ: {quiz['dragon_normal']}")

    # 手牌を表示
    st.write("手牌: ")
    hand_tiles = quiz["hand"].split(",") # 1カラム1牌にするならここは変える!
    for tile in hand_tiles: 
        tile_url = f"https://raw.githubusercontent.com/kotaroburrito/mahjong/master/images/{quiz['tile']}.PNG"
        st.image(title_url, width=50)

    # ツモを表示
    st.write("ツモ: ")
    zimo_tile_url = f"https://raw.githubusercontent.com/kotaroburrito/mahjong/master/images/{quiz['zimo']}.PNG"
    st.image(zimo_tile_url, width=50)

    # 答えを非表示にしておき、回答後に表示
    if st.button("答えを見る"): 
        correct_tile_url = f"https://raw.githubusercontent.com/kotaroburrito/mahjong/master/images/{quiz['correct_tile']}.PNG"
        st.write("正解: ")
        st.image(correct_tile_url, width=50)
        st.write(f"解説: {quiz['explanation']}")



