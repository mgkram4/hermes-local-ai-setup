"""View 4: The Tablets -- Memory viewer with epic divine stone tablet art.

Features:
- Epic Hades hero art (god of the underworld/hidden knowledge)
- Divine memory tablet with rich formatting
- User profile tablet with personality insights
- Memory statistics and entry counts
"""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static
from textual import work


# =============================================================================
# EPIC TABLETS HERO ART — Hades' Divine Archives
# =============================================================================

TABLETS_HERO_FRAME_1 = """\
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]
[dim #1A1A38]░░[/][#2A2A50]╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]                                                                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀[/]       [bold #9B59B6]╔═══════════════════════════════════════╗[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀[/]       [bold #9B59B6]║[/]  [bold #DDA0DD]🕯 THE TABLETS 🕯[/]               [bold #9B59B6]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀[/]       [bold #9B59B6]║[/]  [dim #00D4FF]Divine Memory Archives[/]             [bold #9B59B6]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#9B59B6]⠀⠀⠀⠀⣿⣿⣿[/][dim #555577]  ≡ ≡ ≡ ≡ ≡ ≡  [/][#9B59B6]⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿[/][dim #555577]  ≡ ≡ ≡ ≡ ≡ ≡  [/][#9B59B6]⣿⣿⣿⠀⠀⠀⠀[/]       [bold #9B59B6]╠═══════════════════════════════════════╣[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#9B59B6]⠀⠀⠀⠀⣿⣿⣿[/][dim #555577]  ΜΝΗΜΗ MEMORY [/][#9B59B6]⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿[/][dim #555577]  ΠΡΟΦΙΛ  USER  [/][#9B59B6]⣿⣿⣿⠀⠀⠀⠀[/]       [bold #9B59B6]║[/]                                       [bold #9B59B6]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#DDA0DD]⠀⠀⠀⠀⣿⣿⣿[/][dim #555577]  ≡ ≡ ≡ ≡ ≡ ≡  [/][#DDA0DD]⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿[/][dim #555577]  ≡ ≡ ≡ ≡ ≡ ≡  [/][#DDA0DD]⣿⣿⣿⠀⠀⠀⠀[/]       [bold #9B59B6]║[/]  [#9B59B6]🕯[/] [dim #555577]HADES[/] — Keeper of Secrets    [bold #9B59B6]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#DDA0DD]⠀⠀⠀⠀⣿⣿⣿[/][dim #555577]  ≡ ≡ ≡ ≡ ≡ ≡  [/][#DDA0DD]⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿[/][dim #555577]  ≡ ≡ ≡ ≡ ≡ ≡  [/][#DDA0DD]⣿⣿⣿⠀⠀⠀⠀[/]       [bold #9B59B6]║[/]  [dim #00D4FF]remember · learn · persist[/]        [bold #9B59B6]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#9B59B6]⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀[/]       [bold #9B59B6]║[/]                                       [bold #9B59B6]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀[/]       [bold #9B59B6]║[/]  [dim #555577]MEMORY.md • USER.md[/]              [bold #9B59B6]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀[/]       [bold #9B59B6]╚═══════════════════════════════════════╝[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]                                                                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝[/][dim #1A1A38]░░[/]
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]\
"""


# =============================================================================
# WIDGETS
# =============================================================================

class TabletsHero(Static):
    """Tablets hero art widget."""
    
    def render(self) -> str:
        return TABLETS_HERO_FRAME_1


class MemoryStats(Static):
    """Memory statistics bar."""
    
    stats: reactive[dict] = reactive(dict, always_update=True)
    
    def render(self) -> str:
        if not self.stats:
            return "[dim #555577]Consulting the archives...[/]"
        
        memory_count = self.stats.get("memory_count", 0)
        user_count = self.stats.get("user_count", 0)
        total_chars = self.stats.get("total_chars", 0)
        
        return (
            f"[bold #9B59B6]🕯 Memory Entries[/]  [bold #DDA0DD]{memory_count}[/]"
            f"     [bold #9B59B6]User Entries[/]  [bold #00D4FF]{user_count}[/]"
            f"     [bold #9B59B6]Total Characters[/]  [bold #FFD700]{total_chars:,}[/]"
        )


