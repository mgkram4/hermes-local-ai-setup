"""Fleet monitor — tracks Hermes agent fleet and mirrors to Telegram.

Hooks into existing AIAgent callbacks (thinking, tool_progress, status, step)
and delegate_tool lifecycle events to maintain a live fleet state, then pushes
formatted updates to a Telegram chat so you can manage the pantheon on the go.

Telegram config is read from:
  1. ~/.hermes/config.yaml  gateway.platforms.telegram.token + home_channel.chat_id
  2. Env overrides: FLEET_TELEGRAM_TOKEN, FLEET_TELEGRAM_CHAT_ID

Usage from cli.py (after agent creation):
    from agent.fleet_monitor import init_fleet_monitor, get_fleet_monitor
    init_fleet_monitor(config)
    monitor = get_fleet_monitor()
    agent.thinking_callback  = monitor.wrap_thinking(agent.thinking_callback)
    agent.tool_progress_callback = monitor.wrap_tool(agent.tool_progress_callback)
    agent.status_callback    = monitor.on_status
"""

import datetime
import logging
import os
import queue
import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# God metadata
# ---------------------------------------------------------------------------

GOD_ICONS: Dict[str, str] = {
    "Hermes":     "~E~",
    "Athena":     ">O<",
    "Hephaestus": "[#]",
    "Poseidon":   "-Y-",
    "Artemis":    "->-",
    "Apollo":     "*O*",
    "Ares":       ">|<",
    "Zeus":       "/|\\",
    "Demeter":    "@.@",
    "Dionysus":   "<~>",
    "Hades":      "X.X",
}

GOD_ROLES: Dict[str, str] = {
    "Hermes":     "Orchestrator / Router",
    "Athena":     "Planner / Strategy",
    "Hephaestus": "Code Forge / Builder",
    "Poseidon":   "Tools / APIs / External",
    "Artemis":    "Search / Hunt / Retrieval",
    "Apollo":     "Oracle / Knowledge / RAG",
    "Ares":       "Executor / Task Runner",
    "Zeus":       "Critic / Validation",
    "Demeter":    "Memory / Storage",
    "Dionysus":   "Reflection / Improvement",
    "Hades":      "Failure Watch / Recovery",
}

STATUS_ICONS: Dict[str, str] = {
    "idle":        "...",
    "spawning":    ">>>",
    "thinking":    "???",
    "querying":    "<->",
    "processing":  "###",
    "responding":  ">>-",
    "complete":    "[x]",
    "failed":      "!!!",
    "interrupted": "/!\\",
    "retrying":    "<>",
}

