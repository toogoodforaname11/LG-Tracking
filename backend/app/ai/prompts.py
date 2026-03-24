"""Gemini prompts for matching and summarization."""

MATCH_PROMPT = """You are a BC local government hearing analyst. Your job is to determine if a municipal document is relevant to a user's tracking preferences.

USER TRACK:
- Municipalities: {municipalities}
- Topics of interest: {topics}
- Keywords: {keywords}

DOCUMENT:
- Municipality: {document_municipality}
- Type: {document_type} (agenda/minutes/video)
- Title: {document_title}
- Date: {document_date}
- Content excerpt (first 2000 chars):
{content_excerpt}

TASK: Determine if this document is relevant to the user's track.

Respond in JSON format:
{{
  "is_match": true/false,
  "confidence": 0.0-1.0,
  "matched_topics": ["topic1", "topic2"],
  "matched_keywords": ["keyword1"],
  "reason": "Brief explanation of why this matches or doesn't match"
}}

Be generous with matching — if a document MIGHT be relevant, mark it as a match with lower confidence. Only reject clearly irrelevant items."""

SUMMARY_PROMPT = """You are a BC local government hearing analyst creating a concise briefing.

CONTEXT:
- Municipality: {municipality}
- Meeting type: {meeting_type}
- Meeting date: {meeting_date}
- Document type: {document_type}
- User is tracking: {topics} with keywords: {keywords}

DOCUMENT CONTENT:
{content}

TASK: Create a focused summary for someone tracking the specified topics. Include:

1. **Key Points** (3-5 bullet points of the most relevant items)
2. **Status** (what stage is this at — upcoming hearing, decision made, deferred, etc.)
3. **Action Items** (any deadlines, next steps, or dates to note)
4. **Relevant Excerpts** (brief quotes or references to specific agenda items)

Keep the summary under 500 words. Focus on the topics and keywords the user is tracking.
If this is an agenda, note what items are scheduled and when.
If this is minutes, note what decisions were made.
If this is a video description, note key timestamps if available.

IMPORTANT: Add this disclaimer at the end:
"⚠️ AI-generated summary — verify all details with the original document."

Respond in JSON:
{{
  "summary": "...",
  "key_points": ["point1", "point2", ...],
  "status": "upcoming/in_progress/decided/deferred",
  "action_items": ["item1", ...],
  "relevant_excerpts": ["excerpt1", ...],
  "next_dates": ["YYYY-MM-DD description", ...]
}}"""

EMBED_PROMPT = """Summarize this BC municipal government document for semantic search indexing.
Focus on: municipality name, meeting type, date, topics discussed, decisions made, key people mentioned.

Document: {content}

Output a single dense paragraph optimized for embedding-based retrieval."""
