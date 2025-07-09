import streamlit as st
import random
import time

st.title("🐎 경주마 10마리 달리기 시뮬레이션 with 이미지 🐎")

NUM_HORSES = 10
FINISH_LINE = 100

# 말 이름
horses = [f"말{i+1}" for i in range(NUM_HORSES)]

# 말 이미지 URL (달리는 말 아이콘 또는 GIF)
HORSE_IMG = "https://upload.wikimedia.org/wikipedia/commons/3/3a/Horse_icon.svg"  # 심플 아이콘 예시
# 넘어짐 이미지 URL (말 넘어짐 아이콘)
STUMBLE_IMG = "https://upload.wikimedia.org/wikipedia/commons/9/9b/Horse_silhouette_falling.svg"  # 예시 이미지 (말 넘어지는 실루엣)

def run_race():
    positions = [0] * NUM_HORSES
    finished = [False] * NUM_HORSES
    rank_list = []
    rank_count = 0
    stunned = [0] * NUM_HORSES
    
    race_log = []
    
    while rank_count < NUM_HORSES:
        frame = []
        for i in range(NUM_HORSES):
            if finished[i]:
                frame.append((horses[i], positions[i], "finish"))
                continue
            
            if stunned[i] > 0:
                stunned[i] -= 1
                frame.append((horses[i], positions[i], "stumble"))
                continue
            
            speed = random.randint(1, 10)
            
            if random.random() < 0.1:
                stunned[i] = 1
                frame.append((horses[i], positions[i], "stumble"))
                continue
            
            positions[i] += speed
            if positions[i] >= FINISH_LINE:
                positions[i] = FINISH_LINE
                finished[i] = True
                rank_count += 1
                rank_list.append((rank_count, horses[i]))
            
            frame.append((horses[i], positions[i], "running"))
        
        race_log.append(frame)
        time.sleep(0.3)
    
    return rank_list, race_log

def display_frame(frame):
    # 가로 최대 길이 설정 (픽셀)
    max_width = 800
    finish_px = max_width
    
    for horse, pos, status in frame:
        # 위치를 픽셀로 변환 (pos / FINISH_LINE * max_width)
        x_pos = int(pos / FINISH_LINE * max_width)
        
        # 말 상태에 따라 이미지 선택
        if status == "stumble":
            img_url = STUMBLE_IMG
        else:
            img_url = HORSE_IMG
        
        # 말 이름, 이미지, 위치 출력 (HTML + CSS로 좌우 위치 조절)
        st.markdown(
            f"""
            <div style="position: relative; width: {finish_px}px; height: 50px; margin-bottom: 5px; background: linear-gradient(to right, #e0e0e0 0%, #a0ffa0 100%); border-radius: 10px;">
                <span style="position: absolute; left: 0; top: 10px; font-weight: bold;">{horse}</span>
                <img src="{img_url}" style="position: absolute; left: {x_pos}px; top: 0; width: 40px; height: 40px;">
                <span style="position: absolute; right: 0; top: 10px; font-size: 12px;">결승선</span>
            </div>
            """, unsafe_allow_html=True
        )

if st.button("경주 시작"):
    ranks, logs = run_race()
    
    st.subheader("레이스 진행 상황")
    for i, frame in enumerate(logs):
        st.write(f"턴 {i+1}")
        display_frame(frame)
        st.write("---")
    
    st.subheader("최종 순위")
    for rank, horse in ranks:
        st.write(f"{rank}위: {horse}")

