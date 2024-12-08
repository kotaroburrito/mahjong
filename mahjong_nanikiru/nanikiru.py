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

# 牌画像
# TILE_BAI = os.getenv("BAI_URL")
# TILE_FA = os.getenv("FA_URL")
# TILE_ZHONG = os.getenv("BAI_ZHONG")

# tiles = [
#     f"{TILE_BAI}", 
#     f"{TILE_FA}", 
#     f"{TILE_ZHONG}"
# ]

# アプリケーションのメイン
st.title("Nanikiru?")

# Superbaseからクイズデータを取得
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Supabase connection.
conn = st.connection(name="supabase", type=SupabaseConnection, url=SUPABASE_URL, key=SUPABASE_KEY)

# Pythonクライエントを取得
supabase = conn.client

st.write(dir(conn))

def fetch_quiz():
    try: 
        # Perform query.
        # response = conn.query("*", table="nanikiru", ttl="10m").execute()
        # response = conn.execute("SELECT * FROM nanikiru")
        response = supabase.table("nanikiru").select("*").execute()

        # response = supabase.table('nanikiru').select('*').execute()
        # response = supabase.table("nanikiru").select("id, dragon_normal, your_wind, table_wind, hand, zimo, correct_tile, explanation").execute()
        
        # debug用
        st.write("レスポンスの内容: ", response)
        st.write("レスポンスの種類: ", type(response))
        st.write("レスポンスのデータ: ", response.data)
        st.write("レスポンスの詳細:", response.__dict__)
        # ここまでdebug用
    
        # レスポンスデータがあるとき
        if response.get(data):
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
    for tile in hand_tiles: 
        hand_tile_url = f"https://raw.githubusercontent.com/kotaroburrito/mahjong/master/images/{tile}.PNG"
        st.image(hand_title_url, width=50)

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



