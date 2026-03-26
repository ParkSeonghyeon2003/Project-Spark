import streamlit as st
import uuid
from langchain_core.messages import HumanMessage
from service import load_graph, create_project_zip, run_agent_workflow
from config import settings

def init_session():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = str(uuid.uuid4())
    if "final_state" not in st.session_state:
        st.session_state["final_state"] = None

def render_sidebar():
    with st.sidebar:
        st.header("📋 Project Blueprint")
        st.info("에이전트가 분석을 완료하면 여기에 설계도가 나타납니다.")
        st.write("현재 세션")
        st.code(st.session_state["thread_id"])

        if st.button("대화 초기화", use_container_width=True):
            st.session_state["thread_id"] = str(uuid.uuid4())
            st.session_state["messages"] = []
            st.rerun()

def render_chat_interface(graph):
    for msg in st.session_state["messages"]:
        with st.chat_message(msg.type):
            st.markdown(msg.content)

    if prompt := st.chat_input("어떤 프로젝트를 만들고 싶나요?"):
        # 사용자 입력단
        user_msg = HumanMessage(content=prompt)
        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            st.markdown(prompt)


        config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

        agent_names = {
            "pm_agent": "📋 요구사항 분석",
            "architect_agent": "🏗️ 기술 스택 설계",
            "developer_agent": "🛠️ 코드 생성",
            "coordinator_agent": "✅ 최종 검토"
        }

        with st.chat_message("assistant"):
            with st.status("에이전트 팀이 협업 중입니다...", expanded=True) as status:
                for agent_msg in run_agent_workflow(graph, st.session_state.messages, config):
                    display_name = agent_names.get(agent_msg.name, agent_msg.name)
                    with st.status(f"🔔 **{display_name}** 완료", expanded=False):
                        st.markdown(agent_msg.content)
                final_state = graph.get_state(config).values
                st.session_state["final_state"] = final_state
                status.update(label="✨ 모든 설계가 완료되었습니다!", state="complete", expanded=False)

            if st.session_state.messages:
                st.markdown(st.session_state.messages[-1].content)

    if st.session_state.final_state:
        render_download_section(st.session_state.final_state)

def render_download_section(state):
    if state.get("file_structure"):
        zip_data = create_project_zip(state["file_structure"].file_structure)
        project_name = getattr(state["requirements"], 'project_name', 'project')

        st.download_button(
            label="🎁 프로젝트 다운로드 (.zip)",
            data=zip_data,
            file_name=f"{project_name}.zip",
            mime="application/zip",
            use_container_width=True
        )


def main():
    st.set_page_config(page_title="Blueprint AI", layout="wide")
    st.title("🚀 Blueprint AI: 프로젝트 스파크")

    # SSL 설정
    settings.setup_ssl()

    init_session()
    graph = load_graph()
    render_sidebar()
    render_chat_interface(graph)


if __name__ == "__main__":
    main()