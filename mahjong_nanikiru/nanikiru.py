'''
Created on 2024/12/01

@author: kotaro
'''

import streamlit as st
import requests
import os
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
    if response.status_code == 200 and response.data:
        # ランダムに1問選ぶ
        quiz_data = random.choice(response.data)
        return quiz_data
    else: 
        st.error("クイズデータの取得に失敗しました。")
        return None

# クイズデータのオブジェクト生成
quiz = fetch_quiz()
if not quiz: 
    st.stop()

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














# セッション情報の初期化
if "page_id" not in st.session_state:
    st.session_state.page_id = "main"
    st.session_state.answers = []

# 最初のページ
def main():
    st.markdown(
        "<h1 style = 'text-align: center;> Nanikiru </h1>"
        )
    
    def change_page():
        st.session_state.answer.append(st.session_state.answer0)
        st.session_state.page_id = "page1"
        
    with st.form("f0"): 
        st.form_submit_button("Start", on_click = change_page)
        
# 問題1
def page1():
    st.markdown(
        "<h1 style='text-align: center;'>何切る?</h1>", 
        unsafe_allow_html = True,
        )
    
    def change_page():
        st.session_state.answer.append(st.session_state.answer1)
        st.session_state.page_id = "page2"
    
    with st.form("f1"): 
        st.radio("何切る?", ["A", "B", "C"], key = "answer1")
        st.form_submit_button("これ切る!", on_click = change_page)
        
def page_end():
    st.markdown(
        "<h2 style='text-align: center;'>あなたの回答は</h2>",
        unsafe_allow_html = True,
        )

    st.markdown(
        f"<div style='text-align: center;'>テーブル: {st.session_state.answer[0]}</div>",
        unsafe_allow_html = True,
        )
    
    for num, value in enumerate(st.session_state.answers, 0):
        if num != 0:
            st.markdown(
                f"<div style='text-lign: center;'> 第{num}問: {value}</div>", 
                unsafe_allow_html = True,
                )
            
    if st.session_state.page_id == "main": 
        main()
    
    if st.session_state.page_id == "page1":
        page1()
    
    if st.session_state.page_id == "page_end":
        page_end()


