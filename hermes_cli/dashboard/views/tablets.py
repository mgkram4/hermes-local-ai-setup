"""View 4: The Tablets -- Memory viewer with 8-bit stone tablet art and bento grid."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static
from textual import work


TABLET_ART = """\
[#15152D]          \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584              \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584          [/]
[#1A1A38]         \u2588[/][#222248]                 [/][#1A1A38]\u2588            \u2588[/][#222248]                 [/][#1A1A38]\u2588         [/]
[#1E1E40]         \u2588[/][#282850]  \u2261 \u2261 \u2261 \u2261 \u2261 \u2261  [/][#1E1E40]\u2588            \u2588[/][#282850]  \u2261 \u2261 \u2261 \u2261 \u2261 \u2261  [/][#1E1E40]\u2588         [/]
[#222248]         \u2588[/][#303060]  \u2261 \u2261 \u2261 \u2261 \u2261 \u2261  [/][#222248]\u2588            \u2588[/][#303060]  \u2261 \u2261 \u2261 \u2261 \u2261 \u2261  [/][#222248]\u2588         [/]
[#282850]         \u2588[/][#353568]  \u039C\u039D\u0397\u039C\u0397  MEMORY [/][#282850]\u2588            \u2588[/][#353568]  \u03A0\u03A1\u039F\u03A6\u0399\u039B  USER   [/][#282850]\u2588         [/]
[#282850]         \u2588[/][#303060]  \u2261 \u2261 \u2261 \u2261 \u2261 \u2261  [/][#282850]\u2588            \u2588[/][#303060]  \u2261 \u2261 \u2261 \u2261 \u2261 \u2261  [/][#282850]\u2588         [/]
[#222248]         \u2588[/][#282850]  \u2261 \u2261 \u2261 \u2261 \u2261 \u2261  [/][#222248]\u2588            \u2588[/][#282850]  \u2261 \u2261 \u2261 \u2261 \u2261 \u2261  [/][#222248]\u2588         [/]
[#1A1A38]         \u2588[/][#222248]                 [/][#1A1A38]\u2588            \u2588[/][#222248]                 [/][#1A1A38]\u2588         [/]
[#15152D]          \u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580              \u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580          [/]\
"""


class MemoryTablet(Static):
    entries: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        header = "[bold #FFD700]\u039C\u039D\u0397\u039C\u0397 \u2014 AGENT MEMORY[/]  [dim #00A8CC]MEMORY.md[/]\n\n"
        if not self.entries:
            return header + "[dim #555577]The tablets are empty.\nHermes has not yet carved any memories.[/]"
        lines = []
        for i, entry in enumerate(self.entries):
            lines.append(f"[dim #FFD700]\u2560\u2550\u2550 \u00A7 {i + 1} \u2550\u2550\u2563[/]")
            for line in entry.split("\n"):
                lines.append(f"[dim #2A2A50]\u2551[/]  [#E0F7FF]{line}[/]")
            lines.append(f"[dim #2A2A50]\u2551[/]")
        return header + "\n".join(lines)


class UserTablet(Static):
    entries: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        header = "[bold #00D4FF]\u03A0\u03A1\u039F\u03A6\u0399\u039B \u2014 USER PROFILE[/]  [dim #00A8CC]USER.md[/]\n\n"
        if not self.entries:
            return header + "[dim #555577]No user profile entries yet.[/]"
        lines = []
        for i, entry in enumerate(self.entries):
            lines.append(f"[dim #00D4FF]\u2560\u2550\u2550 \u00A7 {i + 1} \u2550\u2550\u2563[/]")
            for line in entry.split("\n"):
                lines.append(f"[dim #2A2A50]\u2551[/]  [#E0F7FF]{line}[/]")
            lines.append(f"[dim #2A2A50]\u2551[/]")
        return header + "\n".join(lines)


class TabletsView(ScrollableContainer):
    """The Tablets -- memory viewer with bento grid."""

    def compose(self) -> ComposeResult:
        yield Static(TABLET_ART, classes="bento-hero")
        with Horizontal(classes="bento-row"):
            yield MemoryTablet(id="memory-tablet", classes="bento")
            yield UserTablet(id="user-tablet", classes="bento")

    @work(thread=True)
    def load_data(self) -> None:
        from hermes_cli.dashboard.data import get_memory_entries, get_user_entries
        memories = get_memory_entries()
        user = get_user_entries()
        self.app.call_from_thread(self._apply, memories, user)

    def _apply(self, memories, user):
        self.query_one("#memory-tablet", MemoryTablet).entries = memories
        self.query_one("#user-tablet", UserTablet).entries = user

    def on_show(self) -> None:
        self.load_data()
