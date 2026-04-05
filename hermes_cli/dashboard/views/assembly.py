"""View 1: The Assembly -- OLYMPUS ASCENDED Home View.

Divine command center with:
- Epic animated 8-bit Hermes hero art with caduceus
- God Stats Leaderboard with rankings
- Interactive pantheon god cards with full details
- Live execution lanes with real tool call data
- Divine notifications panel
- Cost tracker widget
- Activity heatmap and sparklines
- Divine achievements system
"""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static, Button
from textual import work
import time


# =============================================================================
# EPIC HERO PIXEL ART — Divine Hermes with Caduceus Animation
# =============================================================================

HERMES_HERO_FRAME_1 = """\
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]
[dim #1A1A38]░░[/][#2A2A50]╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]                                                                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]╔═══════════════════════════════════════╗[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [bold #FFEC8B]⚡ OLYMPUS ASCENDED ⚡[/]            [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [dim #00D4FF]Divine Orchestration System[/]       [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]╠═══════════════════════════════════════╣[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#C9A227]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿[/][#FFD700]⚡[/][#C9A227]⣿⣿⣿⣿⣿⣿⣿⣿[/][#FFD700]⚡[/][#C9A227]⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]                                       [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [#C0C0C0]△[/] [dim #555577]ATHENA[/]    [#32CD32]🏹[/] [dim #555577]ARTEMIS[/]          [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [#DC143C]⚔[/] [dim #555577]ARES[/]      [#FF8C00]🔨[/] [dim #555577]HEPHAESTUS[/]       [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#C9A227]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [#1E90FF]🌊[/] [dim #555577]POSEIDON[/]  [#9B59B6]🕯[/] [dim #555577]HADES[/]            [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [#FFE066]☀[/] [dim #555577]APOLLO[/]    [#F0F0FF]👁[/] [dim #555577]ZEUS[/]             [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]                                       [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [bold #FFD700]⚕ HERMES[/] [dim #555577]— Divine Messenger[/]     [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [dim #00D4FF]route · spawn · synthesize[/]         [bold #FFD700]║[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#C9A227]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]╚═══════════════════════════════════════╝[/]      [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]║[/]                                                                                                              [#2A2A50]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#2A2A50]╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝[/][dim #1A1A38]░░[/]
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]\
"""

HERMES_HERO_FRAME_2 = """\
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]
[dim #1A1A38]░░[/][#3A3A6A]╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]                                                                                                              [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]╔═══════════════════════════════════════╗[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]  [bold #FFD700]✦ OLYMPUS ASCENDED ✦[/]            [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]  [dim #00D4FF]Divine Orchestration System[/]       [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]╠═══════════════════════════════════════╣[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿[/][#FFEC8B]✦[/][#FFD700]⣿⣿⣿⣿⣿⣿⣿⣿[/][#FFEC8B]✦[/][#FFD700]⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]                                       [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#FFEC8B]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]  [#C0C0C0]△[/] [dim #555577]ATHENA[/]    [#32CD32]🏹[/] [dim #555577]ARTEMIS[/]          [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#FFEC8B]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]  [#DC143C]⚔[/] [dim #555577]ARES[/]      [#FF8C00]🔨[/] [dim #555577]HEPHAESTUS[/]       [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]  [#1E90FF]🌊[/] [dim #555577]POSEIDON[/]  [#9B59B6]🕯[/] [dim #555577]HADES[/]            [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]  [#FFE066]☀[/] [dim #555577]APOLLO[/]    [#F0F0FF]👁[/] [dim #555577]ZEUS[/]             [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]                                       [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]  [bold #FFEC8B]⚕ HERMES[/] [dim #555577]— Divine Messenger[/]     [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#FFEC8B]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]║[/]  [dim #00D4FF]route · spawn · synthesize[/]         [bold #FFEC8B]║[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFEC8B]╚═══════════════════════════════════════╝[/]      [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [#555577]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]                                                              [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]                                                              [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]║[/]                                                                                                              [#3A3A6A]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#3A3A6A]╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝[/][dim #1A1A38]░░[/]
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]\
"""

