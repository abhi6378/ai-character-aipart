# AI Character App — AI Services

This repository contains the **AI services layer** for a character-based AI companion app.

The product is **character-first**, not story-first. Users can chat 1:1 with predefined or user-created characters, return after days, and continue with proper memory, continuity, personality, and voice behavior.

The AI service is designed as a clean internal package that the backend can call. Backend owns API, auth, database persistence, and deployment. AI service owns prompt logic, memory logic, continuity logic, language handling, response parsing, LangChain calls, LangSmith tracing, and VoxCPM voice payload preparation.

---

## What This Repo Handles

The AI service is responsible for:

- character response generation
- prompt building
- memory selection and memory update proposals
- user-character continuity
- language / Hinglish handling
- raw LLM response parsing
- VoxCPM TTS payload preparation
- LangChain-based model calls
- LangSmith tracing support
- AI-backend contracts

The backend is responsible for:

- authentication
- API routes
- PostgreSQL models and migrations
- Redis / cache usage
- Cloud Storage / media persistence
- actual DB writes
- calling the AI orchestrator
- triggering real audio generation jobs

---

## Project Flow

```mermaid
flowchart TD
    User[User sends message from mobile app] --> Backend[Backend API]

    Backend --> Auth[Validate user and chat request]
    Backend --> DBLoad[Load required data from DB]
    DBLoad --> Character[Character version and inference config]
    DBLoad --> Persona[User persona]
    DBLoad --> Continuity[User-character continuity state]
    DBLoad --> Memory[Recent messages and memory items]
    DBLoad --> Voice[Character voice config]

    Character --> AI[AI Services Package]
    Persona --> AI
    Continuity --> AI
    Memory --> AI
    Voice --> AI

    AI --> Prompt[Prompt Builder]
    Prompt --> Chain[LangChain Character Response Chain]
    Chain --> LLM[OpenAI LLM]
    Chain --> LangSmith[LangSmith Trace]

    LLM --> Parser[Response Parser]
    Parser --> MemoryUpdate[Memory Update Proposals]
    Parser --> ContinuityUpdate[Continuity Update Proposal]
    Parser --> VoicePayload[VoxCPM Voice Payload]

    MemoryUpdate --> AIResponse[Structured AIChatResponse]
    ContinuityUpdate --> AIResponse
    VoicePayload --> AIResponse
    Parser --> AIResponse

    AIResponse --> Backend
    Backend --> SaveDB[Backend saves message, memory, state, and audio metadata]
    SaveDB --> Mobile[Mobile receives final chat response]
Main AI Runtime Flow

When backend calls the AI service, the flow is:

Backend creates AIChatRequest
AI service loads context through store interfaces
Prompt builder creates the final character prompt
LangChain calls the selected LLM
LangSmith tracks the run for debugging
Response parser cleans the raw model response
Memory service proposes memory updates
Continuity service proposes state updates
Voice service prepares VoxCPM TTS payload
Backend receives AIChatResponse and persists everything

Backend should call only the orchestrator:

response = await chat_orchestrator.process(ai_request)

Backend should not directly call prompt builder, memory selector, parser, or voice payload builder.

Current AI Package Structure
app/
└── ai_services/
    ├── orchestrators/
    ├── contracts/
    ├── ports/
    ├── chains/
    ├── prompts/
    ├── memory/
    ├── continuity/
    ├── language/
    ├── parser/
    ├── voice/
    ├── providers/
    ├── observability/
    ├── config/
    ├── evals/
    └── utils/
Design Principles
1. Modular Code

Each module has one responsibility.

prompts/ handles prompt building
chains/ handles LangChain execution wrappers
parser/ handles raw LLM response parsing
memory/ handles memory selection and update proposals
continuity/ handles user-character state continuity
language/ handles Hinglish/language processing
voice/ handles VoxCPM payload preparation
providers/ handles external integrations
contracts/ defines backend-facing request/response models
ports/ defines backend data access interfaces
2. No Hardcoding

Do not hardcode:

API keys
model names
prompt versions
temperature
max tokens
voice IDs
provider URLs
bucket names

Use config, environment variables, database fields, and prompt registry.

3. No Over-Engineering

Use abstraction only where useful:

LLM provider abstraction
TTS provider abstraction
storage provider abstraction
store ports for backend integration

Do not create deep inheritance trees for business logic.

4. Backend and AI Boundary

AI service returns proposals and payloads.

Backend performs persistence and infrastructure actions.

AI returns:

generated message
emotion
action text
memory update proposals
continuity update proposal
voice payload
trace metadata

Backend saves:

chat messages
memory items
continuity state
audio metadata
DB transactions
LangChain and LangSmith Usage

LangChain is used for:

character response chain
LLM provider integration
future structured output support

LangSmith is used for:

tracing
debugging
prompt review
model behavior tracking
token/latency visibility

We do not use autonomous agents in the main chat flow because our workflow is predictable.

Local Testing

Run all AI tests:

pytest tests/ai

Run a specific test file:

pytest tests/ai/unit/test_ai_contracts.py

Run the local mock demo:

python scripts/run_ai_demo_mock.py

Mock tests do not require:

OpenAI API key
LangSmith key
database
backend API
GCP credentials
VoxCPM GPU
Environment Setup

Copy .env.example to .env locally.

Never commit .env.

APP_ENV=local
OPENAI_API_KEY=
LLM_MODEL_NAME=gpt-4o-mini
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=ai-character-dev
VOXCPM_TTS_URL=
Git Workflow

We use:

main for stable production-ready code
dev for integration/testing
feature/* for new features
fix/* for bug fixes
hotfix/* for urgent fixes

Normal flow:

dev → feature branch → PR to dev → test → merge

Do not push directly to main.

Completed Phases
Phase 0: AI project skeleton
Phase 1: AI contracts
Phase 2: store ports and fake stores
Phase 3: prompt system
Phase 4: LangChain provider and LangSmith setup
Phase 5: response parser

Next phase:

Phase 6: memory service