# ASCII art faces — shown in Telegram when a god is the active worker.
# Kept compact (≤8 lines, ≤28 chars wide) for mobile readability.
GOD_ART: Dict[str, str] = {
    "Hermes": (
        "   /\\  ~E~  /\\\n"
        "  (  \\____/  )\n"
        "  ( . o  o . )\n"
        "   \\ . -- . /\n"
        "  ~~|  --  |~~\n"
        "    |  /\\  |\n"
        "   /~~  ~~\\\n"
        "  ~ messenger ~"
    ),
    "Athena": (
        "   ^ ^ ^ ^ ^\n"
        "   /~~~~~~~\\\n"
        "  | o --- o |\n"
        "  |  ` ^ `  |\n"
        "  |  =====  |\n"
        "   \\_______/\n"
        "  -^--^--^--\n"
        "  [ strategy ]"
    ),
    "Hephaestus": (
        "  [#]  [#]  [#]\n"
        "  /~~------~~\\\n"
        " | o      o |\n"
        " |   ====   |\n"
        " |_/~~~~~~\\_|\n"
        " |   ####   |\n"
        " |__ #### __|\n"
        "  [  forge  ]"
    ),
    "Poseidon": (
        "  -Y-  -Y-  -Y-\n"
        "  /~~~~~~~~~~~\\\n"
        " | o ----- o |\n"
        " |   ` ~ `   |\n"
        "  \\~~~~~~~~~/\n"
        "  ~~~~~~~~~~~\n"
        "  ~ ~ ~ ~ ~ ~\n"
        "  [  depths  ]"
    ),
    "Artemis": (
        "    ->   ->\n"
        "   /--------\\\n"
        "  | o --- o |\n"
        "  |  ` ^ `  |\n"
        "   \\-------/\n"
        "   /|     |\\\n"
        "  -*----- -*-\n"
        "  [  hunter  ]"
    ),
    "Apollo": (
        "  *.*  *.*  *.*\n"
        "  /~~-------~~\\\n"
        " | o ----- o |\n"
        " |   ` O `   |\n"
        "  \\---------/\n"
        "  -|---------|--\n"
        "  -|---------|--\n"
        "  [  oracle  ]"
    ),
    "Ares": (
        "  >|<  >|<  >|<\n"
        "  /##########\\\n"
        " |o ------- o|\n"
        " |  `  #  `  |\n"
        " |  ========  |\n"
        "  \\##########/\n"
        "  /|        |\\\n"
        "  [ execute ]"
    ),
    "Zeus": (
        "  /|\\  /|\\  /|\\\n"
        "  /~~------~~\\\n"
        " |o ------- o|\n"
        " |   ` - `   |\n"
        " |  =======  |\n"
        "  \\---------/\n"
        "  ~-----------~\n"
        "  [  judge  ]"
    ),
    "Demeter": (
        "  -#-  -#-  -#-\n"
        "  /~~-------~~\\\n"
        " | o ----- o |\n"
        " |   ` w `   |\n"
        "  \\---------/\n"
        "  ~*-------*~\n"
        "  ~*-------*~\n"
        "  [  memory  ]"
    ),
    "Dionysus": (
        "  <~>  <~>  <~>\n"
        "  /~~-------~~\\\n"
        " | o ----- o |\n"
        " |   ` & `   |\n"
        "  \\---------/\n"
        "  ~~~~~~~~~~~\n"
        "  ~~~~~~~~~~~\n"
        "  [ reflect ]"
    ),
    "Hades": (
        "  X.X  X.X  X.X\n"
        "  /##-------##\\\n"
        " |o ------- o|\n"
        " |   ` v `   |\n"
        " |###########|\n"
        "  \\#########/\n"
        "  ...........\n"
        "  [ recovery ]"
    ),
}


# ---------------------------------------------------------------------------
# State dataclasses
# ---------------------------------------------------------------------------

@dataclass
class AgentState:
    name: str
    role: str = ""
    status: str = "thinking"
    current_tool: str = ""
    tool_preview: str = ""
    step: int = 0
    start_time: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    parent: str = "Hermes"
    last_event: str = ""


@dataclass
class FleetState:
    task: str = ""
    start_time: float = field(default_factory=time.time)
    agents: Dict[str, AgentState] = field(default_factory=dict)
    events: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# FleetMonitor
# ---------------------------------------------------------------------------

