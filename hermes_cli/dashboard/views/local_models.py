"""View 6: Local Model Forge -- 8-bit furnace art, bento grid, local inference stats."""

import os
import json
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static
from textual import work


FURNACE_ART = """\
[#15152D]                                  \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584                                  [/]
[#1A1A38]                              \u2584\u2588\u2580[/][#222248]                   [/][#1A1A38]\u2580\u2588\u2584                              [/]
[#1E1E40]                            \u2588\u2588[/][#282850]                       [/][#1E1E40]\u2588\u2588                            [/]
[#222248]          \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584        \u2588\u2588[/][#303060]    [/][#353568]\u2666[/][#404078]\u2666[/][#484888]\u2666[/][#555599]\u2668[/][#484888]\u2666[/][#555599]\u2668[/][#484888]\u2666[/][#404078]\u2666[/][#353568]\u2666[/][#303060]    [/][#222248]\u2588\u2588        \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584          [/]
[#282850]         \u2588[/][#353568]\u2592\u2592\u2592\u2592\u2592\u2592\u2592[/][#282850]\u2588       \u2588\u2588[/][#383870]   [/][#484888]\u2666[/][#555599]\u2666\u2668\u2668\u2668\u2668\u2668\u2666[/][#484888]\u2666[/][#383870]   [/][#282850]\u2588\u2588       \u2588[/][#353568]\u2592\u2592\u2592\u2592\u2592\u2592\u2592[/][#282850]\u2588         [/]
[#303060]         \u2588[/][#404078]\u2592\u2592\u2592\u2592\u2592\u2592\u2592[/][#303060]\u2588       \u2588\u2588[/][#404078]  [/][#555599]\u2668\u2668[/][#484888] LOCAL [/][#555599]\u2668\u2668[/][#404078]  [/][#303060]\u2588\u2588       \u2588[/][#404078]\u2592\u2592\u2592\u2592\u2592\u2592\u2592[/][#303060]\u2588         [/]
[#282850]         \u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580        \u2588\u2588[/][#383870]   [/][#484888]\u2666[/][#555599]\u2666[/][#484888] FORGE [/][#555599]\u2666[/][#484888]\u2666[/][#383870]   [/][#282850]\u2588\u2588        \u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580         [/]
[#222248]                            \u2588\u2588[/][#303060]    [/][#353568]\u2666[/][#404078]\u2666[/][#484888]\u2666[/][#404078]\u2666[/][#353568]\u2666[/][#404078]\u2666[/][#484888]\u2666[/][#404078]\u2666[/][#353568]\u2666[/][#303060]    [/][#222248]\u2588\u2588                            [/]
[#1E1E40]                            \u2580\u2588\u2584[/][#282850]                       [/][#1E1E40]\u2584\u2588\u2580                            [/]
[#15152D]                                \u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580                                [/]\
"""


class ConnectionStatus(Static):
    status: reactive[dict] = reactive(dict, always_update=True)

    def render(self) -> str:
        header = "[bold #FFD700]\u2692 CONNECTION[/]\n\n"
        if not self.status:
            return header + "[dim #555577]Heating the forge...[/]"
        online = self.status.get("online", False)
        url = self.status.get("url", "localhost:1234")
        models = self.status.get("models", [])
        if online:
            status_line = f"[bold #00FF99]\u25CF ONLINE[/]  [dim #00A8CC]{url}[/]"
            if models:
                status_line += f"\n[dim #555577]{len(models)} model{'s' if len(models) != 1 else ''} loaded[/]"
                model_lines = []
                for m in models[:5]:
                    mid = m.get("id", "?")
                    model_lines.append(f"  [#E0F7FF]\u2514\u2500 \u2692 {mid}[/]")
                return header + status_line + "\n" + "\n".join(model_lines)
            return header + status_line
        else:
            error = self.status.get("error", "Connection refused")
            return header + f"[bold #FF4444]\u25CF OFFLINE[/]  [dim #00A8CC]{url}[/]\n[dim #555577]{error}[/]"


