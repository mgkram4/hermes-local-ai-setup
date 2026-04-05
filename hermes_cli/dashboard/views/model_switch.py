"""View 7: Model Switchboard -- Type model name to switch."""

from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static, Input
from textual import work


CADUCEUS_ART = """\
[#15152D]                                        \u2584\u2584\u2584\u2584\u2584                                        [/]
[#1A1A38]                                      \u2588\u2588[/][#222248]\u2695[/][#1A1A38]\u2588\u2588                                      [/]
[#1E1E40]                                       \u2580\u2588\u2588\u2580                                       [/]
[#222248]                                        \u2588\u2588                                        [/]
[#1E1E40]                            \u2584\u2584\u2584\u2584\u2584       \u2588\u2588       \u2584\u2584\u2584\u2584\u2584                            [/]
[#222248]                        \u2584\u2588\u2588\u2580[/][#282850]     [/][#222248]\u2580\u2584   \u2588\u2588   \u2584\u2580[/][#282850]     [/][#222248]\u2580\u2588\u2588\u2584                        [/]
[#282850]                       \u2588\u2580[/][#303060]         [/][#282850]\u2580\u2584 \u2588\u2588 \u2584\u2580[/][#303060]         [/][#282850]\u2580\u2588                       [/]
[#303060]                        \u2580\u2588\u2584[/][#353568]       [/][#303060]\u2580\u2588\u2588\u2588\u2580[/][#353568]       [/][#303060]\u2584\u2588\u2580                        [/]
[#282850]                          \u2580\u2588\u2588\u2584[/][#353568]     [/][#282850]\u2588\u2588[/][#353568]     [/][#282850]\u2584\u2588\u2588\u2580                          [/]
[#222248]                        \u2584\u2588\u2580[/][#303060]       [/][#222248]\u2584\u2588\u2588\u2584[/][#303060]       [/][#222248]\u2580\u2588\u2584                        [/]
[#1E1E40]                       \u2588\u2584[/][#282850]         [/][#1E1E40]\u2584\u2580\u2588\u2588\u2580\u2584[/][#282850]         [/][#1E1E40]\u2584\u2588                       [/]
[#1A1A38]                        \u2580\u2588\u2588\u2584[/][#222248]     [/][#1A1A38]\u2584\u2580 \u2588\u2588 \u2580\u2584[/][#222248]     [/][#1A1A38]\u2584\u2588\u2588\u2580                        [/]
[#15152D]                            \u2580\u2580\u2580\u2580\u2580  \u2580    \u2588\u2588    \u2580  \u2580\u2580\u2580\u2580\u2580                            [/]
[#15152D]                                       \u2584\u2588\u2588\u2584                                       [/]
[#15152D]                                     \u2580\u2580\u2580\u2580\u2580\u2580\u2580                                     [/]\
"""


class ActiveModelPanel(Static):
    """Shows the current active model config."""
    info: reactive[dict] = reactive(dict, always_update=True)

    def render(self) -> str:
        if not self.info:
            return "[dim #555577]Loading...[/]"
        model = self.info.get("model", "?")
        provider = self.info.get("provider", "?")
        base_url = self.info.get("base_url", "")
        ctx = self.info.get("context_length")
        ctx_line = ""
        if ctx:
            ctx_line = f"\n  [dim #555577]context: {ctx} tokens[/]"
        return (
            f"[bold #FFD700]\u2695 ACTIVE MODEL[/]\n\n"
            f"  [bold #00FF99]\u25C6 {model}[/]\n"
            f"  [dim #00A8CC]{provider}[/]\n"
            f"  [dim #555577]{base_url}[/]"
            f"{ctx_line}"
        )


class LMStudioPanel(Static):
    """Shows LM Studio connection status and loaded models."""
    content: reactive[str] = reactive("", always_update=True)

    def render(self) -> str:
        return self.content or "[dim #555577]Checking LM Studio...[/]"


class ProvidersPanel(Static):
    """Shows all configured providers and their models."""
    content: reactive[str] = reactive("", always_update=True)

    def render(self) -> str:
        return self.content or "[dim #555577]Loading providers...[/]"


class StatusMessage(Static):
    message: reactive[str] = reactive("")

    def render(self) -> str:
        return f"\n{self.message}\n" if self.message else ""


