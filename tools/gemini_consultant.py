#!/usr/bin/env python3
"""
gemini_consultant tool
Queries Gemini via VoiceNav bridge with Thinking/Pro selection.
"""

import json
import logging
from pathlib import Path

from tools.registry import registry

logger = logging.getLogger(__name__)

def check_requirements() -> bool:
    return Path.home().joinpath(".hermes/work/voicenavbrowser").exists()

def gemini_consultant(query: str, force_model: str = None) -> str:
    """
    Tool handler for Hermes.
    Returns JSON string with answer, model_used, success, query, error.
    """
    try:
        from skills.research.gemini_consultant.scripts.gemini_consultant import gemini_consultant as gc
        result = gc(query=query, force_model=force_model)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"gemini_consultant failed: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "query": query,
            "answer": "",
            "model_used": None
        })

# Register tool
registry.register(
    name="gemini_consultant",
    toolset="web",
    schema={
        "name": "gemini_consultant",
        "description": "Query Gemini via VoiceNav browser with automatic Thinking/Pro model selection. Primary consultant for complex and engineering problems.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The question or problem to ask Gemini."
                },
                "force_model": {
                    "type": "string",
                    "description": "Optional: 'thinking' or 'pro' to override auto-detection."
                }
            },
            "required": ["query"]
        }
    },
    handler=lambda args, **kw: gemini_consultant(**args),
    check_fn=check_requirements,
    requires_env=[],
    is_async=False,
    description="Query Gemini via VoiceNav browser with automatic Thinking/Pro model selection. Primary consultant for complex and engineering problems.",
    emoji="🔬"
)
