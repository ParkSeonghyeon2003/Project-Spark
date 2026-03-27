import streamlit as st
import uuid
from langchain_core.messages import AIMessage, HumanMessage
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

        if st.session_state.final_state:
            req = st.session_state.final_state.get("requirements")
            p_name = getattr(req, "project_name", "분석 완료!")
            st.success(f"**프로젝트 명:** {p_name}")
        else:
            st.info("에이전트가 분석을 완료하면 여기에 설계도가 나타납니다.")

        st.write("---")
        st.caption(f"Session ID: {st.session_state["thread_id"]}")

        if st.button("대화 초기화", use_container_width=True):
            st.session_state["thread_id"] = str(uuid.uuid4())
            st.session_state["messages"] = []
            st.session_state["final_state"] = None
            st.rerun()

def render_chat_interface(graph):
    agent_names = {
        "pm_agent": "📋 요구사항 분석",
        "architect_agent": "🏗️ 기술 스택 설계",
        "developer_agent": "🛠️ 코드 생성",
        "coordinator_agent": "✅ 최종 검토"
    }

    for msg in st.session_state["messages"]:
        # 에이전트 중간 로그인지 확인 (metadata 활용)
        if isinstance(msg, AIMessage) and "is_agent_log" in msg.additional_kwargs:
            with st.expander(f"🔔 {msg.additional_kwargs.get('agent_display_name')} 완료", expanded=False):
                st.markdown(msg.content)
        else:
            with st.chat_message(msg.type):
                st.markdown(msg.content)

    if prompt := st.chat_input("어떤 프로젝트를 만들고 싶나요?"):
        # 사용자 입력단
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)


        config = {"configurable": {"thread_id": st.session_state["thread_id"]}}


        with st.chat_message("assistant"):
            with st.status("에이전트 팀이 협업 중입니다...", expanded=True) as status:
                try:
                    for agent_msg in run_agent_workflow(graph, st.session_state.messages, config):
                        display_name = agent_names.get(agent_msg.name, agent_msg.name)
                        log_msg = AIMessage(
                            content=agent_msg.content,
                            additional_kwargs={
                                "is_agent_log": True,
                                "agent_display_name": display_name
                            }
                        )
                        st.session_state.messages.append(log_msg)

                        with st.status(f"🔔 **{display_name}** 완료", expanded=True):
                            st.markdown(agent_msg.content)

                    final_state = graph.get_state(config).values
                    st.session_state["final_state"] = final_state

                    final_content = final_state["messages"][-1].content
                    final_ai_msg = AIMessage(content=final_content)
                    st.session_state.messages.append(final_ai_msg)

                    status.update(label="✨ 모든 설계가 완료되었습니다!", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    status.update(label="❌ 오류가 발생했습니다.", state="error")
                    st.error(f"Error: {e}")

    if st.session_state.final_state:
        render_download_section(st.session_state.final_state)

def render_download_section(state):
    if state.get("file_structure"):
        st.divider()
        st.subheader("📦 생성된 프로젝트 파일")
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