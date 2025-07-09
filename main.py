import streamlit as st
import random
import time

st.title("🐎 30프레임 경주마 달리기 시뮬레이션 🐎")

NUM_HORSES = 10
FINISH_LINE = 100
TOTAL_FRAMES = 30  # 총 30프레임 고정
horses = [f"말{i+1}" for i in range(NUM_HORSES)]

HORSE_IMG = "https://upload.wikimedia.org/wikipedia/commons/3/3a/Horse_icon.svg"
STUMBLE_IMG = "https://upload.wikimedia.org/wikipedia/commons/9/9b/Horse_silhouette_falling.svg"

def run_race(total_frames=TOTAL_FRAMES):
    positions = [0] * NUM_HORSES
    stunned = [0] * NUM_HORSES
    finished = [False] * NUM_HORSES
    ranks = []
    rank_count = 0
    
    frames = []
    
    for frame_num in range(total_frames):
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
                if horses[i] not in [h for r, h in ranks]:
                    rank_count += 1
                    ranks.append((rank_count, horses[i]))
            
            frame.append((horses[i], positions[i], "running"))
        frames.append(frame)
    
    # 프레임 끝나도 완주 안한 말 있으면 순위 뒤에 정렬
    not_finished = [(positions[i], horses[i]) for i in range(NUM_HORSES) if horses[i] not in [h for r,h in ranks]]
    not_finished.sort(key=lambda x: x[0], reverse=True)
    for pos, horse in not_finished:
        rank_count += 1
        ranks.append((rank_count, horse))
    
    return ranks, frames

def display_frame(frame):
    max_width = 800
    for horse, pos, status in frame:
        x_pos = int(pos / FINISH_LINE * max_width)
        img_url = STUMBLE_IMG if status == "stumble" else HORSE_IMG
        st.markdown(
            f"""
            <div style="position: relative; width: {max_width}px; height: 50px; margin-bottom: 5px; background: linear-gradient(to right, #e0e0e0 0%, #a0ffa0 100%); border-radius: 10px;">
                <span style="position: absolute; left: 0; top: 10px; font-weight: bold;">{horse}</span>
                <img src="{img_url}" style="position: absolute; left: {x_pos}px; top: 0; width: 40px; height: 40px;">
                <span style="position: absolute; right: 0; top: 10px; font-size: 12px;">결승선</span>
            </div>
            """, unsafe_allow_html=True
        )

if st.button("경주 시작 (30프레임)"):
    ranks, frames = run_race()
    
    race_placeholder = st.empty()
    for i, frame in enumerate(frames):
        race_placeholder.markdown(f"### 프레임 {i+1} / {TOTAL_FRAMES}")
        display_frame(frame)
        time.sleep(0.1)  # 30fps 이므로 1/30초 약 0.033초, 웹 환경 안정 위해 0.1초로 조정
        race_placeholder.empty()
    
    st.subheader("최종 순위")
    for rank, horse in ranks:


