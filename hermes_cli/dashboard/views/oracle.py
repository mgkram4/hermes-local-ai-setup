"""View 3: The Oracle -- Cost analytics with 8-bit Apollo eye and bento grid."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static
from textual import work


APOLLO_ART = """\
[#15152D]                                    \u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584                                    [/]
[#1A1A38]                               \u2584\u2580\u2580[/][#222248]             [/][#1A1A38]\u2580\u2580\u2584                               [/]
[#1E1E40]                          \u2584\u2580\u2580[/][#282850]     \u2584\u2584\u2584\u2584\u2584\u2584\u2584     [/][#1E1E40]\u2580\u2580\u2584                          [/]
[#222248]                      \u2584\u2580\u2580[/][#303060]    \u2584\u2588\u2580\u2580[/][#383870]       [/][#303060]\u2580\u2580\u2588\u2584    [/][#222248]\u2580\u2580\u2584                      [/]
[#282850]                  \u2584\u2580[/][#353568]      \u2588\u2588[/][#404078]   [/][#484888]\u2584\u2584\u2584\u2584\u2584[/][#404078]   [/][#353568]\u2588\u2588      [/][#282850]\u2580\u2584                  [/]
[#303060]                \u2584\u2580[/][#383870]      \u2588\u2588[/][#484888]  \u2588\u2588[/][#555599]\u2609[/][#484888]\u2588\u2588\u2588\u2588\u2588[/][#383870]  \u2588\u2588      [/][#303060]\u2580\u2584                [/]
[#282850]                  \u2580\u2584[/][#353568]      \u2588\u2588[/][#404078]   [/][#484888]\u2580\u2580\u2580\u2580\u2580[/][#404078]   [/][#353568]\u2588\u2588      [/][#282850]\u2584\u2580                  [/]
[#222248]                      \u2580\u2584\u2584[/][#303060]    \u2580\u2588\u2584\u2584[/][#383870]       [/][#303060]\u2584\u2584\u2588\u2580    [/][#222248]\u2584\u2584\u2580                      [/]
[#1E1E40]                          \u2580\u2584\u2584[/][#282850]     \u2580\u2580\u2580\u2580\u2580\u2580\u2580     [/][#1E1E40]\u2584\u2584\u2580                          [/]
[#1A1A38]                               \u2580\u2584\u2584[/][#222248]             [/][#1A1A38]\u2584\u2584\u2580                               [/]
[#15152D]                                    \u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580                                    [/]\
"""


def _sparkline(values: list, width: int = 40, color: str = "#00D4FF") -> str:
    blocks = " \u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"
    if not values:
        empty = '\u2591' * width
        return f"[dim #1A1A3A]{empty}[/]"
    mx = max(values) if max(values) > 0 else 1
    padded = values[-width:] if len(values) >= width else values
    chars = []
    for v in padded:
        idx = min(int((v / mx) * (len(blocks) - 1)), len(blocks) - 1)
        chars.append(blocks[idx])
    return f"[{color}]{''.join(chars)}[/]"


class StatCard(Static):
    label: reactive[str] = reactive("")
    value: reactive[str] = reactive("\u2014")
    sub: reactive[str] = reactive("")
    greek: reactive[str] = reactive("")

    def render(self) -> str:
        gk = f"[dim #2A2A50]{self.greek}[/]\n" if self.greek else ""
        return (
            gk
            + f"[bold #FFD700]{self.label}[/]\n"
            f"[bold #00FF99]{self.value}[/]\n"
            f"[dim #555577]{self.sub}[/]"
        )


class ActivityChart(Static):
    activity: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        header = "[bold #FFD700]\u0393\u03A1\u0391\u03A6\u0397\u039C\u0391  Activity \u2014 Last 14 Days[/]\n\n"
        if not self.activity:
            return header + "[dim #555577]The oracle has no visions yet.[/]"
        session_vals = [d.get("sessions", 0) for d in self.activity]
        msg_vals = [d.get("messages", 0) for d in self.activity]
        cost_vals = [d.get("cost", 0) for d in self.activity]
        lines = [
            f"  [dim #00A8CC]Sessions [/]  {_sparkline(session_vals, 50, '#00FF99')}",
            f"  [dim #00A8CC]Messages [/]  {_sparkline(msg_vals, 50, '#00D4FF')}",
            f"  [dim #00A8CC]Cost     [/]  {_sparkline(cost_vals, 50, '#FFD700')}",
        ]
        day_labels = "  [dim #555577]"
        for d in self.activity:
            day_labels += d.get("day", "")[-5:] + " "
        day_labels += "[/]"
        return header + "\n".join(lines) + "\n" + day_labels


class ModelTable(Static):
    models: reactive[list] = reactive(list, always_update=True)

    def render(self) -> str:
        from hermes_cli.dashboard.data import format_tokens, format_cost
        header = "[bold #FFD700]\u039C\u039F\u039D\u03A4\u0395\u039B  Model Breakdown[/]\n\n"
        if not self.models:
            return header + "[dim #555577]No model data yet.[/]"
        col_header = (
            "  [dim #00A8CC]MODEL"
            + " " * 30
            + "SESSIONS    TOKENS         COST[/]\n"
            + "  [dim #2A2A50]" + "\u2500" * 70 + "[/]"
        )
        lines = [col_header]
        for m in self.models:
            model_name = m.get("model", "unknown")[:35]
            sessions = m.get("sessions", 0)
            tokens = format_tokens(m.get("total_tokens", 0))
            cost = format_cost(m.get("cost", 0))
            bar_len = min(sessions, 30)
            bar = "\u2588" * bar_len + "\u2591" * (30 - bar_len)
            lines.append(
                f"  [#E0F7FF]{model_name:<35}[/]  "
                f"[#00FF99]{sessions:>5}[/]    "
                f"[#00D4FF]{tokens:>8}[/]    "
                f"[#FFD700]{cost:>8}[/]\n"
                f"  [dim #00D4FF]{bar}[/]"
            )
        return header + "\n".join(lines)


class OracleView(ScrollableContainer):
    """The Oracle -- analytics with bento grid and Apollo eye art."""

    def compose(self) -> ComposeResult:
        yield Static(APOLLO_ART, classes="bento-hero")
        with Horizontal(id="stats-row"):
            yield StatCard(id="stat-sessions", classes="stat-card")
            yield StatCard(id="stat-tokens", classes="stat-card")
            yield StatCard(id="stat-cost", classes="stat-card")
            yield StatCard(id="stat-tools", classes="stat-card")
        yield ActivityChart(id="activity-chart", classes="bento")
        yield ModelTable(id="model-table", classes="bento")

    @work(thread=True)
    def load_data(self) -> None:
        from hermes_cli.dashboard.data import (
            get_usage_stats, get_daily_activity, get_model_breakdown,
            format_tokens, format_cost,
        )
        stats = get_usage_stats()
        activity = get_daily_activity(14)
        models = get_model_breakdown()
        self.app.call_from_thread(self._apply, stats, activity, models)

    def _apply(self, stats, activity, models):
        from hermes_cli.dashboard.data import format_tokens, format_cost
        total_tokens = stats.get("total_input_tokens", 0) + stats.get("total_output_tokens", 0)
        s = self.query_one("#stat-sessions", StatCard)
        s.greek = "\u03A3\u03C5\u03BD\u03B5\u03B4\u03C1\u03AF\u03B5\u03C2"
        s.label = "SESSIONS"
        s.value = str(stats.get("total_sessions", 0))
        s.sub = f"{stats.get('total_messages', 0)} msgs"
        t = self.query_one("#stat-tokens", StatCard)
        t.greek = "\u039C\u03AC\u03C1\u03BA\u03B5\u03C2"
        t.label = "TOKENS"
        t.value = format_tokens(total_tokens)
        t.sub = f"in:{format_tokens(stats.get('total_input_tokens', 0))} out:{format_tokens(stats.get('total_output_tokens', 0))}"
        c = self.query_one("#stat-cost", StatCard)
        c.greek = "\u0394\u03C1\u03B1\u03C7\u03BC\u03B1\u03AF"
        c.label = "COST"
        c.value = format_cost(stats.get("total_cost", 0))
        c.sub = "all time"
        tl = self.query_one("#stat-tools", StatCard)
        tl.greek = "\u0395\u03C1\u03B3\u03B1\u03BB\u03B5\u03AF\u03B1"
        tl.label = "TOOL CALLS"
        tl.value = str(stats.get("total_tool_calls", 0))
        tl.sub = "all sessions"
        self.query_one("#activity-chart", ActivityChart).activity = activity
        self.query_one("#model-table", ModelTable).models = models

    def on_show(self) -> None:
        self.load_data()