class LocalStats(Static):
    stats: reactive[dict] = reactive(dict, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_tokens
        header = "[bold #FFD700]\u03A3\u03A4\u0391\u03A4 \u2014 LOCAL USAGE[/]\n\n"
        if not self.stats:
            return header + "[dim #555577]No local forging recorded yet.[/]"
        sessions = self.stats.get("sessions", 0)
        messages = self.stats.get("messages", 0)
        tools = self.stats.get("tool_calls", 0)
        tokens = self.stats.get("total_tokens", 0)
        avg = int(self.stats.get("avg_tokens_per_session", 0))
        return (
            header
            + f"[bold #FFD700]SESS[/]       [#00FF99]{sessions}[/]\n"
            + f"[bold #FFD700]MSGS[/]       [#00FF99]{messages}[/]\n"
            + f"[bold #FFD700]STRK[/]       [#00FF99]{tools}[/]\n"
            + f"[bold #FFD700]TKNS[/]       [#00D4FF]{format_tokens(tokens)}[/]\n"
            + f"[bold #FFD700]AVG/S[/]      [dim #00A8CC]{format_tokens(avg)}[/]"
        )


class LocalModelBreakdown(Static):
    models: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_tokens
        header = "[bold #FFD700]\u039C\u039F\u039D\u03A4\u0395\u039B \u2014 LOCAL MODELS USED[/]\n\n"
        if not self.models:
            return header + "[dim #555577]No local model usage data.[/]"
        lines = [
            "  [dim #00A8CC]MODEL" + " " * 35 + "SESSIONS    MSGS      TOKENS[/]\n"
            + "  [dim #2A2A50]" + "\u2500" * 75 + "[/]"
        ]
        max_sessions = max(m.get("sessions", 1) for m in self.models)
        for m in self.models:
            name = m.get("model", "?")[:40]
            sessions = m.get("sessions", 0)
            msgs = m.get("messages", 0)
            tokens = format_tokens(m.get("tokens", 0))
            bar_len = int((sessions / max_sessions) * 25) if max_sessions > 0 else 0
            bar = "\u2588" * bar_len + "\u2591" * (25 - bar_len)
            lines.append(
                f"  [#E0F7FF]{name:<40}[/]  "
                f"[#00FF99]{sessions:>5}[/]    "
                f"[#00D4FF]{msgs:>5}[/]    "
                f"[#FFD700]{tokens:>8}[/]\n"
                f"  [dim #FF4444]{bar}[/]"
            )
        return header + "\n".join(lines)


class RecentLocalSessions(Static):
    sessions: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_timestamp
        header = "[bold #FFD700]\u039B\u039F\u0393 \u2014 RECENT FORGE SESSIONS[/]\n\n"
        if not self.sessions:
            return header + "[dim #555577]No local model sessions found.[/]"
        lines = []
        for s in self.sessions[:12]:
            ts = format_timestamp(s.get("started_at", 0))
            model = (s.get("model") or "?").split("/")[-1][:25]
            msgs = s.get("message_count", 0)
            tools = s.get("tool_call_count", 0)
            title = (s.get("title") or "untitled")[:30]
            sid = s.get("id", "")[:12]
            lines.append(
                f"  [dim #FF4444]\u2666[/]  [dim #00A8CC]{ts:<16}[/]  [#E0F7FF]{model:<25}[/]  "
                f"[dim #00D4FF]{msgs:>3}m[/]  [dim #FFD700]{tools:>3}\u2692[/]  "
                f"[dim #555577]{title:<30}[/]  [dim #2A2A50]{sid}[/]"
            )
        return header + "\n".join(lines)


class LocalModelsView(ScrollableContainer):
    """Local Model Forge -- bento grid with furnace art."""

    def compose(self) -> ComposeResult:
        yield Static(FURNACE_ART, classes="bento-hero")
        with Horizontal(classes="bento-row"):
            yield ConnectionStatus(id="conn-status", classes="bento")
            yield LocalStats(id="local-stats", classes="bento")
        yield LocalModelBreakdown(id="local-breakdown", classes="bento")
        yield RecentLocalSessions(id="local-sessions", classes="bento")

    @work(thread=True)
    def load_data(self) -> None:
        from hermes_cli.dashboard.data import (
            get_local_model_stats, get_local_model_breakdown,
            get_local_model_sessions,
        )
        stats = get_local_model_stats()
        breakdown = get_local_model_breakdown()
        sessions = get_local_model_sessions(limit=12)
        conn = self._check_connection()
        self.app.call_from_thread(self._apply, stats, breakdown, sessions, conn)

    def _check_connection(self) -> dict:
        import yaml
        from hermes_constants import get_hermes_home
        config_path = get_hermes_home() / "config.yaml"
        base_url = "http://localhost:1234/v1"
        try:
            if config_path.exists():
                with open(config_path) as f:
                    cfg = yaml.safe_load(f) or {}
                for p in cfg.get("custom_providers", []):
                    url = p.get("base_url", "")
                    if "localhost" in url or "127.0.0.1" in url:
                        base_url = url
                        break
        except Exception:
            pass
        try:
            import httpx
            resp = httpx.get(f"{base_url}/models", timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                models = data.get("data", [])
                return {"online": True, "url": base_url, "models": models}
            return {"online": False, "url": base_url, "error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"online": False, "url": base_url, "error": str(e)[:60]}

    def _apply(self, stats, breakdown, sessions, conn):
        self.query_one("#conn-status", ConnectionStatus).status = conn
        self.query_one("#local-stats", LocalStats).stats = stats
        self.query_one("#local-breakdown", LocalModelBreakdown).models = breakdown
        self.query_one("#local-sessions", RecentLocalSessions).sessions = sessions

    def on_show(self) -> None:
        self.load_data()
