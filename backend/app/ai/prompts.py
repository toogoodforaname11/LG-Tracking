"""Gemini prompts for matching and summarization."""

MATCH_PROMPT = """You are a BC local government hearing analyst specializing in housing policy. Your job is to determine if a municipal document is relevant to a user's tracking preferences.

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

TOPIC DEFINITIONS (be highly sensitive to these):
- "tod" = Transit Oriented Development — TOD policies, transit-oriented development plans, transit corridor planning, density along transit routes
- "toa_impl" = Transit Oriented Areas (TOA) implementation — TOA designations, TOA bylaws, TOA zoning, transit area plans
- "area_plans" = Area Plans — local area plans, neighbourhood plans, community-level land use plans
- "brt" = BRT (Bus Rapid Transit) or bus priority infrastructure — bus rapid transit, BRT corridors, bus lanes, transit priority signals
- "multimodal" = Multimodal transport and active transportation — cycling infrastructure, pedestrian networks, bike lanes, active transport, complete streets, multi-modal
- "provincial_targets" = Alignment with provincial housing targets / Housing Needs Reports — provincial housing targets, housing needs reports, mandated housing units, compliance with provincial requirements
- "ssmuh" = Small-Scale Multi-Unit Housing — SSMUH, duplex, triplex, fourplex, missing middle housing, small-scale multi-unit
- "housing_statutes" = Housing Statutes Amendment bills, Bill 44, Bill 46, Bill 47, provincial housing legislation, Housing Statutes Amendment Act
- "ocp_housing" = Official Community Plan housing updates — OCP amendments related to housing, housing designations in community plans
- "zoning_density" = Zoning/rezoning for housing density — upzoning, density bonuses, zoning bylaw amendments for housing
- "dev_permits_housing" = Development permits affecting housing supply — DP applications for residential, housing development variance permits
- "dev_cost_charges" = Development cost charges or affordability incentives — DCCs, community amenity contributions, density bonusing, affordable housing incentives, fee waivers
- "transportation_plan" = Transportation plan or transportation study — municipal transportation master plans, transportation studies

KEYWORD HIGH-PRIORITY RULE: The user's keywords field is the HIGHEST priority trigger. Every keyword — whether it looks like a bylaw number (e.g. "Bylaw 1700"), a bill name (e.g. "Bill 44"), an act name (e.g. "Housing Statutes Amendment Act"), or a general term (e.g. "TOA zoning") — should be treated as an exact-match trigger. If ANY keyword appears in the document text, it is a match with confidence 1.0 regardless of topic alignment. Keywords take precedence over topic matching.

Respond in JSON format:
{{
  "is_match": true/false,
  "confidence": 0.0-1.0,
  "matched_topics": ["topic1", "topic2"],
  "matched_keywords": ["keyword1"],
  "reason": "Brief explanation of why this matches or doesn't match"
}}

Be generous with matching — if a document MIGHT be relevant to housing or transit, mark it as a match with lower confidence. Only reject clearly irrelevant items."""

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
BATCH_MATCH_PROMPT = """You are a BC local government hearing analyst specializing in housing policy. Determine which of these documents are relevant to the user's tracking preferences.

USER TRACK:
- Municipalities: {municipalities}
- Topics of interest: {topics}
- Keywords: {keywords}

TOPIC DEFINITIONS (be highly sensitive to these):
- "tod" = Transit Oriented Development — TOD policies, transit-oriented development plans, transit corridor planning
- "toa_impl" = Transit Oriented Areas (TOA) implementation — TOA designations, TOA bylaws, TOA zoning
- "area_plans" = Area Plans — local area plans, neighbourhood plans, community-level land use plans
- "brt" = BRT (Bus Rapid Transit) or bus priority infrastructure — bus rapid transit, BRT corridors, bus lanes
- "multimodal" = Multimodal transport and active transportation — cycling, pedestrian networks, bike lanes, complete streets
- "provincial_targets" = Provincial housing targets / Housing Needs Reports — mandated housing units, compliance
- "ssmuh" = Small-Scale Multi-Unit Housing — SSMUH, duplex, triplex, fourplex, missing middle
- "housing_statutes" = Housing Statutes Amendment bills — Bill 44, Bill 46, Bill 47, provincial housing legislation
- "ocp_housing" = OCP housing updates — OCP amendments related to housing, housing designations
- "zoning_density" = Zoning/rezoning for housing density — upzoning, density bonuses, zoning bylaw amendments
- "dev_permits_housing" = Development permits affecting housing supply — DP applications, housing variance permits
- "dev_cost_charges" = Development cost charges or affordability incentives — DCCs, amenity contributions, fee waivers
- "transportation_plan" = Transportation plan or transportation study — municipal transportation master plans, transportation studies

KEYWORD HIGH-PRIORITY RULE: Every keyword in the user's keywords field is a HIGH PRIORITY exact-match trigger. If ANY keyword appears in the document, it is a match with confidence 1.0 regardless of topic alignment.

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

Be generous — if a document MIGHT be relevant to housing or transit, mark it as a match with lower confidence."""

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