HERMES_HERO_FRAME_3 = """\
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]
[dim #1A1A38]░░[/][#FFD700]╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]                                                                                                              [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]╔═══════════════════════════════════════╗[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [bold #FFD700]◈ OLYMPUS ASCENDED ◈[/]            [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [#C9A227]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [dim #00D4FF]Divine Orchestration System[/]       [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [#C9A227]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]╠═══════════════════════════════════════╣[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [#FFEC8B]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿[/][bold #FFD700]◈[/][#FFEC8B]⣿⣿⣿⣿⣿⣿⣿⣿[/][bold #FFD700]◈[/][#FFEC8B]⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]                                       [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [bold #FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [#C0C0C0]△[/] [dim #555577]ATHENA[/]    [#32CD32]🏹[/] [dim #555577]ARTEMIS[/]          [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [bold #FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [#DC143C]⚔[/] [dim #555577]ARES[/]      [#FF8C00]🔨[/] [dim #555577]HEPHAESTUS[/]       [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [#FFEC8B]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [#1E90FF]🌊[/] [dim #555577]POSEIDON[/]  [#9B59B6]🕯[/] [dim #555577]HADES[/]            [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [#C9A227]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [#FFE066]☀[/] [dim #555577]APOLLO[/]    [#F0F0FF]👁[/] [dim #555577]ZEUS[/]             [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]                                       [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [bold #FFD700]⚕ HERMES[/] [dim #555577]— Divine Messenger[/]     [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [bold #FFD700]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]║[/]  [dim #00D4FF]route · spawn · synthesize[/]         [bold #FFD700]║[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [#FFEC8B]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]       [bold #FFD700]╚═══════════════════════════════════════╝[/]      [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [#C9A227]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]                                                              [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]      [dim #3A3A6A]⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀[/]                                                              [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]║[/]                                                                                                              [#FFD700]║[/][dim #1A1A38]░░[/]
[dim #1A1A38]░░[/][#FFD700]╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝[/][dim #1A1A38]░░[/]
[dim #0A0A12]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[/]\
"""

HERO_FRAMES = [HERMES_HERO_FRAME_1, HERMES_HERO_FRAME_2, HERMES_HERO_FRAME_3]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _make_god_card_full(god: dict, stats: dict = None) -> str:
    """Create a full god card with icon, name, rank, role, face, and stats."""
    name = god.get("name", "?")
    icon = god.get("icon", "✦")
    rank = god.get("rank", "???")
    desc = god.get("desc", "")
    hat = god.get("hat", "")
    face = god.get("face", "(-_-)")
    
    calls = stats.get("calls", 0) if stats else 0
    status = stats.get("status", "idle") if stats else "idle"
    
    status_color = "#00FF99" if status == "active" else "#FFD700" if status == "ready" else "#555577"
    status_icon = "●" if status == "active" else "◐" if status == "ready" else "○"
    
    god_colors = {
        "Hermes": "#FFD700",
        "Athena": "#C0C0C0",
        "Apollo": "#FFE066",
        "Ares": "#DC143C",
        "Zeus": "#F0F0FF",
        "Hephaestus": "#FF8C00",
        "Artemis": "#32CD32",
        "Poseidon": "#1E90FF",
        "Hades": "#9B59B6",
        "Dionysus": "#FF00FF",
    }
    color = god_colors.get(name, "#FFD700")
    
    lines = [
        f"[{color}]{hat}[/]" if hat else "",
        f"[bold {color}]{icon}[/]  [bold #E0F7FF]{face}[/]",
        f"[bold {color}]{name}[/]",
        f"[dim #00A8CC]{rank}[/]",
        f"[dim #555577]{desc}[/]" if desc else "",
        f"[{status_color}]{status_icon}[/] [{status_color}]{calls} calls[/]" if calls > 0 else f"[{status_color}]{status_icon}[/] [dim #555577]idle[/]",
    ]
    return "\n".join(line for line in lines if line)


