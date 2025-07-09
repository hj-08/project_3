import streamlit as st
import random

st.title("🎮 게임 추천 프로그램")

# 5가지 장르와 각 장르별 인기 게임과 선호도 점수(예시)
games = {
    "FPS": [
        {"name": "Overwatch", "popularity": 90},
        {"name": "Valorant", "popularity": 85},
        {"name": "Call of Duty", "popularity": 80},
        {"name": "Counter-Strike", "popularity": 75},
        {"name": "Apex Legends", "popularity": 70},
    ],
    "스토리게임": [
        {"name": "The Last of Us", "popularity": 95},
        {"name": "God of War", "popularity": 90},
        {"name": "Red Dead Redemption", "popularity": 88},
        {"name": "Life is Strange", "popularity": 80},
        {"name": "Firewatch", "popularity": 70},
    ],
    "AOS": [
        {"name": "League of Legends", "popularity": 95},
        {"name": "Dota 2", "popularity": 90},
        {"name": "Smite", "popularity": 70},
        {"name": "Heroes of the Storm", "popularity": 65},
        {"name": "Mobile Legends", "popularity": 60},
    ],
    "RPG": [
        {"name": "The Witcher 3", "popularity": 95},
        {"name": "Skyrim", "popularity": 90},
        {"name": "Final Fantasy VII",





