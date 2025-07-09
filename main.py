import streamlit as st
import random
import time

st.title("🐎 200프레임 부드러운 경주마 달리기 시뮬레이션 🐎")

NUM_HORSES = 10
FINISH_LINE = 100
TOTAL_FRAMES = 200
horses = [f"말{i+1}" for i in range(NUM_HORSES)]

HORSE_IMG = "https://upload.wikimedia.org/wikipedia/commons/3/3a/Horse_icon.svg"
STUMBLE_IMG = "https://upload.wikimedia.org/wikipedia/commons/9/9b/Horse_silhouette_falling.svg"

def run_race(total_frames=TOTAL_FRAMES):
    positions = [0.0] * NUM_HORSES
    stunned = [0] * NUM_HORSES
    finished = [False] * NUM_HORSES
    ranks = []
    rank_count = 0
    
    frames = []
    
    for frame_num in range(total_frames):
        frame = []
        all_finished = all(finished)
        if all_finished:
            # 모두 완주했으면 남은 프레임은 현재 위치로 동일하게 저장
            for i in range(NUM_HORSES):
                status = "finish" if finished[i] else "running"
                frame.append((horses[i], positions[i], status))
            frames.append(frame)
            continue
        
        for i in range(NUM_HORSES):
            if finished[i]:
                frame.append((horses[i], positions[i], "finish"))
                continue
            
            if stunned[i] > 0:
                stunned[i] -= 1
                frame.append((horses[i], positions[i], "stumble"))
                continue
            
            # 속도를 0.0 ~ 1.0 까지 부드럽게 이동 (조금씩 움직임)
            speed = random.uniform(0.0, 1.0)
            
            # 3% 확률로 넘어짐 (좀 더 희박하게)
            if random.random() < 0.03:
                stunned[i] = 3  # 3프레임 동안 경직
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
    
    # 완주 못한 말도 위치 기준으로 순위 뒤에 매김
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
            <div style="position: relative; width: {max_width}px; height: 50px; margin-bottom: 5px; background: linear-gradient(to right, #f0f0f0 0%, #a0ffa0 100%); border-radius: 10px;">
                <span style="position: absolute; left: 0; top: 10px; font-weight: bold;">{horse}</span>
                <img src="{img_url}" style="position: absolute; left: {x_pos}px; top: 0; width: 40px; height: 40px;">
                <span style="position: absolute; right: 0; top: 10px; font-size: 12px;">결승선</span>
            </div>
            """, unsafe_allow_html=True
        )

if st.button("경주 시작 (200프레임 부드럽게)"):
    ranks, frames = run_race()
    
    race_placeholder = st.empty()
    for i, frame in enumerate(frames):
        race_placeholder.markdown(f"### 프레임 {i+1} / {TOTAL_FRAMES}")
        display_frame(frame)
        time.sleep(0.03)  # 30fps 느낌으로 부드럽게
        race_placeholder.empty()
    
    st.subheader("최종 순위")
    for rank, horse in ranks:
        st.write(f"{rank}위: {horse}")




