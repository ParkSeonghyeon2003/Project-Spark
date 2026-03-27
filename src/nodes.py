from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from agent_state import AgentState
from schema import PMOutput, ArchitectOutput, DeveloperOutput, CoordinatorOutput
from factory import get_llm
import prompts


# PM 에이전트 (분석 노드)
def pm_node(state: AgentState):
    print("[PM Agent] 요구 사항 분석 중...")

    llm = get_llm(PMOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompts.PM_SYSTEM_PROMPT),
        ("placeholder", "{messages}")
    ])

    # 체인 + invoke
    chain = prompt | llm
    result = chain.invoke(state)

    if not result:
        raise ValueError("requiremets 분석을 실패")

    # 충족 체크
    if isinstance(result, PMOutput):
        content = (
            f"'✅ {result.project_name}' 프로젝트 분석 완료!\n"
            f"- MVP 기능 제안: {', '.join(result.mvp_features)}\n"
            f"- 추가 기능 제안: {', '.join(result.ext_features)}"
            if result.is_info_sufficient else "❓ 정보가 부족합니다. 추가적으로 자세한 정보를 입력해주세요."
        )

    print("[PM Agent] 요구 사항 분석 완료.")

    # 분석 내용 업데이트
    return {
        "requirements": result, # LangGraph가 알아서 dict 처리
        "messages": [AIMessage(content=content, name="pm_agent")]
    }


# Architect 에이전트 (디자인 노드)
def architect_node(state: AgentState):
    print("[Architect Agent] 기술 스택 설계 중...")

    llm = get_llm(ArchitectOutput)

    reqs = state["requirements"]

    if not reqs:
        return {"messages": [AIMessage(content="requirements 데이터가 없습니다.")]}

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompts.ARCHITECT_SYSTEM_PROMPT),
        ("human", prompts.ARCHITECT_HUMAN_PROMPT)
    ])

    # 체인 + invoke
    chain = prompt | llm
    result = chain.invoke({
        "project_name": reqs.project_name,
        "mvp_features": reqs.mvp_features,
        "ext_features": reqs.ext_features,
        "feedback": state.get("feedback", "없음")
    })

    # 충족 체크
    if isinstance(result, ArchitectOutput):
        content = f"### 🏗️ 설계된 기술 스택\n- **기술 스택**: {result.stacks}\n- **💡 추천 이유:** {result.reasoning}"

    print("[Architect Agent] 기술 스택 설계 완료.")

    return {
        "tech_stack": result,
        "messages": [AIMessage(content=content, name="architect_agent")]
    }


# Developer 에이전트 (생성 노드)
def developer_node(state: AgentState):
    print("[Dev Agent] 코드 및 구조 생성 중...")

    llm = get_llm(DeveloperOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompts.DEVELOPER_SYSTEM_PROMPT),
        ("human", prompts.DEVELOPER_HUMAN_PROMPT)
    ])

    chain = prompt | llm
    result = chain.invoke(state)

    if isinstance(result, DeveloperOutput):
        files_list = "\n".join([f"- {f.path}" for f in result.file_structure])
        content = f"### 🛠️ 프로젝트 뼈대 생성 완료!\n\n" \
                f"**생성된 파일 목록:**\n" \
                f"{files_list}\n\n" \
                f"**💡 가이드:** {result.explanation}\n\n" \
                f"**프로젝트 구조 트리:**\n\n" \
                f"```bash\n{result.tree}\n```"

    print("[Dev Agent] 코드 및 구조 생성 완료.")

    return {
        "file_structure": result,
        "messages": [AIMessage(content=content, name="developer_agent")]
        
    }


# Coordinator 에이전트 (리뷰 노드)
def coordinator_node(state: AgentState):
    print("[Coordinator Agent] 결과물 검토 중...")

    llm = get_llm(CoordinatorOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompts.COORDINATOR_SYSTEM_PROMPT),
        ("human", prompts.COORDINATOR_HUMAN_PROMPT)
    ])

    chain = prompt | llm
    result = chain.invoke(state)

    if isinstance(result, CoordinatorOutput):
        icon = "✅" if result.is_approved else "❌"
        content = f"### {icon} 최종 검토 결과\n\n{result.feedback}"

    print("[Coordinator Agent] 결과물 검토 완료.")

    return {
        "is_approved": result.is_approved,
        "feedback": result.feedback,
        "messages": [AIMessage(content=content, name="coordinator_agent")]
    }