# AI Contract

This document defines how the backend will call the AI service.

## Backend Calls AI With

`AIChatRequest`

Required fields:
- `user_id`
- `character_id`
- `thread_id`
- `message`

Optional fields:
- `request_audio`
- `language_mode`
- `request_id`

## AI Service Returns

`AIChatResponse`

Fields:
- `display_text`
- `action_text`
- `emotion`
- `character_version_id`
- `memory_updates`
- `continuity_update`
- `voice_payload`
- `trace`

## Important Rule

Backend owns persistence.

AI service only returns:
- generated response
- memory update proposals
- continuity update proposal
- TTS payload

Backend decides how to save these in PostgreSQL and when to trigger audio generation.

## Why This Contract Exists

This contract lets AI and backend work in parallel.

AI developer can test with fake stores.
Backend developer can later implement real PostgreSQL repositories.