def _make_leaderboard_entry(rank: int, god: dict, stats: dict) -> str:
    """Create a leaderboard entry for a god."""
    name = god.get("name", "?")
    icon = god.get("icon", "✦")
    calls = stats.get("calls", 0)
    pct = stats.get("pct", 0)
    
    god_colors = {
        "Hermes": "#FFD700", "Athena": "#C0C0C0", "Apollo": "#FFE066",
        "Ares": "#DC143C", "Zeus": "#F0F0FF", "Hephaestus": "#FF8C00",
        "Artemis": "#32CD32", "Poseidon": "#1E90FF", "Hades": "#9B59B6",
        "Dionysus": "#FF00FF",
    }
    color = god_colors.get(name, "#FFD700")
    
    rank_colors = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}
    rank_color = rank_colors.get(rank, "#555577")
    rank_icon = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")
    
    bar_len = min(int(pct / 5), 20)
    bar = "█" * bar_len + "░" * (20 - bar_len)
    
    return (
        f"  [{rank_color}]{rank_icon:<3}[/]  [{color}]{icon}[/] [{color}]{name:<12}[/]  "
        f"[{color}]{bar}[/]  [bold #00FF99]{calls:>6}[/]  [dim #555577]{pct:>3}%[/]"
    )


def _make_exec_lane_live(lane: dict) -> str:
    """Create an execution lane display with live data."""
    name = lane.get("name", "UNKNOWN")
    god = lane.get("god", "Hermes")
    icon = lane.get("icon", "◈")
    color = lane.get("color", "#FFD700")
    calls = lane.get("calls", 0)
    pct = lane.get("pct", 0)
    latency = lane.get("latency_ms", 0)
    
    filled = int(pct / 100 * 20)
    bar = "█" * filled + "░" * (20 - filled)
    
    bar_color = "#00FF99" if pct > 60 else "#FFD700" if pct > 30 else "#FF4444" if pct > 0 else "#2A2A50"
    
    return (
        f"  [{color}]{icon}[/]  [bold #E0F7FF]{name:<12}[/]  "
        f"[dim #555577]{god:<12}[/]  "
        f"[{bar_color}]{bar}[/] [{bar_color}]{pct:>3}%[/]  "
        f"[dim #00D4FF]{calls:>5} calls[/]  "
        f"[dim #555577]{latency}ms[/]"
    )


def _make_notification(notif: dict, icons: dict) -> str:
    """Create a notification line with icon and message."""
    level = notif.get("level", "info")
    message = notif.get("message", "")
    ts = notif.get("timestamp", 0)
    
    from hermes_cli.dashboard.data import format_timestamp
    time_str = format_timestamp(ts)
    
    icon_map = {
        "info": icons.get("info_icon", "✦"),
        "warn": icons.get("warn_icon", "⚠"),
        "error": icons.get("error_icon", "⚡"),
        "success": icons.get("success_icon", "✓"),
    }
    color_map = {
        "info": "#00D4FF",
        "warn": "#FFD700",
        "error": "#FF4444",
        "success": "#00FF99",
    }
    
    icon = icon_map.get(level, "•")
    color = color_map.get(level, "#555577")
    
    return f"  [{color}]{icon}[/]  [dim #555577]{time_str}[/]  [{color}]{message}[/]"


def _make_activity_heatmap(daily_data: list) -> str:
    """Create a 14-day activity heatmap."""
    if not daily_data:
        return "[dim #555577]No activity data[/]"
    
    blocks = " ░▒▓█"
    max_sessions = max(d.get("sessions", 0) for d in daily_data) or 1
    
    heatmap = ""
    for d in daily_data[-14:]:
        sessions = d.get("sessions", 0)
        level = min(int((sessions / max_sessions) * 4), 4)
        color = ["#1A1A38", "#2A4A2A", "#3A6A3A", "#4A8A4A", "#00FF99"][level]
        heatmap += f"[{color}]{blocks[level]}[/]"
    
    return heatmap


