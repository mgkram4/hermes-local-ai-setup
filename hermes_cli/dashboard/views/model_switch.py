"""View 7: Model Switchboard -- Epic Hermes art with divine model switching.

Features:
- Epic Hermes hero art (messenger god - model routing)
- Hermes braille pixel art portrait
- Active model panel with divine styling
- LM Studio status panel
- Configured providers list
- Model switch input with context length
"""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static, Input
from textual import work
import random


# =============================================================================
# EPIC MODEL SWITCH HERO ART — Hermes' Divine Caduceus
# =============================================================================

SWITCH_HERO_FRAME_1 = """\
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]
[dim #1A1A38]░░[/][#2A2A50]╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]                                                                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]╔═══════════════════════════════════════╗[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [bold #FFEC8B]⚕ MODEL SWITCHBOARD ⚕[/]          [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [dim #00D4FF]Divine Model Routing[/]               [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#C9A227]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]╠═══════════════════════════════════════╣[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿[/][#FFEC8B]⚕[/][#FFD700]⣿⣿⣿⣿⣿⣿⣿⣿[/][#FFEC8B]⚕[/][#FFD700]⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]                                       [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#FFEC8B]⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [#FFD700]⚕[/] [dim #555577]HERMES[/] — Divine Messenger     [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#FFEC8B]⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [dim #00D4FF]route · switch · connect[/]          [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#C9A227]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]                                       [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [dim #555577]LM Studio • OpenRouter • Custom[/]   [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]╚═══════════════════════════════════════╝[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]                                                                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝[/][dim #1A1A38]░░[/]
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]\
"""


# =============================================================================
# WIDGETS
# =============================================================================

class SwitchHero(Static):
    """Model switch hero art widget."""
    
    def render(self) -> str:
        return SWITCH_HERO_FRAME_1


