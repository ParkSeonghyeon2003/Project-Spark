## Software Requirements Specification (SRS)
**프로젝트명:** Blueprint AI (Project Spark)  
**기술 스택:** Python, LangGraph, Streamlit, LLM API (GPT/Gemini 등)

---

### 1. 프로젝트 개요 (Introduction)
* **목적:** 아이디어 단계에서 멈춰있는 초보 개발자들에게 구체적인 기술 설계, 개발 로드맵, 기초 코드를 제공하여 프로젝트 착수 문턱을 낮춤.
* **핵심 가치:** 의사결정 자동화, 표준화된 프로젝트 구조 학습, MVP 중심의 개발 습관 형성.

---

### 2. 시스템 아키텍처 (System Architecture)
에이전트 간의 협업은 **LangGraph**를 통해 상태 기반 그래프(State-based Graph)로 관리됩니다.



* **State:** 프로젝트 아이디어, 선정된 기술 스택, 기능 리스트, 파일 구조 등을 포함하는 공유 객체.
* **Nodes (Agents):** 각 전문가 페르소나를 가진 에이전트 노드.
* **Edges:** 에이전트 간의 조건부 전이 및 피드백 루프.

---

### 3. 기능 요구사항 (Functional Requirements)

#### **F1. 요구사항 분석 및 기능 정의 (PM Agent)**
* 사용자의 모호한 입력을 분석하여 핵심 기능(MVP)과 확장 기능을 구분함.
* 사용자에게 추가 질문을 던져 요구사항의 모호함을 해소(Human-in-the-loop).

#### **F2. 기술 스택 추천 (Architect Agent)**
* 프로젝트 성격에 맞는 프론트엔드, 백엔드, 데이터베이스 조합 추천.
* 추천 이유와 각 기술의 장단점을 초보자 눈높이에서 설명.

#### **F3. 청사진 및 가이드 생성 (Dev Agent)**
* `README.md`: 프로젝트 개요, 설치 방법, 사용법 포함.
* `requirements.txt` 또는 `pyproject.toml` 생성.
* 표준화된 폴더 구조(Folder Tree) 시각화 및 생성.

#### **F4. 단계별 로드맵 수립 (Coordinator Agent)**
* 개발 우선순위에 따른 단계별(Step-by-step) 구현 가이드라인 제공.
* 각 단계에서 참고할 만한 공식 문서 링크나 학습 키워드 포함.

#### **F5. 결과물 내보내기 (Export System)**
* 생성된 모든 문서와 구조를 `.zip` 형태나 개별 `.md` 파일로 로컬 다운로드 지원.

---

### 4. 사용자 인터페이스 (UI/UX) - Streamlit 구성
* **Sidebar:** API 키 설정, LLM 모델 선택, 프로젝트 히스토리 관리.
* **Main Canvas:** * **Chat Interface:** 에이전트와 대화하며 아이디어를 구체화하는 영역.
    * **Dashboard:** 현재 진행 중인 에이전트 작업 단계(Graph Visualization) 표시.
    * **Preview Pane:** 생성된 `README.md`나 폴더 구조를 실시간 렌더링하여 보여줌.

---

### 5. 비기능 요구사항 (Non-functional Requirements)
* **응답성:** LLM의 생성 시간이 길어질 수 있으므로 Streamlit의 `st.status` 등을 활용해 작업 진행 상황을 실시간으로 노출함.
* **확장성:** 새로운 에이전트(예: UI Designer, Tester)를 쉽게 추가할 수 있는 모듈형 그래프 설계.
* **안정성:** LLM API 호출 실패 시 재시도 로직 및 에러 메시지 처리.

---

### 6. 에이전트 워크플로우 상세 (LangGraph Logic)

| 단계 | 노드명 | 입력 | 출력 | 조건부 로직 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Analyze** | 유저 아이디어 | 기능 명세(JSON) | 정보 부족 시 유저에게 재질문 |
| 2 | **Design** | 기능 명세 | 기술 스택 & DB 설계 | - |
| 3 | **Generate** | 기술 스택 | 파일 구조 & 가이드 | - |
| 4 | **Review** | 전체 결과물 | 최종 승인/수정안 | 불만족 시 Design 단계로 회귀 |