def _make_sparkline(values: list, width: int = 20, color: str = "#00D4FF") -> str:
    """Create a sparkline from values."""
    if not values:
        return "[dim #1A1A38]" + "░" * width + "[/]"
    
    blocks = " ▁▂▃▄▅▆▇█"
    mx = max(values) if max(values) > 0 else 1
    
    padded = values[-width:] if len(values) >= width else values
    chars = []
    for v in padded:
        idx = min(int((v / mx) * (len(blocks) - 1)), len(blocks) - 1)
        chars.append(blocks[idx])
    
    return f"[{color}]{''.join(chars)}[/]"


# =============================================================================
# WIDGETS
# =============================================================================

class HeroArt(Static):
    """Animated hero art widget with frame cycling."""
    
    frame_index: reactive[int] = reactive(0)
    
    def render(self) -> str:
        frames = HERO_FRAMES
        if self.frame_index < len(frames):
            return frames[self.frame_index]
        return frames[0] if frames else ""
    
    def cycle_frame(self) -> None:
        self.frame_index = (self.frame_index + 1) % len(HERO_FRAMES)


class GodLeaderboard(Static):
    """God stats leaderboard with rankings."""
    
    activity: reactive[list] = reactive(list, always_update=True)
    
    def render(self) -> str:
        header = "[bold #FFD700]🏆 DIVINE LEADERBOARD — God Activity Rankings[/]\n\n"
        header += "  [dim #555577]RANK  GOD           ACTIVITY                  CALLS    %[/]\n"
        header += "  [dim #2A2A50]" + "─" * 70 + "[/]\n"
        
        if not self.activity:
            return header + "  [dim #555577]The gods are resting. No activity recorded.[/]"
        
        sorted_gods = sorted(self.activity, key=lambda x: x.get("calls", 0), reverse=True)
        
        lines = []
        for i, god in enumerate(sorted_gods[:10], 1):
            lines.append(_make_leaderboard_entry(i, god, god))
        
        total_calls = sum(g.get("calls", 0) for g in self.activity)
        footer = f"\n  [dim #2A2A50]{'─' * 70}[/]\n"
        footer += f"  [bold #FFD700]TOTAL DIVINE STRIKES:[/]  [bold #00FF99]{total_calls:,}[/]"
        
        return header + "\n".join(lines) + footer


class PantheonStrip(Static):
    """Compact pantheon strip showing all gods."""
    
    gods: reactive[list] = reactive(list, always_update=True)
    activity: reactive[dict] = reactive(dict, always_update=True)
    
    def render(self) -> str:
        if not self.gods:
            return "[dim #555577]Summoning the pantheon...[/]"
        
        activity_map = {g.get("name"): g for g in self.activity} if isinstance(self.activity, list) else {}
        
        god_colors = {
            "Hermes": "#FFD700", "Athena": "#C0C0C0", "Apollo": "#FFE066",
            "Ares": "#DC143C", "Zeus": "#F0F0FF", "Hephaestus": "#FF8C00",
            "Artemis": "#32CD32", "Poseidon": "#1E90FF", "Hades": "#9B59B6",
            "Dionysus": "#FF00FF",
        }
        
        parts = []
        for god in self.gods[:10]:
            name = god.get("name", "?")
            icon = god.get("icon", "✦")
            face = god.get("face", "(-_-)")
            color = god_colors.get(name, "#FFD700")
            
            stats = activity_map.get(name, {})
            calls = stats.get("calls", 0)
            status = stats.get("status", "idle")
            
            status_color = "#00FF99" if status == "active" else "#FFD700" if status == "ready" else "#555577"
            status_dot = "●" if status == "active" else "◐" if status == "ready" else "○"
            
            parts.append(
                f"[{color}]{icon}[/][{status_color}]{status_dot}[/]"
            )
        
        return "  ".join(parts)