class ActiveModelPanel(Static):
    """Shows the current active model config with divine styling."""
    
    info: reactive[dict] = reactive(dict, always_update=True)

    def render(self) -> str:
        header = "[bold #FFD700]⚕ ACTIVE MODEL[/]\n\n"
        
        if not self.info:
            return header + "[dim #555577]Loading...[/]"
        
        model = self.info.get("model", "?")
        provider = self.info.get("provider", "?")
        base_url = self.info.get("base_url", "")
        ctx = self.info.get("context_length")
        
        # Provider styling
        if "openrouter" in provider.lower():
            provider_icon = "🌐"
            provider_color = "#00D4FF"
        elif "lmstudio" in provider.lower() or "custom:" in provider.lower():
            provider_icon = "🖥"
            provider_color = "#00FF99"
        elif "ollama" in provider.lower():
            provider_icon = "🦙"
            provider_color = "#FF8C00"
        else:
            provider_icon = "⚡"
            provider_color = "#FFD700"
        
        ctx_line = ""
        if ctx:
            ctx_line = f"\n  [dim #555577]Context: {ctx:,} tokens ({ctx // 1024}K)[/]"
        
        return (
            header
            + f"  [{provider_color}]{provider_icon}[/] [bold #00FF99]{model}[/]\n"
            + f"  [dim #00A8CC]{provider}[/]\n"
            + f"  [dim #555577]{base_url}[/]"
            + ctx_line
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
    """Status message display."""
    
    message: reactive[str] = reactive("")

    def render(self) -> str:
        return f"\n{self.message}\n" if self.message else ""


class HermesPortrait(Static):
    """Hermes pixel art portrait with lore and abilities."""
    
    god_data: reactive[dict] = reactive(dict, always_update=True)
    
    def render(self) -> str:
        if not self.god_data:
            return "[dim #555577]Summoning the Divine Messenger...[/]"
        
        pixel_art = self.god_data.get("pixel_art", "")
        abilities = self.god_data.get("abilities", [])
        quotes = self.god_data.get("quotes", [])
        
        content = ""
        if pixel_art:
            content += pixel_art + "\n"
        
        if abilities:
            content += "\n[bold #FFD700]DIVINE POWERS:[/]\n"
            for ability in abilities[:3]:
                content += f"  [dim #FFEC8B]{ability}[/]\n"
        
        if quotes:
            quote = random.choice(quotes)
            content += f"\n[italic dim #555577]\"{quote}\"[/]"
        
        return content


class ModelSwitchView(ScrollableContainer):
    """Model Switchboard -- Divine model routing with Hermes hero art.
    
    Features:
    - Epic Hermes hero art
    - Hermes braille pixel art portrait
    - Active model panel
    - LM Studio status
    - Configured providers list
    - Model switch input
    """

    def compose(self) -> ComposeResult:
        yield SwitchHero(id="switch-hero", classes="hero-art")
        with Horizontal(classes="bento-row"):
            yield HermesPortrait(id="hermes-portrait", classes="divine-panel-gold")
            yield ActiveModelPanel(id="active-model", classes="divine-panel-gold")
            yield LMStudioPanel(id="lms-panel", classes="divine-panel-gold")
        yield ProvidersPanel(id="providers-panel", classes="divine-panel")
        yield Static(
            "[bold #FFD700]⚕ SWITCH MODEL[/]  "
            "[dim #00A8CC]Enter model name as shown in LM Studio / config. "
            "Context = max tokens (optional: leave blank for default 32K)[/]",
            classes="bento-gold",
        )
        with Horizontal(id="switch-row", classes="divine-panel"):
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
            self._set_status("[bold #FF4444]✗ Enter a model name[/]")
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
                "[bold #FF4444]✗ No custom providers configured in config.yaml[/]",
            )
            return
        
        tokens, err = resolve_dashboard_context_input(
            ctx_inp.value, target, model_id,
        )
        
        if err:
            self._set_status(f"[bold #FF4444]✗ {err}[/]")
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
                f"[bold #00FF99]✓ Switched to {model_id}[/]  "
                f"[dim #00A8CC]({context_length:,} ctx) via {target} "
                f"— restart hermes to use[/]"
            )
        else:
            msg = f"[bold #FF4444]✗ Failed to switch to {model_id}[/]"
        
        self.app.call_from_thread(self._set_status, msg)
        self.app.call_from_thread(self.load_data)

    def _set_status(self, msg: str) -> None:
        self.query_one("#switch-status", StatusMessage).message = msg

    @work(thread=True)
    def load_data(self) -> None:
        from hermes_cli.dashboard.data import (
            get_active_model_info, get_custom_providers, get_lmstudio_models,
            get_god_detail,
        )
        
        active = get_active_model_info()
        providers = get_custom_providers()
        hermes_data = get_god_detail("Hermes")

        # Find LM Studio URLs
        lms_urls = set()
        for p in providers:
            url = p.get("base_url", "")
            if "localhost" in url or "127.0.0.1" in url:
                lms_urls.add(url)
        if not lms_urls:
            lms_urls.add("http://localhost:1234/v1")

        # Check LM Studio connection
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

        # Build LM Studio panel content
        if lms_online:
            lines = [f"[bold #00FF99]● LM STUDIO ONLINE[/]  [dim #00A8CC]{lms_url}[/]\n"]
            for m in lms_models:
                mid = m.get("id", "?")
                lines.append(f"  [bold #E0F7FF]⚕ {mid}[/]")
            lms_text = "\n".join(lines)
        else:
            lms_text = (
                f"[bold #FF4444]○ LM STUDIO OFFLINE[/]  [dim #00A8CC]{lms_url}[/]\n\n"
                f"[dim #555577]Start LM Studio to see loaded models[/]"
            )

        # Build providers panel content
        active_model = active.get("model", "")
        active_pname = active.get("provider_name", "")
        
        prov_lines = ["[bold #FFD700]ΓΝΩΣΤΟΙ — CONFIGURED PROVIDERS[/]\n"]
        
        for p in providers:
            pname = p.get("name", "?")
            purl = p.get("base_url", "")
            models = p.get("models", [])
            is_active_prov = pname == active_pname
            
            badge = "[bold #00FF99]◆ ACTIVE[/]" if is_active_prov else "[dim #555577]◇[/]"
            prov_lines.append(f"  {badge}  [bold #FFD700]{pname}[/]  [dim #00A8CC]{purl}[/]")
            
            for m in models:
                mid = m.get("id", "?")
                ctx = m.get("context_length", 0)
                ctx_str = f"  {ctx // 1024}K" if ctx else ""
                is_current = is_active_prov and mid == active_model
                marker = "[bold #00FF99]→[/]" if is_current else "[dim #2A2A50]│[/]"
                prov_lines.append(f"      {marker}  [#E0F7FF]{mid}[/][dim #555577]{ctx_str}[/]")
            
            prov_lines.append("")
        
        prov_text = "\n".join(prov_lines)

        self.app.call_from_thread(self._apply, active, lms_text, prov_text, hermes_data)

    def _apply(self, active: dict, lms_text: str, prov_text: str, hermes_data: dict) -> None:
        self.query_one("#active-model", ActiveModelPanel).info = active
        self.query_one("#lms-panel", LMStudioPanel).content = lms_text
        self.query_one("#providers-panel", ProvidersPanel).content = prov_text
        
        if hermes_data:
            self.query_one("#hermes-portrait", HermesPortrait).god_data = hermes_data
        
        model_inp = self.query_one("#switch-input-model", Input)
        ctx_inp = self.query_one("#switch-input-context", Input)
        model_inp.value = active.get("model") or ""
        ctx = active.get("context_length")
        ctx_inp.value = str(ctx) if ctx else ""

    def on_show(self) -> None:
        self.load_data()
