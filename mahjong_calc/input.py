'''
Created on 2024/12/01

@author: kotaro
'''
import mahjong

import streamlit as st
from _ast import Div

# ページ名
st.set_page_config(
    page_title = "Nanikiru")

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