class ExecutionLanes(Static):
    """Live execution lanes with real tool call data."""
    
    lanes: reactive[list] = reactive(list, always_update=True)
    
    def render(self) -> str:
        header = "[bold #FFD700]✦ EXECUTION LANES — Divine Tool Flow[/]\n\n"
        
        if not self.lanes:
            return header + "[dim #555577]The lanes are quiet. No tool calls recorded.[/]"
        
        lane_lines = [_make_exec_lane_live(lane) for lane in self.lanes]
        
        total_calls = sum(l.get("calls", 0) for l in self.lanes)
        footer = f"\n\n  [dim #555577]Total divine strikes: [bold #FFD700]{total_calls}[/][/]"
        
        return header + "\n".join(lane_lines) + footer


class ActivityDashboard(Static):
    """Activity dashboard with heatmap and sparklines."""
    
    daily_data: reactive[list] = reactive(list, always_update=True)
    stats: reactive[dict] = reactive(dict, always_update=True)
    
    def render(self) -> str:
        header = "[bold #FFD700]📊 ACTIVITY OVERVIEW[/]\n\n"
        
        heatmap = _make_activity_heatmap(self.daily_data)
        header += f"  [dim #00A8CC]14-Day Heatmap[/]  {heatmap}\n\n"
        
        if self.daily_data:
            sessions = [d.get("sessions", 0) for d in self.daily_data]
            messages = [d.get("messages", 0) for d in self.daily_data]
            costs = [d.get("cost", 0) for d in self.daily_data]
            
            header += f"  [dim #00A8CC]Sessions [/]  {_make_sparkline(sessions, 30, '#00FF99')}\n"
            header += f"  [dim #00A8CC]Messages [/]  {_make_sparkline(messages, 30, '#00D4FF')}\n"
            header += f"  [dim #00A8CC]Cost     [/]  {_make_sparkline(costs, 30, '#FFD700')}\n"
        
        return header


class DivineNotifications(Static):
    """Divine notifications panel showing recent events."""
    
    notifications: reactive[list] = reactive(list, always_update=True)
    
    def render(self) -> str:
        from hermes_cli.dashboard.data import get_skin_notifications_config
        icons = get_skin_notifications_config()
        
        header = "[bold #FFD700]⚕ DIVINE PROCLAMATIONS[/]\n\n"
        
        if not self.notifications:
            return header + "[dim #555577]The oracle is silent. No recent decrees.[/]"
        
        lines = [_make_notification(n, icons) for n in self.notifications[:8]]
        return header + "\n".join(lines)


class CostTracker(Static):
    """Drachmai cost tracker widget."""
    
    costs: reactive[dict] = reactive(dict, always_update=True)
    
    def render(self) -> str:
        from hermes_cli.dashboard.data import format_cost
        
        header = "[bold #FFD700]💰 ΔΡΑΧΜΑΙ — Divine Treasury[/]\n\n"
        
        if not self.costs:
            return header + "[dim #555577]Consulting the treasury...[/]"
        
        daily = self.costs.get("daily", 0)
        weekly = self.costs.get("weekly", 0)
        monthly = self.costs.get("monthly", 0)
        total = self.costs.get("total", 0)
        
        lines = [
            f"  [dim #00A8CC]Today[/]     [bold #00FF99]{format_cost(daily)}[/]",
            f"  [dim #00A8CC]Week[/]      [bold #00D4FF]{format_cost(weekly)}[/]",
            f"  [dim #00A8CC]Month[/]     [bold #FFD700]{format_cost(monthly)}[/]",
            f"  [dim #00A8CC]All Time[/]  [bold #FF4444]{format_cost(total)}[/]",
        ]
        
        model_breakdown = self.costs.get("model_breakdown", [])
        if model_breakdown:
            lines.append("")
            lines.append("  [dim #555577]─── By Model ───[/]")
            for m in model_breakdown[:3]:
                model_name = (m.get("model", "?")).split("/")[-1][:20]
                cost = format_cost(m.get("cost", 0))
                lines.append(f"  [dim #555577]{model_name:<20}[/]  [#FFD700]{cost}[/]")
        
        return header + "\n".join(lines)


