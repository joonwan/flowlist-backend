# Flow List

Flow List는 FastAPI 기반으로 만든 태스크 관리 백엔드 학습 프로젝트입니다.

![Flow List cover](assets/flowlist-cover.png)

이 저장소의 목표는 개별 예제를 따로 따라가는 대신, 하나의 애플리케이션을 직접 점진적으로 확장하면서 백엔드 개발을 익히는 것입니다. 프로젝트는 단순한 TODO API로 시작했지만, 현재는 영속성, 캐싱, 로컬 AI 연동까지 포함하는 백엔드로 발전한 상태입니다.

## 현재 구현된 내용

현재 프로젝트에는 다음 내용이 구현되어 있습니다.

- FastAPI 애플리케이션 기본 구성
- 라우터 기반 API 구조
- Task CRUD API
- MySQL + SQLAlchemy 연동
- schema, router, service, repository 계층 분리
- `.env` 기반 환경변수 설정
- Redis 기반 task 목록 캐싱
- Ollama 기반 로컬 LLM task breakdown 기능
- `pytest` 기반 기본 API 테스트

## 현재 기능

### Task API

- task 생성
- task 전체 조회
- task 단건 조회
- task 수정
- task 삭제

### Task 필드

현재 task는 아래 필드를 지원합니다.

- `title`
- `description`
- `priority`
- `due_date`
- `is_done`

### Validation

요청 데이터 검증은 Pydantic으로 처리합니다.

예를 들면:

- `title`은 빈 문자열일 수 없음
- `title`은 최대 길이 제한이 있음
- `priority`는 허용된 범위 안에서만 입력 가능

### Redis 캐시

Task 목록 조회는 Redis 캐시를 사용합니다.

- `GET /tasks` 호출 시 먼저 Redis를 확인함
- 캐시가 없으면 MySQL에서 조회 후 Redis에 저장함
- task 생성, 수정, 삭제 시 task 목록 캐시를 무효화함

### AI Task Breakdown

Flow List는 Ollama를 통해 로컬 LLM을 사용해서 하나의 task를 더 작은 실행 단위로 분해할 수 있습니다.

예시 엔드포인트:

- `POST /tasks/{task_id}/breakdown`

이 기능은 OpenAI-compatible client를 사용해 로컬 Ollama 서버를 호출하는 방식으로 구현되어 있습니다.

## 기술 스택

- FastAPI
- SQLAlchemy
- MySQL
- Redis
- Ollama
- OpenAI Python SDK (OpenAI-compatible local model 호출용)
- Pytest

## 프로젝트 구조

```text
app/
  core/
    config.py
  infrastructure/
    database.py
    redis_client.py
  models/
    task.py
  repositories/
    task_repository.py
  routers/
    tasks.py
  schemas/
    task.py
    task_ai.py
  services/
    task_service.py
    task_ai_service.py
  main.py
```

## 환경변수

프로젝트 루트에 `.env` 파일을 만들고 아래처럼 설정합니다.

예시:

```env
DATABASE_URL=mysql+pymysql://root:1234@localhost:3306/flowlist
REDIS_URL=redis://localhost:6379/0
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama3.1:8b
LLM_API_KEY=ollama
```

## 설치 방법

가상환경을 만들고 의존성을 설치합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 실행 방법

FastAPI 서버 실행:

```bash
uvicorn app.main:app --reload
```

접속 주소:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## 인프라 준비

### MySQL

실행 중인 MySQL 인스턴스와 `flowlist` 데이터베이스가 필요합니다.

### Redis

예시 Docker 실행 명령어:

```bash
docker run -d --name flowlist-redis -p 6379:6379 redis:7
```

### Ollama

예시 설치 및 실행 흐름:

```bash
ollama pull llama3.1:8b
ollama serve
```

## 테스트 실행

```bash
python -m pytest -v
```

## 지금까지 학습한 내용

이 프로젝트를 통해 현재까지 아래 내용을 다뤘습니다.

- FastAPI 기반 REST API 기초
- request/response schema 설계
- 데이터베이스 연동과 ORM 사용
- service / repository 계층 분리
- 환경변수 기반 설정 관리
- Redis 캐시 연동
- 로컬 AI 모델 연동

## 다음 단계

다음으로 확장할 수 있는 주제는 아래와 같습니다.

- 메시지 큐 연동
- 비동기 AI 워크플로우
- AI가 생성한 subtasks 저장
- 테스트 격리 강화
- 배포 및 문서 보강

## 개발 철학

Flow List는 의도적으로 손으로 직접 만드는 프로젝트입니다.

목적은 단순히 애플리케이션을 완성하는 것이 아니라, 백엔드 시스템이 어떻게 구성되는지, 책임이 어떻게 분리되는지, 그리고 여러 기술이 하나의 서비스 안에서 어떻게 함께 동작하는지를 이해하는 데 있습니다.
