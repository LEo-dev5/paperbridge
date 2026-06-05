# 📚 PaperBridge

> LLM 시대의 Top-Down 학습자를 위한 AI 논문 브리핑 에이전트

## 만든 이유

요즘 많은 개발자들이 LLM을 활용해 코드를 먼저 짜고 이론을 나중에 채우는 **Top-Down 방식**으로 공부합니다.

저도 그런 사람 중 하나였습니다. SLAM, LiDAR, 컴퓨터비전 같은 분야에 관심이 생겼지만, 논문을 읽으려면 수학적 배경지식이 너무 많이 필요했습니다.

**PaperBridge는 이 간극을 메우기 위해 만들었습니다.**

논문을 못 읽는 사람도 최신 연구 흐름을 파악할 수 있도록, AI Agent가 논문을 대신 읽고 초등학생도 이해할 수 있는 언어로 설명해줍니다.

## 주요 기능

- 📬 **매일 자동 브리핑** → arXiv 최신 논문을 수집해 Discord로 요약 전송
- 💬 **대화형 질문** → 논문 내용에 대해 자유롭게 질문 가능
- 🔍 **RAG 기반 답변** → 실제 논문 내용을 근거로 Hallucination 방지
- ⚙️ **카테고리 설정** → 관심 분야를 자유롭게 변경 가능

## 기술 스택 및 선택 이유

| 기술 | 선택 이유 |
|---|---|
| **Claude API (Tool Use)** | Agent가 상황에 따라 도구를 스스로 선택하도록 구현 |
| **RAG + ChromaDB** | 논문 데이터 기반 정확한 답변, Hallucination 방지 |
| **arXiv API** | 유일한 무료 공식 논문 API |
| **Discord Webhook** | 배포 없이 실시간 모바일 알림 구현 |
| **APScheduler** | 매일 자동 브리핑을 위한 스케줄러 |
| **FastAPI** | 비동기 처리, 자동 API 문서화 |
| **PostgreSQL** | 배포 환경을 고려한 프로덕션 수준 DB |

## 아키텍처

```
arXiv API → 논문 수집 → PostgreSQL 저장
                      → ChromaDB 벡터화

사용자 질문 → Claude Agent
              → search_vectordb (RAG 검색)
              → search_papers (arXiv 검색)
              → get_paper_content (논문 상세)
              → 한국어 답변 생성

APScheduler → 매일 오전 9시
            → 논문 수집 + 요약
            → Discord 브리핑 전송
```

## 기술적 도전

**Agent 도구 우선순위 설계**
단순히 도구를 나열하는 것이 아니라, 시스템 프롬프트에 도구 사용 우선순위를 명시했습니다. ChromaDB를 먼저 검색하고, 결과가 없을 때만 arXiv API를 호출하도록 설계해 불필요한 외부 API 호출을 최소화했습니다.

**arXiv API Rate Limit 처리**
개발 중 arXiv API의 429 에러를 경험했습니다. `delay_seconds`, `num_retries` 설정과 예외처리를 추가해 안정적인 수집 파이프라인을 구축했습니다.

## 실행 방법

### 백엔드
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 프론트엔드
```bash
cd frontend
npm install
npm run dev
```

### 환경변수 설정
```bash
cp backend/.env.example backend/.env
# .env 파일에 API 키 입력
```

## 프로젝트 구조

```
paperbridge/
├── backend/
│   ├── app/
│   │   ├── agent/        # Claude Tool Use Agent
│   │   ├── tools/        # Agent 도구 함수들
│   │   ├── routers/      # API 엔드포인트
│   │   ├── services/     # 비즈니스 로직
│   │   ├── scheduler/    # 자동 브리핑 스케줄러
│   │   └── models/       # DB 스키마
└── frontend/
    └── src/
        ├── pages/        # 채팅, 브리핑, 설정
        └── services/     # API 호출
```