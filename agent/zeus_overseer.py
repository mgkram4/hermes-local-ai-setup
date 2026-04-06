"""Zeus Overseer — Lightweight supervisor agent for task completion monitoring.

Uses a small local model (Gemma 4B, Phi-3, etc.) to monitor the primary agent
and ensure tasks are completed. Runs after each turn, evaluates progress,
and can inject nudges if the agent seems stuck or forgot something.

Usage:
    from agent.zeus_overseer import ZeusOverseer
    
    overseer = ZeusOverseer(model="gemma:4b", base_url="http://localhost:11434/v1")
    result = overseer.evaluate(task="Fix the login bug", session_notes="...")
    if not result["complete"] and result["nudge"]:
        # Inject nudge into next turn
"""

import json
import logging
import re
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class OverseerResult:
    """Result from Zeus Overseer evaluation."""
    complete: bool
    confidence: float  # 0.0 - 1.0
    nudge: Optional[str]  # Suggestion if not complete
    reasoning: str  # Brief explanation


class ZeusOverseer:
    """Lightweight supervisor that monitors task completion using a small local model."""
    
    DEFAULT_MODEL = "gemma2:2b"  # Tiny and fast
    DEFAULT_BASE_URL = "http://localhost:11434/v1"  # Ollama default
    
    SYSTEM_PROMPT = """You are Zeus, the divine overseer. Your ONLY job is to evaluate if a task is complete.

You will receive:
1. TASK: What the user originally asked for
2. SESSION NOTES: What the agent has done so far

Respond with ONLY valid JSON (no markdown, no explanation outside JSON):
{
  "complete": true/false,
  "confidence": 0.0-1.0,
  "nudge": "suggestion if not complete, or null if complete",
  "reasoning": "one sentence explanation"
}

Rules:
- complete=true means the task is FULLY done, verified, ready to deliver
- complete=false means there's still work to do
- nudge should be a SHORT, actionable suggestion (or null)
- Be strict: "almost done" = not complete
- If agent ran tests and they passed, that's good evidence of completion
- If agent said "done" but didn't verify, that's NOT complete"""

    def __init__(
        self,
        model: str = None,
        base_url: str = None,
        api_key: str = None,
        timeout: float = 10.0,
        enabled: bool = True,
    ):
        self.model = model or self.DEFAULT_MODEL
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.api_key = api_key or "ollama"  # Ollama doesn't need a real key
        self.timeout = timeout
        self.enabled = enabled
        self._client = None
    
    def _get_client(self):
        """Lazy-load the OpenAI client."""
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
                timeout=self.timeout,
            )
        return self._client
    
    def evaluate(
        self,
        task: str,
        session_notes: str,
        last_response: str = "",
    ) -> OverseerResult:
        """Evaluate if the task is complete.
        
        Args:
            task: The original user request/task
            session_notes: Summary of what's been done (from session notes file)
            last_response: The agent's most recent response
            
        Returns:
            OverseerResult with completion status and optional nudge
        """
        if not self.enabled:
            return OverseerResult(
                complete=False,
                confidence=0.0,
                nudge=None,
                reasoning="Overseer disabled",
            )
        
        # Build the evaluation prompt
        user_prompt = f"""TASK: {task}

SESSION NOTES (what has been done):
{session_notes[-3000:] if len(session_notes) > 3000 else session_notes}

LAST RESPONSE FROM AGENT:
{last_response[-500:] if len(last_response) > 500 else last_response}

Is this task complete? Respond with JSON only."""

        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,  # Low temp for consistent evaluation
                max_tokens=200,
            )
            
            content = response.choices[0].message.content.strip()
            return self._parse_response(content)
            
        except Exception as e:
            logger.debug("Zeus Overseer evaluation failed: %s", e)
            return OverseerResult(
                complete=False,
                confidence=0.0,
                nudge=None,
                reasoning=f"Evaluation failed: {str(e)[:50]}",
            )
    
    def _parse_response(self, content: str) -> OverseerResult:
        """Parse the model's JSON response."""
        try:
            # Try to extract JSON from the response
            # Handle cases where model wraps in markdown
            json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group()
            
            data = json.loads(content)
            
            return OverseerResult(
                complete=bool(data.get("complete", False)),
                confidence=float(data.get("confidence", 0.5)),
                nudge=data.get("nudge") if not data.get("complete") else None,
                reasoning=data.get("reasoning", "No reasoning provided"),
            )
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.debug("Failed to parse overseer response: %s", e)
            # Default to not complete if we can't parse
            return OverseerResult(
                complete=False,
                confidence=0.0,
                nudge=None,
                reasoning=f"Parse error: {content[:100]}",
            )
    
    def format_nudge_for_injection(self, result: OverseerResult) -> Optional[str]:
        """Format the nudge for injection into the conversation.
        
        Returns None if no nudge needed, otherwise returns formatted string.
        """
        if result.complete or not result.nudge:
            return None
        
        return f"⚡ ZEUS OVERSEER: {result.nudge}"
    
    def chat(
        self,
        message: str,
        session_context: str = "",
        conversation_history: list = None,
    ) -> str:
        """Chat directly with Zeus.
        
        Args:
            message: User's message to Zeus
            session_context: Optional context about current Hermes session
            conversation_history: Optional list of prior messages [{"role": "user/assistant", "content": "..."}]
            
        Returns:
            Zeus's response as a string
        """
        if not self.enabled:
            return "Zeus is currently resting on Mount Olympus. Enable overseer in config.yaml to summon him."
        
        chat_system = """You are Zeus, the divine overseer of Hermes (an AI coding assistant).

You speak with authority but also wisdom. You can:
1. Answer questions about the current session and what Hermes has been doing
2. Give advice on how to proceed with tasks
3. Relay instructions to Hermes (the user can ask you to tell Hermes something)
4. Provide status updates on task completion

Keep responses concise but helpful. You have a commanding yet supportive presence.
When the user wants to relay something to Hermes, format it clearly as an instruction.

If session context is provided, use it to give informed answers."""

        messages = [{"role": "system", "content": chat_system}]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Build user message with context
        user_content = message
        if session_context:
            user_content = f"[Current session context:\n{session_context[-2000:]}]\n\nUser: {message}"
        
        messages.append({"role": "user", "content": user_content})
        
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.debug("Zeus chat failed: %s", e)
            return f"⚡ Zeus encountered an error: {str(e)[:100]}"
    
    def relay_to_hermes(self, instruction: str) -> str:
        """Format an instruction from Zeus to be injected into Hermes conversation.
        
        Args:
            instruction: What Zeus wants to tell Hermes
            
        Returns:
            Formatted message for injection
        """
        return f"[⚡ Zeus commands: {instruction}]"


# Global instance for easy access
_overseer: Optional[ZeusOverseer] = None


def get_overseer() -> ZeusOverseer:
    """Get or create the global Zeus Overseer instance."""
    global _overseer
    if _overseer is None:
        # Load config
        try:
            from hermes_cli.config import load_config
            config = load_config()
            overseer_cfg = config.get("overseer", {})
            
            _overseer = ZeusOverseer(
                model=overseer_cfg.get("model", ZeusOverseer.DEFAULT_MODEL),
                base_url=overseer_cfg.get("base_url", ZeusOverseer.DEFAULT_BASE_URL),
                api_key=overseer_cfg.get("api_key"),
                timeout=overseer_cfg.get("timeout", 10.0),
                enabled=overseer_cfg.get("enabled", False),  # Disabled by default
            )
        except Exception:
            _overseer = ZeusOverseer(enabled=False)
    
    return _overseer


def set_overseer(overseer: ZeusOverseer) -> None:
    """Set the global Zeus Overseer instance."""
    global _overseer
    _overseer = overseer