class RecentSessions(Static):
    """Recent sessions list with divine styling."""
    
    sessions: reactive[list] = reactive(list, always_update=True)
    
    def render(self) -> str:
        from hermes_cli.dashboard.data import format_timestamp, format_cost
        
        header = "[bold #FFD700]📜 RECENT DECREES[/]\n\n"
        
        if not self.sessions:
            return header + "[dim #555577]No decrees yet. The scrolls await.[/]"
        
        lines = []
        for i, s in enumerate(self.sessions[:8]):
            ts = format_timestamp(s.get("last_active") or s.get("started_at", 0))
            model = (s.get("model") or "?").split("/")[-1][:14]
            title = (s.get("title") or s.get("preview", "") or "untitled")[:35]
            cost = format_cost(s.get("actual_cost_usd") or s.get("estimated_cost_usd") or 0)
            msgs = s.get("message_count", 0)
            tools = s.get("tool_call_count", 0)
            
            marker = "[#FFD700]§[/]" if i % 2 == 0 else "[#00A8CC]·[/]"
            tool_indicator = f"[#FF4444]⚔{tools}[/]" if tools > 10 else f"[dim #555577]⚔{tools}[/]"
            
            lines.append(
                f"  {marker}  [dim #00A8CC]{ts:<12}[/]  [#E0F7FF]{title:<35}[/]  "
                f"[dim #555577]{model:<14}[/]  [dim #00D4FF]{msgs:>3}[/]  {tool_indicator}  [#FFD700]{cost}[/]"
            )
        
        return header + "\n".join(lines)


class QuickStats(Static):
    """Quick stats bar with divine metrics."""
    
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
            f"[bold #FFD700]Σεσσιονς[/]  [bold #00FF99]{sessions}[/]"
            f"     [bold #FFD700]Μεσσαγες[/]  [bold #00FF99]{messages}[/]"
            f"     [bold #FFD700]Εργαλεία[/]  [bold #00FF99]{tools}[/]"
            f"     [bold #FFD700]Μάρκες[/]  [bold #00D4FF]{format_tokens(tokens)}[/]"
            f"     [bold #FFD700]Δραχμαί[/]  [bold #FFD700]{format_cost(cost)}[/]"
        )


class ModelStatus(Static):
    """Quick model status showing current active model."""
    
    model_info: reactive[dict] = reactive(dict, always_update=True)
    lms_status: reactive[str] = reactive("checking")
    
    def render(self) -> str:
        from hermes_cli.dashboard.data import format_tokens
        
        model = self.model_info.get("model", "unknown")
        provider = self.model_info.get("provider", "unknown")
        ctx = self.model_info.get("context_length")
        
        if "openrouter" in provider.lower():
            provider_icon = "🌐"
            provider_color = "#00D4FF"
            provider_label = "OpenRouter"
        elif "lmstudio" in provider.lower() or "custom:" in provider.lower():
            provider_icon = "🖥"
            provider_color = "#00FF99"
            provider_label = "LM Studio"
        elif "ollama" in provider.lower():
            provider_icon = "🦙"
            provider_color = "#FF8C00"
            provider_label = "Ollama"
        else:
            provider_icon = "⚡"
            provider_color = "#FFD700"
            provider_label = provider.split(":")[-1] if ":" in provider else provider
        
        model_short = model.split("/")[-1] if "/" in model else model
        if len(model_short) > 25:
            model_short = model_short[:22] + "..."
        
        ctx_str = f"  [dim #555577]{ctx//1024}K ctx[/]" if ctx else ""
        
        lms_indicator = ""
        if self.lms_status == "online":
            lms_indicator = "  [#00FF99]● LMS[/]"
        elif self.lms_status == "offline":
            lms_indicator = "  [#FF4444]○ LMS[/]"
        
        return (
            f"[bold #FFD700]⚕ ACTIVE MODEL[/]  "
            f"[{provider_color}]{provider_icon} {provider_label}[/]  "
            f"[bold #E0F7FF]{model_short}[/]"
            f"{ctx_str}{lms_indicator}"
        )


