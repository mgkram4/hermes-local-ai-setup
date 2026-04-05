"""View 2: Chronicle -- Session history with epic divine scroll art and bento grid.

Features:
- Epic animated scroll hero art with Artemis (goddess of the hunt/search)
- Divine session list with rich formatting
- FTS5 powered search with Greek styling
- Activity sparklines and session stats
"""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static, Input, Button
from textual import work


# =============================================================================
# EPIC CHRONICLE HERO ART — Divine Scroll with Artemis
# =============================================================================

CHRONICLE_HERO_FRAME_1 = """\
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]
[dim #1A1A38]░░[/][#2A2A50]╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]                                                                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #32CD32]╔═══════════════════════════════════════╗[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀[/]       [bold #32CD32]║[/]  [bold #90EE90]📜 THE CHRONICLE 📜[/]              [bold #32CD32]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀[/]       [bold #32CD32]║[/]  [dim #00D4FF]Divine Session Archives[/]           [bold #32CD32]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#32CD32]⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀[/]       [bold #32CD32]╠═══════════════════════════════════════╣[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#32CD32]⠀⠀⠀⠀⣿⣿⣿⣿⣿[/][#90EE90]≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡[/][#32CD32]⣿⣿⣿⣿⣿⠀⠀⠀⠀[/]       [bold #32CD32]║[/]                                       [bold #32CD32]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#90EE90]⠀⠀⠀⠀⣿⣿⣿⣿⣿[/][dim #555577]  Ιστορία • History  [/][#90EE90]⣿⣿⣿⣿⣿⠀⠀⠀⠀[/]       [bold #32CD32]║[/]  [#32CD32]🏹[/] [dim #555577]ARTEMIS[/] — Huntress of Data    [bold #32CD32]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#90EE90]⠀⠀⠀⠀⣿⣿⣿⣿⣿[/][#32CD32]≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡[/][#90EE90]⣿⣿⣿⣿⣿⠀⠀⠀⠀[/]       [bold #32CD32]║[/]  [dim #00D4FF]search · track · recall[/]           [bold #32CD32]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#32CD32]⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀[/]       [bold #32CD32]║[/]                                       [bold #32CD32]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀[/]       [bold #32CD32]║[/]  [dim #555577]FTS5 Powered • Full Text Search[/]   [bold #32CD32]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀[/]       [bold #32CD32]╚═══════════════════════════════════════╝[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]                                                                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝[/][dim #1A1A38]░░[/]
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]\
"""


# =============================================================================
# WIDGETS
# =============================================================================

class ChronicleHero(Static):
    """Chronicle hero art widget."""
    
    def render(self) -> str:
        return CHRONICLE_HERO_FRAME_1


class SessionStats(Static):
    """Quick session stats bar."""
    
    stats: reactive[dict] = reactive(dict, always_update=True)
    
    def render(self) -> str:
        if not self.stats:
            return "[dim #555577]Consulting the archives...[/]"
        
        total = self.stats.get("total", 0)
        today = self.stats.get("today", 0)
        week = self.stats.get("week", 0)
        
        return (
            f"[bold #32CD32]📜 Total Decrees[/]  [bold #00FF99]{total}[/]"
            f"     [bold #32CD32]Today[/]  [bold #00D4FF]{today}[/]"
            f"     [bold #32CD32]This Week[/]  [bold #FFD700]{week}[/]"
        )


class SessionList(Static):
    """Divine session list with rich formatting."""
    
    sessions: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_timestamp, format_cost
        
        if not self.sessions:
            return "[dim #555577]The scrolls are empty. No decrees found.\n\nBegin your divine journey to fill the archives.[/]"

        lines = []
        for i, s in enumerate(self.sessions):
            ts = format_timestamp(s.get("last_active") or s.get("started_at", 0))
            model = (s.get("model") or "?").split("/")[-1][:16]
            title = s.get("title") or s.get("preview", "") or "untitled"
            title = title[:40]
            cost = format_cost(s.get("actual_cost_usd") or s.get("estimated_cost_usd") or 0)
            msgs = s.get("message_count", 0)
            tools = s.get("tool_call_count", 0)
            source = s.get("source", "cli")
            sid = s.get("id", "")[:8]

            # Alternating row colors
            row_color = "#E0F7FF" if i % 2 == 0 else "#C8E8FF"
            marker = "[#32CD32]§[/]" if i % 2 == 0 else "[#00A8CC]·[/]"
            
            # Tool indicator with color based on intensity
            tool_color = "#FF4444" if tools > 20 else "#FFD700" if tools > 10 else "#00D4FF"
            tool_indicator = f"[{tool_color}]⚔{tools}[/]"
            
            # Source icon
            source_icons = {"cli": "💻", "telegram": "📱", "discord": "🎮", "slack": "💬"}
            source_icon = source_icons.get(source, "📡")

            lines.append(
                f"  {marker}  [{row_color}]{ts:<14}[/]  "
                f"[#E0F7FF]{title:<40}[/]  "
                f"[dim #555577]{model:<16}[/]  "
                f"[dim #00D4FF]{msgs:>3}[/]  {tool_indicator}  "
                f"[#FFD700]{cost:>7}[/]  "
                f"{source_icon}  [dim #2A2A50]{sid}[/]"
            )
        
        return "\n".join(lines)


class SearchBox(Static):
    """Divine search box with styling."""
    
    def compose(self) -> ComposeResult:
        yield Input(
            placeholder="🏹 Hunt the archives... (Αναζήτηση — FTS5 powered)",
            id="search-input",
        )


class ChronicleView(ScrollableContainer):
    """The Chronicle -- Divine session history with epic hero art.
    
    Features:
    - Epic scroll hero art with Artemis theming
    - Session statistics bar
    - FTS5 powered search
    - Rich session list with tool indicators
    """

    def compose(self) -> ComposeResult:
        yield ChronicleHero(id="chronicle-hero", classes="hero-art")
        yield SessionStats(id="session-stats", classes="bento-gold")
        yield SearchBox(id="search-box", classes="divine-panel")
        yield Static(
            "  [dim #32CD32]TIME            TITLE" + " " * 24 + 
            "MODEL             MSGS  TOOLS    COST    SRC   ID[/]",
            classes="bento-gold",
        )
        yield SessionList(id="session-list", classes="divine-panel")

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
        
        # Calculate stats
        from datetime import datetime, timedelta
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        week_start = (now - timedelta(days=7)).timestamp()
        
        today_count = sum(1 for s in sessions if (s.get("last_active") or s.get("started_at", 0)) >= today_start)
        week_count = sum(1 for s in sessions if (s.get("last_active") or s.get("started_at", 0)) >= week_start)
        
        stats = {
            "total": len(sessions),
            "today": today_count,
            "week": week_count,
        }
        
        self.app.call_from_thread(self._apply, sessions, stats)

    @work(thread=True)
    def search(self, query: str) -> None:
        from hermes_cli.dashboard.data import search_sessions
        results = search_sessions(query, limit=30)
        
        stats = {
            "total": len(results),
            "today": 0,
            "week": 0,
        }
        
        self.app.call_from_thread(self._apply, results, stats)

    def _apply(self, sessions, stats):
        self.query_one("#session-list", SessionList).sessions = sessions
        self.query_one("#session-stats", SessionStats).stats = stats

    def on_show(self) -> None:
        self.load_data()
