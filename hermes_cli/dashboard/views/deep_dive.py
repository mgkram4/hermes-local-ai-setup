"""View 5: Session Deep Dive -- 8-bit anvil art, bento grid, tool chain inspector."""

import json
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static, Input
from textual import work


FORGE_ART = """\
[#15152D]                                                                                        [/]
[#1A1A38]                    \u2584\u2584\u2584\u2584\u2584              [/][#222248]\u2666[/][#282850]\u2666[/][#303060]\u2666[/][#282850]\u2666[/][#222248]\u2666[/][#1A1A38]              \u2584\u2584\u2584\u2584\u2584                    [/]
[#1E1E40]                  \u2588\u2588[/][#282850]\u2592\u2592\u2592[/][#1E1E40]\u2588\u2588           [/][#303060]\u2666[/][#353568]\u2666[/][#404078]\u2666[/][#484888]\u2666[/][#404078]\u2666[/][#353568]\u2666[/][#303060]\u2666[/][#1E1E40]           \u2588\u2588[/][#282850]\u2592\u2592\u2592[/][#1E1E40]\u2588\u2588                  [/]
[#222248]                  \u2588\u2588[/][#303060]\u2592\u2592\u2592[/][#222248]\u2588\u2588         [/][#353568]\u2666[/][#404078]\u2666[/][#484888]\u2666[/][#555599]\u2692[/][#484888]\u2666[/][#555599]\u2692[/][#484888]\u2666[/][#404078]\u2666[/][#353568]\u2666[/][#222248]         \u2588\u2588[/][#303060]\u2592\u2592\u2592[/][#222248]\u2588\u2588                  [/]
[#282850]                  \u2588\u2588[/][#353568]\u2592\u2592\u2592[/][#282850]\u2588\u2588        [/][#383870]\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584[/][#282850]        \u2588\u2588[/][#353568]\u2592\u2592\u2592[/][#282850]\u2588\u2588                  [/]
[#303060]                  \u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580       [/][#404078]\u2588[/][#484888]  \u03A3\u03C6\u03C5\u03C1\u03AE\u03BB\u03B1\u03C4\u03BF  [/][#404078]\u2588[/][#303060]       \u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580                  [/]
[#282850]                              [/][#383870]\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580[/][#282850]                              [/]
[#15152D]                        [/][#1A1A38]\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584[/][#15152D]                        [/]\
"""


def _truncate(text: str, maxlen: int = 120) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    if len(text) > maxlen:
        return text[:maxlen] + "..."
    return text


def _format_tool_call_args(tc: dict) -> str:
    fn = tc.get("function", tc)
    args_raw = fn.get("arguments", "")
    if isinstance(args_raw, str):
        try:
            args_raw = json.loads(args_raw)
        except (json.JSONDecodeError, TypeError):
            return _truncate(str(args_raw), 80)
    if isinstance(args_raw, dict):
        parts = []
        for k, v in args_raw.items():
            val_str = _truncate(str(v), 50)
            parts.append(f"[dim #555577]{k}[/]=[#E0F7FF]{val_str}[/]")
        return "  ".join(parts)
    return _truncate(str(args_raw), 80)