class MemoryPreview(Static):
    """Memory preview widget."""
    
    entries: reactive[list] = reactive(list, always_update=True)
    
    def render(self) -> str:
        header = "[bold #FFD700]🕯 ΜΝΗΜΗ — Divine Memory[/]\n\n"
        
        if not self.entries:
            return header + "[dim #555577]The tablets are blank.[/]"
        
        lines = []
        for entry in self.entries[:5]:
            text = entry[:50] + ("..." if len(entry) > 50 else "")
            lines.append(f"  [dim #00D4FF]§[/] [dim #E0F7FF]{text}[/]")
        
        return header + "\n".join(lines)


class DivineAchievements(Static):
    """Divine achievements/badges widget."""
    
    stats: reactive[dict] = reactive(dict, always_update=True)
    
    def render(self) -> str:
        header = "[bold #FFD700]🏅 DIVINE ACHIEVEMENTS[/]\n\n"
        
        if not self.stats:
            return header + "[dim #555577]No achievements yet.[/]"
        
        sessions = self.stats.get("total_sessions", 0)
        messages = self.stats.get("total_messages", 0)
        tools = self.stats.get("total_tool_calls", 0)
        
        achievements = []
        
        if sessions >= 100:
            achievements.append(("[#FFD700]🌟[/]", "Century", "100+ sessions"))
        elif sessions >= 50:
            achievements.append(("[#C0C0C0]⭐[/]", "Veteran", "50+ sessions"))
        elif sessions >= 10:
            achievements.append(("[#CD7F32]✦[/]", "Initiate", "10+ sessions"))
        
        if tools >= 1000:
            achievements.append(("[#FFD700]⚔[/]", "Forge Master", "1000+ tool calls"))
        elif tools >= 500:
            achievements.append(("[#C0C0C0]🔨[/]", "Craftsman", "500+ tool calls"))
        elif tools >= 100:
            achievements.append(("[#CD7F32]🛠[/]", "Apprentice", "100+ tool calls"))
        
        if messages >= 1000:
            achievements.append(("[#FFD700]📜[/]", "Chronicler", "1000+ messages"))
        elif messages >= 500:
            achievements.append(("[#C0C0C0]📝[/]", "Scribe", "500+ messages"))
        
        if not achievements:
            return header + "  [dim #555577]Begin your divine journey to earn badges![/]"
        
        lines = []
        for icon, name, desc in achievements:
            lines.append(f"  {icon}  [bold #E0F7FF]{name}[/]  [dim #555577]{desc}[/]")
        
        return header + "\n".join(lines)


# =============================================================================
# MAIN VIEW
# =============================================================================

