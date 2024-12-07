'''
Created on 2024/12/01

@author: kotaro
'''
import mahjong

import streamlit as st

# 計算
from mahjong.hand_calculating.hand import HandCalculator

# 麻雀牌
from mahjong.tile import TilesConverter

# 役、オプションルール
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules

# 鳴き
from mahjong.meld import Meld

# 風
from mahjong.constants import EAST, SOUTH, WEST, NORTH

# Handcalculatorクラスのインスタンス生成
calculator = HandCalculator()

# 結果出力用
def print_hand_result(hand_result):

  # 翻数、符数
  print(hand_result.han, hand_result.fu)

  # 点数
  print(hand_result.cost['main'], hand_result.cost['additional'])

  # 役
  print(hand_result.yaku)

  # 符数の詳細
  for fu_item in hand_result.fu_details:
    print(fu_item)
  print('')

st.title("mahjong calc test")
