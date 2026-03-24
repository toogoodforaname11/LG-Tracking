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

{video_timestamps_section}

TASK: Create a focused summary for someone tracking the specified topics. Include:

1. **Key Points** (3-5 bullet points of the most relevant items)
2. **Status** (what stage is this at — upcoming hearing, decision made, deferred, etc.)
3. **Action Items** (any deadlines, next steps, or dates to note)
4. **Relevant Excerpts** (brief quotes or references to specific agenda items)
5. **Video Timestamps** (if this is a video with timestamps, list the timestamps relevant to the user's tracked topics with deep-link seconds values)

Keep the summary under 500 words. Focus on the topics and keywords the user is tracking.
If this is an agenda, note what items are scheduled and when.
If this is minutes, note what decisions were made.
If this is a video, extract and highlight relevant timestamp chapters so the user can jump directly to the sections they care about.

IMPORTANT: Add this disclaimer at the end:
"AI-generated summary — verify all details with the original document."

Respond in JSON:
{{
  "summary": "...",
  "key_points": ["point1", "point2", ...],
  "status": "upcoming/in_progress/decided/deferred",
  "action_items": ["item1", ...],
  "relevant_excerpts": ["excerpt1", ...],
  "next_dates": ["YYYY-MM-DD description", ...],
  "relevant_timestamps": [
    {{"t": "0:15:30", "seconds": 930, "label": "Public Hearing - OCP Amendment", "relevance": "Matches OCP topic"}}
  ]
}}"""

EMBED_PROMPT = """Summarize this BC municipal government document for semantic search indexing.
Focus on: municipality name, meeting type, date, topics discussed, decisions made, key people mentioned.

If this is a video with chapter timestamps, include each timestamp label as a separate indexable phrase
so that searches for specific agenda items can find the exact video timestamp.

For example, if there are timestamps like:
  0:15:30 Public Hearing - OCP Amendment Bylaw 1234
  1:02:15 Rezoning Application - 123 Main St
Include those labels verbatim so they are searchable.

Document: {content}

{video_timestamps_text}

Output a single dense paragraph optimized for embedding-based retrieval. Include all timestamp labels inline."""

# Batch matching prompt — processes multiple documents in one call to reduce API costs
BATCH_MATCH_PROMPT = """You are a BC local government hearing analyst. Determine which of these documents are relevant to the user's tracking preferences.

USER TRACK:
- Municipalities: {municipalities}
- Topics of interest: {topics}
- Keywords: {keywords}

DOCUMENTS (evaluate each one):
{documents_list}

For EACH document, determine relevance. Respond with a JSON array:
[
  {{
    "doc_index": 0,
    "is_match": true/false,
    "confidence": 0.0-1.0,
    "matched_topics": ["topic1"],
    "matched_keywords": ["keyword1"],
    "reason": "Brief explanation"
  }},
  ...
]

Be generous — if a document MIGHT be relevant, mark it as a match with lower confidence."""

# Batch summary prompt — summarize multiple matched documents in one call
BATCH_SUMMARY_PROMPT = """You are a BC local government hearing analyst creating concise briefings.

USER CONTEXT:
- Tracking topics: {topics}
- Keywords: {keywords}

DOCUMENTS TO SUMMARIZE:
{documents_list}

For EACH document, create a focused summary. Respond with a JSON array:
[
  {{
    "doc_index": 0,
    "summary": "...",
    "key_points": ["point1", "point2"],
    "status": "upcoming/in_progress/decided/deferred",
    "action_items": ["item1"],
    "relevant_timestamps": [
      {{"t": "0:15:30", "seconds": 930, "label": "...", "relevance": "..."}}
    ]
  }},
  ...
]

Keep each summary under 300 words. For videos with timestamps, highlight the timestamps relevant to tracked topics.
Add this disclaimer to each summary: "AI-generated summary — verify with original document." """
