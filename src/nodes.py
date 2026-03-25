from agent_state import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage

class RequirementsOutput(BaseModel):
    project_name: str = Field(description="프로젝트 이름")
    mvp_features: list[str] = Field(description="핵심 기능 리스트")
    is_info_sufficient: bool = Field(description="정보가 충분하면 True, 질문이 더 필요하면 False")

def analyze_node(state: AgentState):
    print("[PM Agent] 요구 사항 분석 중...")

    llm = ChatOpenAI(model="gpt-4.1-nano").with_structured_output(RequirementsOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
[역할]
너는 초보 개발자를 위한 'MVP 기획 전문가'이자 '요구사항 분석가'이다.

[목표]
사용자의 추상적인 아이디어를 분석하여 핵심 기능(MVP)과 나중에 구현할 확장 기능을 구분하고, 프로젝트의 범위를 확정한다.

[작업 지침]
1. 아이디어가 너무 모호하면(예: "게임 만들고 싶어") 구체적인 장르나 핵심 기능을 정중하게 되묻는다.
2. 기술적으로 실현 불가능하거나 초보자가 하기 너무 어려운 범위는 적절히 쳐내고 MVP 중심으로 제안한다.
"""),
        ("placeholder", "{messages}")
    ])

    chain = prompt | llm
    result = chain.invoke(state)

    if isinstance(result, RequirementsOutput):
        content = f"'{result.project_name}' 프로젝트 분석을 완료했습니다! 다음 기능을 MVP로 제안합니다: {', '.join(result.mvp_features)}" \
                  if result.is_info_sufficient else "아이디어가 멋지네요! 더 구체적인 설계를 위해 몇 가지 질문을 드려도 될까요?"
        ai_msg = AIMessage(content=content)

    print("[PM Agent] 요구 사항 분석 완료.")
    # 분석 내용 업데이트
    return {"requirements": result.dict(),
            "messages": [ai_msg]}

def design_node(state: AgentState):
    print("[Architect Agent] 기술 스택 설계 중...")

    print("[Architect Agent] 기술 스택 설계 완료.")
    return {"tech_stack": {"backend": "fastapi"}}

def generate_node(state: AgentState):
    print("[Dev Agent] 코드 및 구조 생성 중...")

    print("[Dev Agent] 코드 및 구조 생성 완료.")
    return {"file_structure": {"main.py": "print('hello world')"}}

def review_node(state: AgentState):
    print("[Coordinator Agent] 결과물 검토 중...")

    print("[Coordinator Agent] 결과물 검토 완료.")
    return {"is_approved": True}