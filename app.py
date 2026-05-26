import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# 1. 설정
st.set_page_config(page_title="Hawkeye 전술 엔진", page_icon="🛰️")
SECRET_PASSWORD = "1234"  # 숫자 비밀번호 설정

# 2. API 키 로드
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 인증 로직
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pw = st.text_input("지휘관 인증 키를 입력하십시오", type="password")
    if st.button("인증"):
        if pw == SECRET_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("접근 거부")
    st.stop()

# 4. 분석 엔진
st.title("🛰️ Hawkeye 전술 대시보드")
uploaded_file = st.file_uploader("전보 이미지를 업로드하십시오", type=['jpg', 'jpeg', 'png'])

if uploaded_file and st.button("🚀 전술 엔진 강제 가동"):
    with st.spinner("DNA 분석 및 연산 중..."):
        try:
            image = Image.open(uploaded_file)
            # 재시도 루프 추가 (안정성 확보)
            for attempt in range(3):
                try:
                    response = model.generate_content([image, "이 전보를 분석하여 Delta_kill, tau, IPAR 비율, 최종 판정을 보고해라."])
                    st.write(response.text)
                    break
                except Exception as e:
                    time.sleep(2)
            else:
                st.error("서버 과부하: 잠시 후 다시 시도하십시오.")
        except Exception as e:
            st.error(f"분석 오류: {e}")
