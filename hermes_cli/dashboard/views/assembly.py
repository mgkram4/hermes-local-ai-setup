"""View 1: The Assembly -- Home view with 8-bit Hermes art, bento grid, live data."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static
from textual import work


HERMES_PIXEL_ART = """\
[#15152D]                                        \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584                                        [/]
[#15152D]                                   \u2584\u2584\u2580\u2580[/][#1A1A38]                   [/][#15152D]\u2580\u2580\u2584\u2584                                   [/]
[#1A1A38]                              \u2584\u2580\u2580[/][#1E1E40]       \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584       [/][#1A1A38]\u2580\u2580\u2584                              [/]
[#1E1E40]                         \u2584\u2580\u2580[/][#222248]     \u2584\u2588\u2588\u2580\u2580[/][#2A2A55]         [/][#222248]\u2580\u2580\u2588\u2588\u2584     [/][#1E1E40]\u2580\u2580\u2584                         [/]
[#222248]                    \u2584\u2580\u2580[/][#282850]    \u2584\u2588\u2580[/][#303060]       [/][#353568]\u2695[/][#303060]       [/][#282850]\u2580\u2588\u2584    [/][#222248]\u2580\u2580\u2584                    [/]
[#282850]                \u2584\u2580\u2580[/][#303060]     \u2584\u2588\u2580[/][#383870]                   [/][#303060]\u2580\u2588\u2584     [/][#282850]\u2580\u2580\u2584                [/]
[#303060]            \u2580\u2580\u2584\u2584[/][#353568]     \u2588\u2580[/][#404078]      \u2584\u2580\u2580\u2580\u2580\u2580\u2584      [/][#353568]\u2580\u2588     [/][#303060]\u2584\u2584\u2580\u2580            [/]
[#353568]                 [/][#303060]\u2580\u2580\u2588\u2580[/][#404078]    \u2580[/][#484888]               [/][#404078]\u2580    [/][#303060]\u2580\u2588\u2580\u2580[/][#353568]                 [/]
[#353568]                  [/][#404078]\u2588\u2588[/][#484888]  \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584  [/][#404078]\u2588\u2588[/][#353568]                  [/]
[#303060]                   [/][#383870]\u2580\u2588\u2584\u2584[/][#484888]\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584[/][#383870]\u2584\u2584\u2588\u2580[/][#303060]                   [/]
[#282850]                      [/][#303060]\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580[/][#282850]                      [/]
[#222248]                              [/][#282850]\u2588\u2588[/][#303060]     [/][#353568]\u2695[/][#303060]     [/][#282850]\u2588\u2588[/][#222248]                              [/]
[#1E1E40]                              [/][#222248]\u2588\u2588[/][#282850]             [/][#222248]\u2588\u2588[/][#1E1E40]                              [/]
[#1A1A38]                              [/][#1E1E40]\u2588\u2588[/][#222248]             [/][#1E1E40]\u2588\u2588[/][#1A1A38]                              [/]
[#15152D]                              [/][#1A1A38]\u2588\u2588[/][#1E1E40]             [/][#1A1A38]\u2588\u2588[/][#15152D]                              [/]
[#15152D]                            [/][#1A1A38]\u2584\u2588\u2588\u2588\u2588[/][#1E1E40]           [/][#1A1A38]\u2588\u2588\u2588\u2588\u2584[/][#15152D]                            [/]
[#15152D]                          [/][#1A1A38]\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580[/][#1E1E40]           [/][#1A1A38]\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580[/][#15152D]                          [/]\
"""


def _make_god_card(god: dict) -> str:
    name = god.get("name", "?")
    icon = god.get("icon", "\u2727")
    rank = god.get("rank", "???")
    return (
        f"[bold #FFD700]{icon}[/]\n"
        f"[bold #E0F7FF]{name}[/]\n"
        f"[dim #00A8CC]{rank}[/]"
    )


def _make_exec_lane(name: str, desc: str, pct: int, lat: int) -> str:
    filled = int(pct / 100 * 15)
    bar = "\u2588" * filled + "\u2591" * (15 - filled)
    color = "#00FF99" if pct > 60 else "#FFD700" if pct > 30 else "#FF4444"
    return (
        f"  [dim #00A8CC]\u039B[/]  [bold #E0F7FF]{name:<10}[/]  "
        f"[dim #555577]{desc:<30}[/]  "
        f"[{color}]{bar}[/] [{color}]{pct}%[/]  "
        f"[dim #555577]{lat}ms[/]"
    )


class HeroArt(Static):
    def render(self) -> str:
        return HERMES_PIXEL_ART


class PantheonRow(Static):
    gods: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        if not self.gods:
            return "[dim #555577]Loading pantheon...[/]"
        cards = []
        for god in self.gods:
            cards.append(_make_god_card(god))
        separator = "  [dim #2A2A50]\u2502[/]  "
        lines_per_card = [c.split("\n") for c in cards]
        max_lines = max(len(c) for c in lines_per_card)
        for c in lines_per_card:
            while len(c) < max_lines:
                c.append("")
        rows = []
        for i in range(max_lines):
            row_parts = [c[i] for c in lines_per_card]
            rows.append(separator.join(row_parts))
        return "\n".join(rows)


class ExecLanes(Static):
    def render(self) -> str:
        header = "[bold #FFD700]\u2727 EXECUTION LANES[/]\n\n"
        lanes = [
            _make_exec_lane("ATHENA", "objective \u2192 architecture", 71, 42),
            _make_exec_lane("APOLLO", "signal \u2192 evaluation", 58, 35),
            _make_exec_lane("ARES", "command \u2192 execution", 44, 49),
        ]
        flow = (
            "\n\n  [dim #00A8CC]\u03A6\u039B\u039F\u03A9[/]  "
            "[dim #00D4FF]ATHENA \u2500\u25B6 APOLLO \u2500\u25B6 ARES \u2500\u25B6 ZEUS[/]  "
            "[dim #2A2A50]\u2502[/]  "
            "[dim #00D4FF]ARTEMIS \u2500\u25B6 HADES \u2500\u25B6 HERMES[/]"
        )
        return header + "\n".join(lanes) + flow


class RecentSessions(Static):
    sessions: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_timestamp, format_cost
        header = "[bold #FFD700]\U0001F4DC RECENT DECREES[/]\n\n"
        if not self.sessions:
            return header + "[dim #555577]No decrees yet.[/]"
        lines = []
        for s in self.sessions[:8]:
            ts = format_timestamp(s.get("last_active") or s.get("started_at", 0))
            model = (s.get("model") or "?").split("/")[-1][:18]
            title = (s.get("title") or s.get("preview", "") or "untitled")[:35]
            cost = format_cost(s.get("actual_cost_usd") or s.get("estimated_cost_usd") or 0)
            msgs = s.get("message_count", 0)
            lines.append(
                f"  [dim #00A8CC]{ts:<16}[/]  [#E0F7FF]{title:<35}[/]  "
                f"[dim #555577]{model:<18}[/]  [dim #00D4FF]{msgs} msgs[/]  [dim #FFD700]{cost}[/]"
            )
        return header + "\n".join(lines)


class MemoryPreview(Static):
    entries: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        header = "[bold #FFD700]\U0001F56F \u039C\u039D\u0397\u039C\u0397[/]\n\n"
        if not self.entries:
            return header + "[dim #555577]The tablets are blank.[/]"
        lines = []
        for entry in self.entries[:5]:
            text = entry[:55] + ("..." if len(entry) > 55 else "")
            lines.append(f"  [dim #00D4FF]\u00A7[/] [dim #E0F7FF]{text}[/]")
        return header + "\n".join(lines)


class QuickStats(Static):
    stats: reactive[dict] = reactive(dict, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_tokens, format_cost
        if not self.stats:
            return "[dim #555577]Consulting the oracle...[/]"
        sessions = self.stats.get("total_sessions", 0)
        messages = self.stats.get("total_messages", 0)
        tools = self.stats.get("total_tool_calls", 0)
        tokens = self.stats.get("total_input_tokens", 0) + self.stats.get("total_output_tokens", 0)
        cost = self.stats.get("total_cost", 0)
        return (
            f"[bold #FFD700]\u03A3\u03B5\u03C3\u03C3\u03B9\u03BF\u03BD\u03C2[/]  [bold #00FF99]{sessions}[/]"
            f"     [bold #FFD700]\u039C\u03B5\u03C3\u03C3\u03B1\u03B3\u03B5\u03C2[/]  [bold #00FF99]{messages}[/]"
            f"     [bold #FFD700]\u0395\u03C1\u03B3\u03B1\u03BB\u03B5\u03AF\u03B1[/]  [bold #00FF99]{tools}[/]"
            f"     [bold #FFD700]\u039C\u03AC\u03C1\u03BA\u03B5\u03C2[/]  [bold #00D4FF]{format_tokens(tokens)}[/]"
            f"     [bold #FFD700]\u0394\u03C1\u03B1\u03C7\u03BC\u03B1\u03AF[/]  [bold #FFD700]{format_cost(cost)}[/]"
        )


class AssemblyView(ScrollableContainer):
    """The Assembly -- main dashboard view with bento grid."""

    def compose(self) -> ComposeResult:
        yield HeroArt(classes="bento-hero")
        yield QuickStats(id="quick-stats", classes="bento-gold")
        yield PantheonRow(id="pantheon-row", classes="bento")
        with Horizontal(classes="bento-row"):
            yield ExecLanes(id="exec-lanes", classes="bento")
            yield MemoryPreview(id="memory-preview", classes="bento")
        yield RecentSessions(id="recent-sessions", classes="bento")

    @work(thread=True)
    def load_data(self) -> None:
        from hermes_cli.dashboard.data import (
            get_recent_sessions, get_usage_stats,
            get_memory_entries, get_skin_pantheon,
        )
        sessions = get_recent_sessions(limit=8)
        stats = get_usage_stats()
        memories = get_memory_entries()
        pantheon = get_skin_pantheon()
        self.app.call_from_thread(self._apply_data, sessions, stats, memories, pantheon)

    def _apply_data(self, sessions, stats, memories, pantheon):
        self.query_one("#recent-sessions", RecentSessions).sessions = sessions
        self.query_one("#quick-stats", QuickStats).stats = stats
        self.query_one("#memory-preview", MemoryPreview).entries = memories
        if pantheon:
            self.query_one("#pantheon-row", PantheonRow).gods = pantheon

    def on_show(self) -> None:
        self.load_data()
