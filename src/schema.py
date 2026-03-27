from pydantic import BaseModel, Field
from enum import Enum

type FeatureList = list[str]

class NodeName(str, Enum):
    PM = "pm"
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    COORDINATOR = "coordinator"

class Route(str, Enum):
    CONTINUE = "continue"
    ASK_MORE = "ask_more"
    END = "end"
    RE_ARCHITECT = "re-architect"


class PMOutput(BaseModel):
    project_name: str = Field(description="프로젝트 이름")
    mvp_features: FeatureList = Field(description="핵심 기능 리스트", default_factory=list)
    ext_features: FeatureList = Field(description="추후 구현할 확장 기능 리스트", default_factory=list)
    is_info_sufficient: bool = Field(description="정보가 충분하면 True, 질문이 더 필요하면 False", default=False)


class ArchitectOutput(BaseModel):
    stacks: list[str] = Field(description="추천하는 기술 스택", min_length=1)
    reasoning: str = Field(description="이 스택들을 추천하는 이유")


class FileItem(BaseModel):
    path: str = Field(description="파일명(경로 포함)")
    content: str = Field(description="파일 내용")
class DeveloperOutput(BaseModel):
    file_structure: list[FileItem] = Field(
        description="생성된 파일들의 리스트"
    )
    explanation: str = Field(description="생성된 프로젝트 구조에 대한 간단한 설명")
    tree: str = Field(description="ascii 문자로 표현된 프로젝트 구조 트리")


class CoordinatorOutput(BaseModel):
    is_approved: bool = Field(description="모든 결과물이 요구사항을 충족하고 일관성이 있으면 True, 아니면 False")
    feedback: str = Field(description="승인 시 결과 요약, 거절 시 구체적인 수정 요청 사항")