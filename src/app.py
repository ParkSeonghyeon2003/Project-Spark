import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from service import load_graph

from dotenv import load_dotenv
import uuid
import os

# 파이썬의 표준 라이브러리(예: urllib, ssl)가 참조할 인증서 파일 경로를 설정합니다.
# 'r'은 Raw String으로, 역슬래시(\)를 경로 기호로 그대로 인식하게 합니다.
os.environ["SSL_CERT_FILE"] = r"C:\cert\cacert.pem"

# curl 기반의 라이브러리나 일부 하위 시스템이 참조할 인증서 묶음(Bundle) 경로를 설정합니다.
# 보안 네트워크(방화벽) 환경에서 인증서 오류를 해결하기 위해 자주 사용됩니다.
os.environ["CURL_CA_BUNDLE"] = r"C:\cert\cacert.pem"

load_dotenv()

st.set_page_config(page_title="Blueprint AI", layout="wide")
st.title("🚀 Blueprint AI: 프로젝트 스파크")

# 세션 상태 초기화 (메모리 유지용)
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())

# 사이드바 - 현재 프로젝트 상태 미리보기
with st.sidebar:
    st.header("📋 Project Blueprint")
    # 그래프 내부의 최신 State를 가져와서 보여줄 영역
    # (일단은 비워두고 채팅부터 연결하자)
    st.info("에이전트가 분석을 완료하면 여기에 설계도가 나타납니다.")

    st.write("현재 thread_id")
    st.code(st.session_state["thread_id"])

    if st.button("대화 초기화"):
        st.session_state["thread_id"] = str(uuid.uuid4())
        st.session_state["messages"] = []
        st.rerun()


# 그래프 로드 (캐싱 적용됨)
graph = load_graph()

# 채팅 인터페이스
for msg in st.session_state["messages"]:
    with st.chat_message(msg.type):
        st.markdown(msg.content)

if prompt := st.chat_input("어떤 프로젝트를 만들고 싶나요?"):
    # 유저 입력 출력
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # LangGraph 실행
    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    
    with st.chat_message("assistant"):
        with st.status("에이전트 팀이 협업 중입니다...", expanded=True) as status:
            # 스트리밍 모드로 실행하여 노드 변화 감지
            for event in graph.stream(
                {"messages": st.session_state.messages}, 
                config, 
                stream_mode="values"
            ):
                if "messages" in event:
                    # 마지막 메시지가 에이전트의 응답이면 상태 업데이트
                    last_msg = event["messages"][-1]
                    if isinstance(last_msg, AIMessage):
                        st.write(f"🔔 **{last_msg.name if hasattr(last_msg, 'name') else 'Agent'}** 작업 완료")
            
            status.update(label="설계 완료!", state="complete", expanded=False)

        # 최종 응답 출력
        final_state = graph.get_state(config).values
        if final_state.get("messages"):
            response = final_state["messages"][-1].content
            st.markdown(response)
            st.session_state.messages.append(AIMessage(content=response))