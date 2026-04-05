"""View 2: Chronicle -- Session history with 8-bit scroll art and bento grid."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static, Input
from textual import work


SCROLL_ART = """\
[#15152D]              \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584              [/]
[#1A1A38]          \u2584\u2588\u2588\u2580[/][#222248]                                                    [/][#1A1A38]\u2580\u2588\u2588\u2584          [/]
[#1E1E40]        \u2584\u2588\u2580[/][#282850]    \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261    [/][#1E1E40]\u2580\u2588\u2584        [/]
[#222248]       \u2588\u2588[/][#303060]                                                        [/][#222248]\u2588\u2588       [/]
[#282850]       \u2588\u2588[/][#353568]    [/][#404078]\u0399\u03C3\u03C4\u03BF\u03C1\u03AF\u03B1[/][#353568]    [/][#404078]\u270D THE CHRONICLE[/][#353568]    [/][#404078]\u0399\u03C3\u03C4\u03BF\u03C1\u03AF\u03B1[/][#353568]    [/][#282850]\u2588\u2588       [/]
[#282850]       \u2588\u2588[/][#303060]                                                        [/][#282850]\u2588\u2588       [/]
[#222248]       \u2588\u2588[/][#282850]    \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261  \u2261    [/][#222248]\u2588\u2588       [/]
[#1E1E40]        \u2580\u2588\u2584[/][#222248]                                                    [/][#1E1E40]\u2584\u2588\u2580        [/]
[#15152D]              \u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580              [/]\
"""


class SessionList(Static):
    sessions: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_timestamp, format_cost
        if not self.sessions:
            return "[dim #555577]The scrolls are empty. No decrees found.[/]"

        lines = []
        for i, s in enumerate(self.sessions):
            ts = format_timestamp(s.get("last_active") or s.get("started_at", 0))
            model = (s.get("model") or "?").split("/")[-1][:18]
            title = s.get("title") or s.get("preview", "") or "untitled"
            title = title[:45]
            cost = format_cost(s.get("actual_cost_usd") or s.get("estimated_cost_usd") or 0)
            msgs = s.get("message_count", 0)
            source = s.get("source", "cli")
            sid = s.get("id", "")[:12]

            marker = "[dim #FFD700]\u00A7[/]" if i % 2 == 0 else "[dim #00A8CC]\u00B7[/]"

            lines.append(
                f"  {marker}  [{('#E0F7FF' if i % 2 == 0 else '#C8E8FF')}]{ts:<16}[/]  "
                f"[#E0F7FF]{title:<45}[/]  "
                f"[dim #555577]{model:<18}[/]  [dim #00D4FF]{msgs:>3} msgs[/]  "
                f"[dim #FFD700]{cost:>8}[/]  [dim #555577]{source:<6}[/]  "
                f"[dim #2A2A50]{sid}[/]"
            )
        return "\n".join(lines)


class ChronicleView(ScrollableContainer):
    """The Chronicle -- session history with bento layout."""

    def compose(self) -> ComposeResult:
        yield Static(SCROLL_ART, classes="bento-hero")
        yield Input(
            placeholder="\u2727 Search the archives... (\u0391\u03BD\u03B1\u03B6\u03AE\u03C4\u03B7\u03C3\u03B7 \u2014 FTS5 powered)",
            id="search-input",
        )
        yield Static(
            "  [dim #00A8CC]TIME              TITLE"
            + " " * 37
            + "MODEL              MSGS     COST    SRC       ID[/]",
            classes="bento-gold",
        )
        yield SessionList(id="session-list", classes="bento")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.value.strip()
        if query:
            self.search(query)
        else:
            self.load_data()

    @work(thread=True)
    def load_data(self) -> None:
        from hermes_cli.dashboard.data import get_recent_sessions
        sessions = get_recent_sessions(limit=50)
        self.app.call_from_thread(self._apply, sessions)

    @work(thread=True)
    def search(self, query: str) -> None:
        from hermes_cli.dashboard.data import search_sessions
        results = search_sessions(query, limit=30)
        self.app.call_from_thread(self._apply, results)

    def _apply(self, sessions):
        self.query_one("#session-list", SessionList).sessions = sessions

    def on_show(self) -> None:
        self.load_data()
