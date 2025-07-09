import streamlit as st
import random
import time

st.title("경주마 10마리 달리기 & 페널티 효과 시뮬레이션")

NUM_HORSES = 10
FINISH_LINE = 100  # 결승선 거리
horses = [f"말{i+1}" for i in range(NUM_HORSES)]

def run_race():
    positions = [0] * NUM_HORSES
    finished = [False] * NUM_HORSES
    rank_list = []
    rank_count = 0
    
    # 경직 여부 저장 (턴 수)
    stunned = [0] * NUM_HORSES
    
    race_log = []
    
    while rank_count < NUM_HORSES:
        for i in range(NUM_HORSES):
            if finished[i]:
                continue
            
            # 경직 중이면 이동 못함, 경직 시간 1턴으로 처리
            if stunned[i] > 0:
                stunned[i] -= 1
                continue
            
            # 속도 1~10 랜덤
            speed = random.randint(1, 10)
            
            # 10% 확률로 돌에 걸림 (경직 발생)
            if random.random() < 0.1:
                stunned[i] = 1
                st.text(f"{horses[i]}가 돌에 걸려 넘어졌어요! 1초 경직 발생!")
                # 경직이라 이번 턴 이동 없음
                continue
            
            positions[i] += speed
            if positions[i] >= FINISH_LINE:
                positions[i] = FINISH_LINE
                finished[i] = True
                rank_count += 1
                rank_list.append((rank_count, horses[i]))
        
        race_log.append(list(positions))
        
        time.sleep(0.3)  # 잠시 대기
    
    return rank_list, race_log

if st.button("경주 시작"):
    ranks, logs = run_race()
    
    st.subheader("최종 순위")
    for rank, horse in ranks:
        st.write(f"{rank}위: {horse}")
    
    st.subheader("레이스 진행 상황")
    for i, pos in enumerate(logs):
        st.write(f"턴 {i+1}:")
        for h, p in zip(horses, pos):
            bar = "🐎" * (p // 5)
            st.write(f"{h}: {bar} ({p})")
        st.write("---")