class ToolHeavySessions(Static):
    sessions: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_timestamp
        header = "[bold #FFD700]\u2692 HEAVIEST FORGING SESSIONS[/]\n\n"
        if not self.sessions:
            return header + "[dim #555577]The forge is cold. No tool-calling sessions found.[/]"
        lines = []
        for s in self.sessions[:15]:
            ts = format_timestamp(s.get("started_at", 0))
            model = (s.get("model") or "?").split("/")[-1][:18]
            title = s.get("title") or _truncate(s.get("preview", ""), 35) or "untitled"
            title = title[:35]
            tc = s.get("tool_call_count", 0)
            msgs = s.get("message_count", 0)
            sid = s.get("id", "")[:14]
            tc_color = "#FF4444" if tc > 20 else "#FFD700" if tc > 10 else "#00FF99"
            sparks = "\u2666" * min(tc // 5, 5)
            lines.append(
                f"  [dim #FF4444]{sparks:<5}[/]  [{tc_color}]{tc:>4}[/]  [#00D4FF]{msgs:>3}[/]   "
                f"[dim #00A8CC]{ts:<16}[/]  [#E0F7FF]{title:<35}[/]  "
                f"[dim #555577]{model:<18}[/]  [dim #2A2A50]{sid}[/]"
            )
        return header + "\n".join(lines)


class SessionTimeline(Static):
    messages: reactive[list] = reactive(list, always_update=True)
    session_meta: reactive[dict] = reactive(dict, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_timestamp, format_tokens, format_cost
        if not self.session_meta:
            return ""
        s = self.session_meta
        sid = s.get("id", "?")
        model = s.get("model") or "unknown"
        title = s.get("title") or "untitled"
        tc = s.get("tool_call_count", 0)
        msgs_count = s.get("message_count", 0)
        tokens_in = s.get("input_tokens", 0)
        tokens_out = s.get("output_tokens", 0)
        cost = s.get("actual_cost_usd") or s.get("estimated_cost_usd") or 0
        ts = format_timestamp(s.get("started_at", 0))
        tc_color = '#FF4444' if tc > 20 else '#FFD700' if tc > 10 else '#00FF99'
        header = (
            f"[bold #FFD700]\u2554\u2550\u2550\u2550 FORGING LOG: {title} \u2550\u2550\u2550\u2557[/]\n"
            f"[dim #00A8CC]ID[/] {sid}  [dim #00A8CC]Model[/] [#E0F7FF]{model}[/]  "
            f"[dim #00A8CC]Started[/] {ts}  [dim #00A8CC]Msgs[/] {msgs_count}  "
            f"[dim #00A8CC]Strikes[/] [{tc_color}]{tc}[/]  "
            f"[dim #00A8CC]Tokens[/] [#00D4FF]{format_tokens(tokens_in + tokens_out)}[/]  "
            f"[dim #00A8CC]Cost[/] [#FFD700]{format_cost(cost)}[/]\n"
        )
        if not self.messages:
            return header + "[dim #555577]No messages in this session.[/]"
        lines = []
        step = 0
        for msg in self.messages:
            role = msg.get("role", "?")
            if role == "user":
                step += 1
                content = _truncate(msg.get("content") or "", 120)
                lines.append(
                    f"\n  [bold #FFD700]\u2560\u2550\u2550 STEP {step} \u2550\u2550\u2563[/]  [bold #00FF99]USER[/]\n"
                    f"    [#E0F7FF]{content}[/]"
                )
            elif role == "assistant":
                tool_calls = msg.get("tool_calls")
                content = msg.get("content")
                if tool_calls and isinstance(tool_calls, list):
                    for tc_item in tool_calls:
                        fn = tc_item.get("function", tc_item)
                        name = fn.get("name", "?")
                        args_str = _format_tool_call_args(tc_item)
                        tc_id = tc_item.get("id", "")[:12]
                        lines.append(
                            f"    [bold #FF4444]\u2666[/] [bold #00D4FF]STRIKE[/]  [bold #FFD700]{name}[/]  [dim #2A2A50]{tc_id}[/]\n"
                            f"      {args_str}"
                        )
                elif content:
                    text = _truncate(content, 200)
                    lines.append(f"    [bold #9B59D6]\u25C6 RESPONSE[/]\n      [#E0F7FF]{text}[/]")
            elif role == "tool":
                tool_name = msg.get("tool_name") or "?"
                content = _truncate(msg.get("content") or "", 150)
                lines.append(
                    f"    [dim #00A8CC]\u21B3 YIELD[/]  [dim #FFD700]{tool_name}[/]\n"
                    f"      [dim #555577]{content}[/]"
                )
        return header + "\n".join(lines)


class DeepDiveView(ScrollableContainer):
    """Session Deep Dive -- forge with bento grid."""

    def compose(self) -> ComposeResult:
        yield Static(FORGE_ART, classes="bento-hero")
        yield Input(
            placeholder="\u2692 Enter a session ID (or prefix) to inspect...",
            id="dive-input",
        )
        yield ToolHeavySessions(id="tool-sessions", classes="bento")
        yield SessionTimeline(id="session-timeline", classes="bento")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        sid = event.value.strip()
        if sid:
            self.inspect_session(sid)

    @work(thread=True)
    def load_data(self) -> None:
        from hermes_cli.dashboard.data import get_tool_heavy_sessions
        sessions = get_tool_heavy_sessions(limit=15)
        self.app.call_from_thread(
            self.query_one("#tool-sessions", ToolHeavySessions).__setattr__,
            "sessions", sessions
        )

    @work(thread=True)
    def inspect_session(self, session_id: str) -> None:
        from hermes_cli.dashboard.data import get_session_detail, get_session_messages
        from hermes_state import SessionDB
        db = SessionDB()
        try:
            resolved = db.resolve_session_id(session_id)
        finally:
            db.close()
        if not resolved:
            self.app.call_from_thread(self._show_error, session_id)
            return
        meta = get_session_detail(resolved)
        messages = get_session_messages(resolved)
        self.app.call_from_thread(self._apply_session, meta, messages)

    def _apply_session(self, meta, messages):
        timeline = self.query_one("#session-timeline", SessionTimeline)
        timeline.session_meta = meta or {}
        timeline.messages = messages or []

    def _show_error(self, sid):
        timeline = self.query_one("#session-timeline", SessionTimeline)
        timeline.session_meta = {"id": sid, "title": f"Session '{sid}' not found"}
        timeline.messages = []

    def on_show(self) -> None:
        self.load_data()