class AssemblyView(ScrollableContainer):
    """The Assembly — OLYMPUS ASCENDED main dashboard view.
    
    Features:
    - Epic animated hero art with Hermes
    - Quick model status with LM Studio / OpenRouter indicator
    - God Stats Leaderboard with rankings
    - Compact pantheon strip
    - Live execution lanes
    - Activity dashboard with heatmap
    - Divine notifications
    - Cost tracker
    - Recent sessions
    - Divine achievements
    """
    
    _animation_timer = None
    
    def compose(self) -> ComposeResult:
        yield HeroArt(id="hero-art", classes="hero-art")
        yield ModelStatus(id="model-status", classes="bento-gold")
        yield QuickStats(id="quick-stats", classes="bento-gold")
        yield PantheonStrip(id="pantheon-strip", classes="divine-panel")
        yield GodLeaderboard(id="god-leaderboard", classes="divine-panel-gold")
        with Horizontal(classes="bento-row"):
            yield ExecutionLanes(id="exec-lanes", classes="divine-panel")
            yield ActivityDashboard(id="activity-dashboard", classes="divine-panel")
        with Horizontal(classes="bento-row"):
            yield RecentSessions(id="recent-sessions", classes="divine-panel")
            with Vertical():
                yield CostTracker(id="cost-tracker", classes="divine-panel-gold")
                yield DivineAchievements(id="achievements", classes="divine-panel")
        yield DivineNotifications(id="notifications", classes="divine-panel")
    
    @work(thread=True)
    def load_data(self) -> None:
        """Load all dashboard data from the data layer."""
        from hermes_cli.dashboard.data import (
            get_recent_sessions, get_usage_stats,
            get_memory_entries, get_skin_pantheon,
            get_execution_lane_stats, get_pantheon_activity,
            get_recent_notifications, get_cost_breakdown,
            get_daily_activity, get_active_model_info, get_lmstudio_models,
        )
        
        sessions = get_recent_sessions(limit=8)
        stats = get_usage_stats()
        memories = get_memory_entries()
        pantheon = get_skin_pantheon()
        lanes = get_execution_lane_stats()
        activity = get_pantheon_activity()
        notifications = get_recent_notifications(limit=6)
        costs = get_cost_breakdown(days=30)
        daily = get_daily_activity(days=14)
        
        model_info = get_active_model_info()
        lms_models = get_lmstudio_models("http://localhost:1234/v1")
        lms_status = "online" if lms_models else "offline"
        
        self.app.call_from_thread(
            self._apply_data, 
            sessions, stats, memories, pantheon, 
            lanes, activity, notifications, costs, daily,
            model_info, lms_status
        )
    
    def _apply_data(self, sessions, stats, memories, pantheon, lanes, activity, notifications, costs, daily, model_info, lms_status):
        """Apply loaded data to widgets."""
        self.query_one("#recent-sessions", RecentSessions).sessions = sessions
        self.query_one("#quick-stats", QuickStats).stats = stats
        
        model_widget = self.query_one("#model-status", ModelStatus)
        model_widget.model_info = model_info
        model_widget.lms_status = lms_status
        
        if pantheon:
            strip = self.query_one("#pantheon-strip", PantheonStrip)
            strip.gods = pantheon
            strip.activity = activity
        
        leaderboard = self.query_one("#god-leaderboard", GodLeaderboard)
        leaderboard.activity = activity
        
        self.query_one("#exec-lanes", ExecutionLanes).lanes = lanes
        self.query_one("#notifications", DivineNotifications).notifications = notifications
        self.query_one("#cost-tracker", CostTracker).costs = costs
        
        activity_dash = self.query_one("#activity-dashboard", ActivityDashboard)
        activity_dash.daily_data = daily
        activity_dash.stats = stats
        
        self.query_one("#achievements", DivineAchievements).stats = stats
    
    def on_show(self) -> None:
        """Called when the view is shown."""
        self.load_data()
        self._start_animation()
    
    def on_hide(self) -> None:
        """Called when the view is hidden."""
        self._stop_animation()
    
    def _start_animation(self) -> None:
        """Start the hero art animation timer."""
        if self._animation_timer is None:
            self._animation_timer = self.set_interval(2.5, self._animate_hero)
    
    def _stop_animation(self) -> None:
        """Stop the hero art animation timer."""
        if self._animation_timer is not None:
            self._animation_timer.stop()
            self._animation_timer = None
    
    def _animate_hero(self) -> None:
        """Cycle the hero art frame."""
        try:
            hero = self.query_one("#hero-art", HeroArt)
            hero.cycle_frame()
        except Exception:
            pass