class MemoryTablet(Static):
    """Divine memory tablet with rich formatting."""
    
    entries: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        header = "[bold #9B59B6]🕯 ΜΝΗΜΗ — AGENT MEMORY[/]  [dim #00A8CC]MEMORY.md[/]\n\n"
        
        if not self.entries:
            return header + (
                "[dim #555577]The tablets are empty.\n"
                "Hermes has not yet carved any memories.\n\n"
                "Memories are created when the agent learns\n"
                "important information during conversations.[/]"
            )
        
        lines = []
        for i, entry in enumerate(self.entries):
            # Entry header with divine styling
            lines.append(f"[#9B59B6]╔══ § {i + 1} ══════════════════════════════════════════╗[/]")
            
            # Entry content
            for line in entry.split("\n"):
                if line.strip():
                    lines.append(f"[#9B59B6]║[/]  [#E0F7FF]{line}[/]")
                else:
                    lines.append(f"[#9B59B6]║[/]")
            
            lines.append(f"[#9B59B6]╚══════════════════════════════════════════════════════╝[/]")
            lines.append("")
        
        return header + "\n".join(lines)


class UserTablet(Static):
    """Divine user profile tablet with rich formatting."""
    
    entries: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        header = "[bold #00D4FF]👤 ΠΡΟΦΙΛ — USER PROFILE[/]  [dim #00A8CC]USER.md[/]\n\n"
        
        if not self.entries:
            return header + (
                "[dim #555577]No user profile entries yet.\n\n"
                "User profile entries are created when\n"
                "the agent learns about you and your\n"
                "preferences during conversations.[/]"
            )
        
        lines = []
        for i, entry in enumerate(self.entries):
            # Entry header with divine styling
            lines.append(f"[#00D4FF]╔══ § {i + 1} ══════════════════════════════════════════╗[/]")
            
            # Entry content
            for line in entry.split("\n"):
                if line.strip():
                    lines.append(f"[#00D4FF]║[/]  [#E0F7FF]{line}[/]")
                else:
                    lines.append(f"[#00D4FF]║[/]")
            
            lines.append(f"[#00D4FF]╚══════════════════════════════════════════════════════╝[/]")
            lines.append("")
        
        return header + "\n".join(lines)


class TabletsView(ScrollableContainer):
    """The Tablets -- Divine memory viewer with epic hero art.
    
    Features:
    - Epic Hades hero art (keeper of secrets)
    - Memory statistics bar
    - Divine memory tablet with rich formatting
    - User profile tablet with personality insights
    """

    def compose(self) -> ComposeResult:
        yield TabletsHero(id="tablets-hero", classes="hero-art")
        yield MemoryStats(id="memory-stats", classes="bento-gold")
        with Horizontal(classes="bento-row"):
            yield MemoryTablet(id="memory-tablet", classes="divine-panel")
            yield UserTablet(id="user-tablet", classes="divine-panel")

    @work(thread=True)
    def load_data(self) -> None:
        from hermes_cli.dashboard.data import get_memory_entries, get_user_entries
        memories = get_memory_entries()
        user = get_user_entries()
        
        # Calculate stats
        memory_chars = sum(len(e) for e in memories)
        user_chars = sum(len(e) for e in user)
        
        stats = {
            "memory_count": len(memories),
            "user_count": len(user),
            "total_chars": memory_chars + user_chars,
        }
        
        self.app.call_from_thread(self._apply, memories, user, stats)

    def _apply(self, memories, user, stats):
        self.query_one("#memory-tablet", MemoryTablet).entries = memories
        self.query_one("#user-tablet", UserTablet).entries = user
        self.query_one("#memory-stats", MemoryStats).stats = stats

    def on_show(self) -> None:
        self.load_data()
