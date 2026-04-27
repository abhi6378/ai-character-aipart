# AI Services Package

This package contains the AI development layer for the character-based AI companion app.

## Responsibility

The AI service is responsible for:
- character response generation
- prompt building
- memory selection and update proposals
- user-character continuity
- language detection and Hinglish handling
- response parsing
- VoxCPM TTS payload preparation
- LangChain and LangSmith integration

## Important Boundary

Backend owns:
- authentication
- API routes
- database models
- database migrations
- persistence
- cloud deployment

AI service owns:
- AI orchestration
- prompt logic
- LLM provider integration
- memory logic
- continuity logic
- language logic
- voice payload logic

Backend should call the AI service through the orchestrator only.