class FleetMonitor:
    """Central fleet state tracker with Telegram push."""

    MAX_EVENTS = 30
    DEBOUNCE_NORMAL = 4.0   # seconds between routine pushes
    DEBOUNCE_URGENT = 0.8   # seconds between urgent pushes

    def __init__(self):
        self._state = FleetState()
        self._lock = threading.Lock()
        self._push_queue: queue.Queue = queue.Queue(maxsize=50)
        self._tg_token: Optional[str] = None
        self._tg_chat_id: Optional[str] = None
        self._enabled = False
        self._verbose_mode = "normal"   # quiet / normal / god
        self._last_msg_id: Optional[int] = None
        self._push_thread: Optional[threading.Thread] = None

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------

    def init(self, config: dict) -> None:
        """Load Telegram config and start push thread."""
        try:
            gw = config.get("gateway", {})
            plats = gw.get("platforms", {})
            tg = plats.get("telegram", {})
            self._tg_token = (
                os.getenv("FLEET_TELEGRAM_TOKEN")
                or tg.get("token")
                or os.getenv("TELEGRAM_BOT_TOKEN")
            )
            home = tg.get("home_channel", {})
            chat_id = ""
            if isinstance(home, dict):
                chat_id = str(home.get("chat_id", ""))
            self._tg_chat_id = os.getenv("FLEET_TELEGRAM_CHAT_ID") or chat_id
        except Exception as e:
            logger.debug("Fleet monitor config error: %s", e)

        self._enabled = bool(self._tg_token and self._tg_chat_id)
        if self._enabled:
            self._push_thread = threading.Thread(
                target=self._push_worker, daemon=True, name="fleet-tg"
            )
            self._push_thread.start()
            logger.info("Fleet monitor: Telegram mirror active → chat %s", self._tg_chat_id)
        else:
            logger.debug("Fleet monitor: Telegram not configured (set FLEET_TELEGRAM_TOKEN + FLEET_TELEGRAM_CHAT_ID)")

        # Always register Hermes as root
        with self._lock:
            self._state.agents["Hermes"] = AgentState(
                name="Hermes", role=GOD_ROLES["Hermes"]
            )

    def set_verbose_mode(self, mode: str) -> None:
        """Set verbosity: quiet / normal / god."""
        self._verbose_mode = mode.lower().strip()
        with self._lock:
            self._log(f"Verbose mode: {self._verbose_mode.upper()}")
        self._push(urgent=True)

    # ------------------------------------------------------------------
    # Callback wrappers (wrap existing cli.py callbacks)
    # ------------------------------------------------------------------

    def wrap_thinking(self, original: Optional[Callable]) -> Callable:
        """Return a thinking_callback that notifies the monitor then calls original."""
        monitor = self

        def _thinking(text: str) -> None:
            if text and not text.startswith("_"):
                with monitor._lock:
                    agent = monitor._get_or_create("Hermes")
                    agent.status = "thinking"
                    agent.last_event = (text[:60] if text else "")
                    agent.last_activity = time.time()
                    if monitor._verbose_mode == "god":
                        monitor._log(f"Hermes thinking: {text[:60]}")
                if monitor._verbose_mode == "god":
                    monitor._push(urgent=False)
            if original:
                original(text)

        return _thinking

    def wrap_tool(self, original: Optional[Callable]) -> Callable:
        """Return a tool_progress_callback that notifies the monitor then calls original."""
        monitor = self

        def _tool(function_name: str, preview: str, function_args: dict) -> None:
            if function_name and not function_name.startswith("_"):
                with monitor._lock:
                    agent = monitor._get_or_create("Hermes")
                    agent.status = "querying"
                    agent.current_tool = function_name
                    agent.tool_preview = (preview or "")[:50]
                    agent.last_activity = time.time()
                    short = f" → {agent.tool_preview}" if agent.tool_preview else ""
                    agent.last_event = f"{function_name}{short}"
                    monitor._log(f"Hermes: {function_name}{short}")
                monitor._push(urgent=False)
            if original:
                original(function_name, preview, function_args)

        return _tool

    def on_status(self, category: str, message: str) -> None:
        """status_callback — lifecycle events from AIAgent."""
        with self._lock:
            self._log(f"[{category}] {message}")
            if any(kw in message.lower() for kw in ("error", "fail", "interrupt", "retry")):
                agent = self._get_or_create("Hermes")
                agent.status = "interrupted"
                agent.last_event = message[:60]
        is_critical = any(kw in message.lower() for kw in ("error", "fail", "interrupt"))
        self._push(urgent=is_critical)

    # ------------------------------------------------------------------
    # God lifecycle (called from delegate_tool.py)
    # ------------------------------------------------------------------

    def on_task_start(self, task: str) -> None:
        with self._lock:
            self._state.task = task[:80]
            self._state.start_time = time.time()
            self._state.events.clear()
            self._last_msg_id = None   # new task = new message thread
            agent = self._get_or_create("Hermes")
            agent.status = "thinking"
            agent.step = 0
            self._log(f"Task received: {task[:60]}")
        self._push(urgent=True)

    def on_god_spawned(self, name: str, role: str = "", goal: str = "", parent: str = "Hermes") -> None:
        with self._lock:
            resolved_role = role or GOD_ROLES.get(name, "Subagent")
            self._state.agents[name] = AgentState(
                name=name, role=resolved_role, status="spawning", parent=parent
            )
            hermes = self._get_or_create("Hermes")
            hermes.status = "processing"
            goal_short = goal[:50] if goal else resolved_role
            self._log(f"Hermes → {name}: {goal_short}")
        self._push(urgent=True)

    def on_god_complete(self, name: str, result_preview: str = "") -> None:
        with self._lock:
            agent = self._get_or_create(name)
            agent.status = "complete"
            agent.current_tool = ""
            agent.last_activity = time.time()
            short = result_preview[:50] if result_preview else "done"
            agent.last_event = short
            self._log(f"{name} ✓ {short}")
        self._push(urgent=True)

    def on_god_failed(self, name: str, error: str = "") -> None:
        with self._lock:
            agent = self._get_or_create(name)
            agent.status = "failed"
            agent.last_activity = time.time()
            agent.last_event = error[:60] if error else "failed"
            self._log(f"⚠ {name} failed: {error[:50]}")
        self._push(urgent=True)

    def on_response_complete(self) -> None:
        with self._lock:
            agent = self._get_or_create("Hermes")
            agent.status = "complete"
            agent.current_tool = ""
            self._log("Response delivered ✓")
        self._push(urgent=True)
        # Reset subagents after a delay
        threading.Timer(8.0, self._reset_subagents).start()

    def on_step(self, iteration: int, tools: list, agent_name: str = "Hermes") -> None:
        with self._lock:
            agent = self._get_or_create(agent_name)
            agent.step = iteration

    # ------------------------------------------------------------------
    # Telegram formatting
    # ------------------------------------------------------------------

    def _format_message(self) -> str:
        state = self._state
        now = time.time()
        elapsed = int(now - state.start_time)
        mins, secs = divmod(elapsed, 60)
        elapsed_str = f"{mins}:{secs:02d}"

        lines: List[str] = []
        lines.append(f"⚡ <b>OLYMPUS FLEET</b>  ·  ⏱ {elapsed_str}")

        if state.task:
            # Truncate long tasks for mobile
            task_display = state.task if len(state.task) <= 70 else state.task[:67] + "..."
            lines.append(f"<i>{task_display}</i>")

        lines.append("──────────────────────")

        # Agent tree: Hermes first, then children
        hermes = state.agents.get("Hermes")
        if hermes:
            lines.append(self._format_agent(hermes))

        children = [a for n, a in state.agents.items() if n != "Hermes"]
        for agent in children:
            lines.append(self._format_agent(agent, child=True))

        # Active god ASCII art — show the god currently doing work
        active_god = None
        active_statuses = ("spawning", "thinking", "querying", "processing")
        for name, agent in state.agents.items():
            if name != "Hermes" and agent.status in active_statuses:
                active_god = agent
                break
        # Fall back to Hermes if no child is active
        if active_god is None and hermes and hermes.status in active_statuses:
            active_god = hermes

        if active_god and active_god.name in GOD_ART:
            art = GOD_ART[active_god.name]
            lines.append("")
            lines.append(f"<code>{art}</code>")

        # Verbose event feed
        if state.events and self._verbose_mode != "quiet":
            count = 8 if self._verbose_mode == "god" else 4
            lines.append("")
            lines.append("<b>Events</b>")
            for evt in state.events[-count:]:
                lines.append(f"  {evt}")

        lines.append("──────────────────────")
        mode_label = f"👁 GOD MODE" if self._verbose_mode == "god" else f"mode: {self._verbose_mode}"
        lines.append(f"<code>{mode_label}</code>  ·  reply /abort /mode /status")

        return "\n".join(lines)

    def _format_agent(self, agent: AgentState, child: bool = False) -> str:
        icon = GOD_ICONS.get(agent.name, "◈")
        s_icon = STATUS_ICONS.get(agent.status, "◈")
        prefix = "  └ " if child else ""
        name_part = f"<b>{agent.name}</b>"

        detail = ""
        if agent.current_tool and agent.status not in ("complete", "failed", "idle"):
            preview = f" → {agent.tool_preview}" if agent.tool_preview else ""
            detail = f"  <code>{agent.current_tool}{preview}</code>"
        elif agent.last_event and agent.status in ("complete", "failed"):
            detail = f"  <i>{agent.last_event}</i>"
        elif agent.role and agent.status in ("spawning", "thinking"):
            detail = f"  <i>{agent.role}</i>"

        return f"{prefix}{icon} {name_part} {s_icon}{detail}"

    # ------------------------------------------------------------------
    # Telegram push (background thread)
    # ------------------------------------------------------------------

    def _push(self, urgent: bool = False) -> None:
        if not self._enabled:
            return
        try:
            self._push_queue.put_nowait(urgent)
        except queue.Full:
            pass

    def _push_worker(self) -> None:
        import requests

        last_push = 0.0
        last_msg_id: Optional[int] = None

        while True:
            try:
                urgent = self._push_queue.get(timeout=60)

                # Drain queue — only care about latest state
                while not self._push_queue.empty():
                    try:
                        latest = self._push_queue.get_nowait()
                        urgent = urgent or latest
                    except queue.Empty:
                        break

                # Debounce
                now = time.time()
                debounce = self.DEBOUNCE_URGENT if urgent else self.DEBOUNCE_NORMAL
                wait = debounce - (now - last_push)
                if wait > 0:
                    time.sleep(wait)

                text = self._format_message()
                base = f"https://api.telegram.org/bot{self._tg_token}"

                # Try edit first (keeps one live message per task)
                edited = False
                if last_msg_id:
                    r = requests.post(
                        f"{base}/editMessageText",
                        json={
                            "chat_id": self._tg_chat_id,
                            "message_id": last_msg_id,
                            "text": text,
                            "parse_mode": "HTML",
                        },
                        timeout=6,
                    )
                    edited = r.ok

                if not edited:
                    r = requests.post(
                        f"{base}/sendMessage",
                        json={
                            "chat_id": self._tg_chat_id,
                            "text": text,
                            "parse_mode": "HTML",
                        },
                        timeout=6,
                    )
                    if r.ok:
                        last_msg_id = r.json().get("result", {}).get("message_id")
                    else:
                        logger.debug("Fleet TG push failed: %s", r.text[:200])

                last_push = time.time()

            except queue.Empty:
                pass
            except Exception as e:
                logger.debug("Fleet monitor push error: %s", e)
                time.sleep(5)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_or_create(self, name: str) -> AgentState:
        """Get or create agent state. Call with self._lock held."""
        if name not in self._state.agents:
            self._state.agents[name] = AgentState(
                name=name, role=GOD_ROLES.get(name, "Subagent")
            )
        return self._state.agents[name]

    def _log(self, message: str) -> None:
        """Append timestamped event. Call with self._lock held."""
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self._state.events.append(f"[{ts}] {message}")
        if len(self._state.events) > self.MAX_EVENTS:
            self._state.events.pop(0)

    def _reset_subagents(self) -> None:
        with self._lock:
            hermes = self._state.agents.get("Hermes")
            self._state.agents.clear()
            if hermes:
                hermes.status = "idle"
                hermes.current_tool = ""
                hermes.last_event = ""
                self._state.agents["Hermes"] = hermes


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_monitor: Optional[FleetMonitor] = None


def get_fleet_monitor() -> FleetMonitor:
    global _monitor
    if _monitor is None:
        _monitor = FleetMonitor()
    return _monitor


def init_fleet_monitor(config: dict) -> FleetMonitor:
    monitor = get_fleet_monitor()
    monitor.init(config)
    return monitor
