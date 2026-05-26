import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Hawkeye", page_icon="🛰️")
SECRET_PASSWORD = "1234"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pw = st.text_input("지휘관 인증 키", type="password")
    if st.button("인증"):
        if pw == SECRET_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

st.title("🛰️ Hawkeye 전술 대시보드")
uploaded_file = st.file_uploader("전보 이미지 업로드", type=['jpg', 'jpeg', 'png'])

if uploaded_file and st.button("🚀 전술 엔진 강제 가동"):
    with st.spinner("최적화 연산 중..."):
        try:
            image = Image.open(uploaded_file)
            # 가장 가볍고 빠른 모델로 고정
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 딱 한 번만 정밀 분석 요청
            response = model.generate_content(
                ["이 전보를 분석하여 Delta_kill, tau, IPAR 비율, 최종 판정을 보고해라.", image]
            )
            st.markdown(response.text)
        except Exception as e:
            st.error("서버 호출 제한: 1분 뒤에 다시 시도하십시오.")
