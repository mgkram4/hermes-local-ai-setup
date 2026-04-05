"""OLYMPUS DASHBOARD — Interactive TUI for Hermes Agent.

A Textual application providing a full divine command center interface
with Greek temple aesthetics, real-time data, and mythological vibes.

Launch: `hermes dashboard` or `/dashboard` in the CLI.
"""

import os
import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static, Header, Footer, Button, Input, Label
from textual.screen import Screen
from textual import work

from hermes_cli.dashboard.views.assembly import AssemblyView
from hermes_cli.dashboard.views.chronicle import ChronicleView
from hermes_cli.dashboard.views.oracle import OracleView
from hermes_cli.dashboard.views.tablets import TabletsView
from hermes_cli.dashboard.views.deep_dive import DeepDiveView
from hermes_cli.dashboard.views.local_models import LocalModelsView
from hermes_cli.dashboard.views.model_switch import ModelSwitchView


VIEWS = [
    ("assembly", "\u2302 Assembly", "1"),
    ("chronicle", "\u270D Chronicle", "2"),
    ("oracle", "\u2609 Oracle", "3"),
    ("tablets", "\u2620 Tablets", "4"),
    ("deepdive", "\u2692 Deep Dive", "5"),
    ("local", "\u2668 Local Forge", "6"),
    ("switch", "\u2695 Switch", "7"),
]


class NavBar(Static):
    """Top navigation bar with Greek motif."""

    current_view: reactive[str] = reactive("assembly")

    def compose(self) -> ComposeResult:
        with Horizontal(id="nav-tabs"):
            yield Button(" \u25C0 ", id="back-btn")
            yield Static(
                " [bold #FFD700]\u2261[/] [bold #FFD700]OLYMPUS[/] [dim #1A1A3A]\u2502[/] ",
                id="header-title",
            )
            for view_id, label, key in VIEWS:
                btn = Button(f" {key}\u00B7{label} ", id=f"nav-{view_id}", classes="nav-button")
                if view_id == self.current_view:
                    btn.add_class("-active")
                yield btn
            yield Static(
                " [dim #555577]\u039B\u03B1\u03BA\u03B5\u03B4\u03B1\u03AF\u03BC\u03C9\u03BD[/] [dim #00D4FF]q[/]:quit ",
                id="header-status",
            )

    def watch_current_view(self, value: str) -> None:
        try:
            for view_id, _, _ in VIEWS:
                btn = self.query_one(f"#nav-{view_id}", Button)
                if view_id == value:
                    btn.add_class("-active")
                else:
                    btn.remove_class("-active")
        except Exception:
            pass


class StatusBar(Static):
    """Bottom status bar with Greek border."""

    def compose(self) -> ComposeResult:
        yield Static(
            "[dim #1A1A3A]\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393[/]  "
            "[dim #555577][1]\u2302  [2]\u270D  [3]\u2609  [4]\u2620  [5]\u2692  [6]\u2668  [7]\u2695[/]  "
            "[dim #1A1A3A]\u2502[/]  [dim #555577]q:quit  r:refresh  \u25C0:back[/]  "
            "[dim #1A1A3A]\u2502[/]  [bold #FFD700]\u2727[/] [dim #00D4FF]Olympus Online[/]  "
            "[dim #1A1A3A]\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393\u0393[/]",
            id="footer-bar",
        )


class OlympusDashboard(App):
    """The Olympus Dashboard — divine command center for Hermes Agent."""

    TITLE = "OLYMPUS // HERMES CONTROL SYSTEM"
    CSS_PATH = "styles.tcss"

    BINDINGS = [
        Binding("1", "switch_view('assembly')", "Assembly", show=False),
        Binding("2", "switch_view('chronicle')", "Chronicle", show=False),
        Binding("3", "switch_view('oracle')", "Oracle", show=False),
        Binding("4", "switch_view('tablets')", "Tablets", show=False),
        Binding("5", "switch_view('deepdive')", "Deep Dive", show=False),
        Binding("6", "switch_view('local')", "Local Forge", show=False),
        Binding("7", "switch_view('switch')", "Switch", show=False),
        Binding("escape", "go_back", "Back", show=False),
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh_data", "Refresh", show=False),
    ]

    current_view: reactive[str] = reactive("assembly")
    _view_history: list = []

    def compose(self) -> ComposeResult:
        yield NavBar()
        yield Container(
            AssemblyView(id="view-assembly"),
            ChronicleView(id="view-chronicle", classes="hidden"),
            OracleView(id="view-oracle", classes="hidden"),
            TabletsView(id="view-tablets", classes="hidden"),
            DeepDiveView(id="view-deepdive", classes="hidden"),
            LocalModelsView(id="view-local", classes="hidden"),
            ModelSwitchView(id="view-switch", classes="hidden"),
            id="main-content",
        )
        yield StatusBar()

    def on_mount(self) -> None:
        from hermes_cli.dashboard.data import _ensure_skin_loaded
        _ensure_skin_loaded()
        for view_id, _, _ in VIEWS:
            try:
                w = self.query_one(f"#view-{view_id}")
                if view_id == "assembly":
                    w.remove_class("hidden")
                    w.display = True
                else:
                    w.add_class("hidden")
                    w.display = False
            except Exception:
                pass
        self.refresh_all_views()

    def action_switch_view(self, view_name: str) -> None:
        if view_name != self.current_view:
            self._view_history.append(self.current_view)
        self.current_view = view_name

    def action_go_back(self) -> None:
        if self._view_history:
            prev = self._view_history.pop()
            self.current_view = prev
        else:
            self.current_view = "assembly"

    def watch_current_view(self, value: str) -> None:
        try:
            navbar = self.query_one(NavBar)
            navbar.current_view = value
        except Exception:
            return

        for view_id, _, _ in VIEWS:
            try:
                widget = self.query_one(f"#view-{view_id}")
                if view_id == value:
                    widget.remove_class("hidden")
                    widget.display = True
                else:
                    widget.add_class("hidden")
                    widget.display = False
            except Exception:
                pass

        try:
            active_view = self.query_one(f"#view-{value}")
            if hasattr(active_view, "on_show"):
                active_view.on_show()
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id or ""
        if btn_id == "back-btn":
            self.action_go_back()
        elif btn_id.startswith("nav-"):
            view_name = btn_id[4:]
            self.action_switch_view(view_name)

    def action_refresh_data(self) -> None:
        self.refresh_all_views()

    @work(thread=True)
    def refresh_all_views(self) -> None:
        try:
            view = self.query_one(f"#view-{self.current_view}")
            if hasattr(view, "load_data"):
                view.load_data()
        except Exception:
            pass


def run_dashboard():
    """Entry point for `hermes dashboard`."""
    app = OlympusDashboard()
    app.run()


if __name__ == "__main__":
    run_dashboard()
