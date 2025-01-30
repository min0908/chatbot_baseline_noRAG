import os
import streamlit as st
from dotenv import load_dotenv
from setup.st_function import print_messages, add_message
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# API key불러오기
load_dotenv()


# 캐시 디렉토리 생성
if not os.path.exists(".cache"):
    os.mkdir(".cache")  # . 은 숨김폴더처리

# 현재 페이지 이름 설정
current_page = "Chatbot_Baseline_NoRAG"

# 상태 초기화 로직
if "current_page" not in st.session_state:
    st.session_state["current_page"] = current_page

if st.session_state["current_page"] != current_page:
    # 페이지 변경 시 모든 상태 초기화
    st.session_state.clear()
    st.session_state["current_page"] = current_page

# title
st.title("챗봇상담 💬")


if "messages" not in st.session_state:
    # 대화내용을 저장
    st.session_state["messages"] = []

# 이전 대화 내용 기억
if "store" not in st.session_state:
    st.session_state["store"] = {}

# 사이드 바 생성
with st.sidebar:
    # 초기화버튼 생성
    clear_btn = st.button("대화내용 초기화")


# 초기화버튼
if clear_btn:
    st.session_state["messages"] = []

# 이전 대화 출력
print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요.")

# 경고 메세지를 띄우기 위한 빈 영역
warning_msg = st.empty()

# 사용자 입력
if user_input:
    st.chat_message("user").write(user_input)

    try:
        # ChatOpenAI 모델 생성
        chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

        # 사용자 입력을 HumanMessage 객체로 변환
        messages = [HumanMessage(content=user_input)]

        # GPT 모델 응답 받기
        ai_answer = chat(messages)

        # 응답 출력
        with st.chat_message("assistant"):
            st.markdown(ai_answer.content)

        # 대화기록 저장
        add_message("user", user_input)
        add_message("assistant", ai_answer.content)

    except Exception as e:
        warning_msg.error(f"오류가 발생했습니다: {str(e)}")

    
