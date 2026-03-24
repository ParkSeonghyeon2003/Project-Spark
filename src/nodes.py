from agent_state import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class RequirementsOutput(BaseModel):
    project_name: str = Field(description="프로젝트 이름")
    mvp_features: list[str] = Field(description="핵심 기능 리스트")
    is_info_sufficient: bool = Field(description="정보가 충분하면 True, 질문이 더 필요하면 False")

def analyze_node(state: AgentState):
    print("[PM Agent] 요구 사항 분석 중...")

    llm = ChatOpenAI(model="gpt-4.1-nano").with_structured_output(RequirementsOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 IT 프로젝트 기획 전문가입니다. 주어진 아이디어를 분석해서 MVP 기능을 도출해주세요."),
        ("placeholder", "{messages}")
    ])

    chain = prompt | llm
    result = chain.invoke(state)

    print("[PM Agent] 요구 사항 분석 완료.")
    
    # 분석 내용 업데이트
    return {"requirements": result.dict()}

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