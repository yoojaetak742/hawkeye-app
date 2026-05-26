import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hawkeye v52.3", page_icon="🛰️")

# API KEY는 나중에 Streamlit Cloud 설정에서 입력합니다.
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

SECRET_PASSWORD = "전술비밀번호123" 

def check_password():
    if "pw" not in st.session_state: st.session_state.pw = False
    if not st.session_state.pw:
        st.title("🛰️ Hawkeye 보안 구역")
        p = st.text_input("지휘관 인증 키:", type="password")
        if st.button("인증"):
            if p == SECRET_PASSWORD:
                st.session_state.pw = True
                st.rerun()
            else: st.error("❌ 접근 거부")
        return False
    return True

if check_password():
    st.title("🛰️ Hawkeye 전술 대시보드")
    uploaded_file = st.file_uploader("전보 이미지 업로드", type=["jpg", "png"])
    if uploaded_file and st.button("🚀 전술 엔진 강제 가동"):
        with st.spinner('DNA Scan 및 연산 중...'):
            image_data = uploaded_file.getvalue()
            response = model.generate_content(["이미지에서 아군/적군 스탯 추출하고 킬델타 및 파상 비율 계산해", {"mime_type": "image/jpeg", "data": image_data}])
            st.success("연산 완료")
            st.markdown(response.text)