class ModelSwitchView(ScrollableContainer):
    """Model Switchboard -- type model name to switch."""

    def compose(self) -> ComposeResult:
        yield Static(CADUCEUS_ART, classes="bento-hero")
        with Horizontal(classes="bento-row"):
            yield ActiveModelPanel(id="active-model", classes="bento")
            yield LMStudioPanel(id="lms-panel", classes="bento")
        yield ProvidersPanel(id="providers-panel", classes="bento")
        yield Static(
            "[bold #FFD700]\u2695 SWITCH MODEL[/]  "
            "[dim #00A8CC]Model name as in LM Studio / config; context = max tokens "
            "(optional: leave blank to keep existing or default 32K)[/]",
            classes="bento-gold",
        )
        with Horizontal(id="switch-row"):
            yield Input(
                placeholder="Model id (e.g. gemma-4-e4b-it)",
                id="switch-input-model",
            )
            yield Input(
                placeholder="Context (e.g. 131072 or 128k)",
                id="switch-input-context",
            )
        yield StatusMessage(id="switch-status")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id not in ("switch-input-model", "switch-input-context"):
            return
        model_inp = self.query_one("#switch-input-model", Input)
        ctx_inp = self.query_one("#switch-input-context", Input)
        model_id = model_inp.value.strip()
        if not model_id:
            self._set_status("[bold #FF4444]\u2717 Enter a model name[/]")
            return
        from hermes_cli.dashboard.data import (
            get_custom_providers,
            resolve_dashboard_context_input,
        )
        providers = get_custom_providers()
        lms_providers = [
            p for p in providers
            if "localhost:1234" in p.get("base_url", "") or "lmstudio" in p.get("name", "").lower()
        ]
        if lms_providers:
            target = lms_providers[0]["name"]
        elif providers:
            target = providers[0]["name"]
        else:
            self._set_status(
                "[bold #FF4444]\u2717 No custom providers configured in config.yaml[/]",
            )
            return
        tokens, err = resolve_dashboard_context_input(
            ctx_inp.value, target, model_id,
        )
        if err:
            self._set_status(f"[bold #FF4444]\u2717 {err}[/]")
            return
        self._do_switch(model_id, tokens, target)

    @work(thread=True)
    def _do_switch(self, model_id: str, context_length: int, target: str) -> None:
        from hermes_cli.dashboard.data import (
            switch_active_model, ensure_provider_has_model,
        )

        ensure_provider_has_model(target, model_id, context_length)
        ok = switch_active_model(model_id, target)
        if ok:
            msg = (
                f"[bold #00FF99]\u2713 Switched to {model_id}[/]  "
                f"[dim #00A8CC]({context_length} ctx) via {target} "
                f"\u2014 restart hermes to use[/]"
            )
        else:
            msg = f"[bold #FF4444]\u2717 Failed to switch to {model_id}[/]"
        self.app.call_from_thread(self._set_status, msg)
        self.app.call_from_thread(self.load_data)

    def _set_status(self, msg: str) -> None:
        self.query_one("#switch-status", StatusMessage).message = msg

    @work(thread=True)
    def load_data(self) -> None:
        from hermes_cli.dashboard.data import (
            get_active_model_info, get_custom_providers, get_lmstudio_models,
        )
        active = get_active_model_info()
        providers = get_custom_providers()

        lms_urls = set()
        for p in providers:
            url = p.get("base_url", "")
            if "localhost" in url or "127.0.0.1" in url:
                lms_urls.add(url)
        if not lms_urls:
            lms_urls.add("http://localhost:1234/v1")

        lms_models = []
        lms_online = False
        lms_url = ""
        for url in sorted(lms_urls):
            models = get_lmstudio_models(url)
            if models:
                lms_models = models
                lms_online = True
                lms_url = url
                break
            lms_url = url

        if lms_online:
            lines = [f"[bold #00FF99]\u25CF LM STUDIO ONLINE[/]  [dim #00A8CC]{lms_url}[/]\n"]
            for m in lms_models:
                mid = m.get("id", "?")
                lines.append(f"  [bold #E0F7FF]\u2692 {mid}[/]")
            lms_text = "\n".join(lines)
        else:
            lms_text = (
                f"[bold #FF4444]\u25CF LM STUDIO OFFLINE[/]  [dim #00A8CC]{lms_url}[/]\n\n"
                f"[dim #555577]Start LM Studio to see loaded models[/]"
            )

        active_model = active.get("model", "")
        active_pname = active.get("provider_name", "")
        prov_lines = ["[bold #FFD700]\u0393\u039D\u03A9\u03A3\u03A4\u039F\u0399 \u2014 CONFIGURED PROVIDERS[/]\n"]
        for p in providers:
            pname = p.get("name", "?")
            purl = p.get("base_url", "")
            models = p.get("models", [])
            is_active_prov = pname == active_pname
            badge = "[bold #00FF99]\u25C6 ACTIVE[/]" if is_active_prov else "[dim #555577]\u25C7[/]"
            prov_lines.append(f"  {badge}  [bold #FFD700]{pname}[/]  [dim #00A8CC]{purl}[/]")
            for m in models:
                mid = m.get("id", "?")
                ctx = m.get("context_length", 0)
                ctx_str = f"  {ctx // 1024}K" if ctx else ""
                is_current = is_active_prov and mid == active_model
                marker = "[bold #00FF99]\u2192[/]" if is_current else "[dim #2A2A50]\u2502[/]"
                prov_lines.append(f"      {marker}  [#E0F7FF]{mid}[/][dim #555577]{ctx_str}[/]")
            prov_lines.append("")
        prov_text = "\n".join(prov_lines)

        self.app.call_from_thread(self._apply, active, lms_text, prov_text)

    def _apply(self, active: dict, lms_text: str, prov_text: str) -> None:
        self.query_one("#active-model", ActiveModelPanel).info = active
        self.query_one("#lms-panel", LMStudioPanel).content = lms_text
        self.query_one("#providers-panel", ProvidersPanel).content = prov_text
        model_inp = self.query_one("#switch-input-model", Input)
        ctx_inp = self.query_one("#switch-input-context", Input)
        model_inp.value = active.get("model") or ""
        ctx = active.get("context_length")
        ctx_inp.value = str(ctx) if ctx else ""

    def on_show(self) -> None:
        self.load_data()
