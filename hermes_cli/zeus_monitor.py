"""Zeus Monitor — Standalone dashboard to watch Hermes activity.

Run in a separate terminal to monitor your active Hermes session:
    hermes zeus

Shows:
- Live session notes (what Hermes is doing)
- Zeus Overseer evaluations (task completion status)
- Recent tool calls and files modified
- Real-time updates every 2 seconds
"""

import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# Rich for beautiful terminal output
try:
    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
    from rich.layout import Layout
    from rich.text import Text
    from rich import box
except ImportError:
    print("Zeus Monitor requires 'rich'. Install with: pip install rich")
    sys.exit(1)


def get_hermes_home() -> Path:
    """Get the Hermes home directory."""
    return Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))


def get_latest_session_notes() -> dict:
    """Load the most recent session notes file."""
    sessions_dir = get_hermes_home() / "sessions"
    if not sessions_dir.exists():
        return {}
    
    # Find the most recent notes file
    notes_files = sorted(sessions_dir.glob("notes_*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not notes_files:
        return {}
    
    latest_notes = notes_files[0]
    try:
        content = latest_notes.read_text(encoding="utf-8")
    except Exception:
        return {}
    
    # Parse the notes file
    session_id = ""
    model = ""
    turns = []
    overseer_evals = []
    
    # Extract session ID from header
    session_match = re.search(r"SESSION NOTES: (\S+)", content)
    if session_match:
        session_id = session_match.group(1)
    
    # Extract model
    model_match = re.search(r"Model: (.+)", content)
    if model_match:
        model = model_match.group(1).strip()
    
    # Parse turns
    turn_blocks = re.split(r"-{50,}", content)
    for block in turn_blocks:
        turn_match = re.search(r"TURN (\d+) \| (\d+:\d+:\d+)", block)
        if turn_match:
            turn_num = int(turn_match.group(1))
            timestamp = turn_match.group(2)
            
            user_match = re.search(r"USER: (.+?)(?:\n|$)", block)
            user_msg = user_match.group(1).strip() if user_match else ""
            
            tools = re.findall(r"→ (\w+)", block)
            files = re.findall(r"• (.+\.(?:py|js|ts|yaml|json|md|txt))", block)
            
            response_match = re.search(r"RESPONSE: (.+?)(?:\n|$)", block)
            response = response_match.group(1).strip() if response_match else ""
            
            turns.append({
                "turn": turn_num,
                "timestamp": timestamp,
                "user": user_msg,
                "tools": tools[:6],
                "files": files[:5],
                "response": response,
            })
        
        # Parse Zeus Overseer evaluations
        zeus_match = re.search(r"\[(\d+:\d+:\d+)\] ZEUS_OVERSEER: (.+)", block)
        if zeus_match:
            overseer_evals.append({
                "timestamp": zeus_match.group(1),
                "message": zeus_match.group(2),
            })
    
    return {
        "session_id": session_id,
        "model": model,
        "turns": turns,
        "overseer_evals": overseer_evals,
        "file_path": str(latest_notes),
        "file_mtime": latest_notes.stat().st_mtime,
    }


def get_overseer_config() -> dict:
    """Load overseer config."""
    try:
        from hermes_cli.config import load_config
        config = load_config()
        return config.get("overseer", {})
    except Exception:
        return {}


def build_layout(data: dict, overseer_cfg: dict) -> Layout:
    """Build the dashboard layout."""
    layout = Layout()
    
    # Split into left (main) and right (overseer) panels
    layout.split_row(
        Layout(name="main", ratio=2),
        Layout(name="overseer", ratio=1),
    )
    
    # Main panel: Session notes
    layout["main"].split_column(
        Layout(name="header", size=3),
        Layout(name="turns", ratio=3),
        Layout(name="activity", ratio=1),
    )
    
    # Header
    session_id = data.get("session_id", "No active session")[:40]
    model = data.get("model", "unknown")
    header_text = Text()
    header_text.append("⚡ HERMES MONITOR", style="bold yellow")
    header_text.append(f"  │  Session: {session_id}", style="dim")
    header_text.append(f"  │  Model: {model}", style="dim cyan")
    layout["header"].update(Panel(header_text, box=box.SIMPLE))
    
    # Turns panel
    turns = data.get("turns", [])
    turns_table = Table(box=box.SIMPLE, expand=True, show_header=True)
    turns_table.add_column("#", style="yellow", width=4)
    turns_table.add_column("Time", style="dim", width=8)
    turns_table.add_column("User", style="white", ratio=2)
    turns_table.add_column("Tools", style="cyan", ratio=1)
    turns_table.add_column("Response", style="dim", ratio=2)
    
    for turn in turns[-8:]:  # Last 8 turns
        tools_str = ", ".join(turn.get("tools", [])[:3])
        if len(turn.get("tools", [])) > 3:
            tools_str += "..."
        
        user_short = turn.get("user", "")[:40]
        if len(turn.get("user", "")) > 40:
            user_short += "..."
        
        resp_short = turn.get("response", "")[:35]
        if len(turn.get("response", "")) > 35:
            resp_short += "..."
        
        turns_table.add_row(
            str(turn.get("turn", "?")),
            turn.get("timestamp", ""),
            user_short,
            tools_str,
            resp_short,
        )
    
    if not turns:
        turns_table.add_row("-", "-", "No turns yet", "-", "-")
    
    layout["turns"].update(Panel(turns_table, title="[bold yellow]📜 Session Turns[/]", border_style="yellow"))
    
    # Activity panel (recent files)
    all_files = []
    for turn in turns[-5:]:
        all_files.extend(turn.get("files", []))
    unique_files = list(dict.fromkeys(all_files))[-6:]  # Last 6 unique files
    
    files_text = Text()
    if unique_files:
        for f in unique_files:
            short = f.split("/")[-1] if "/" in f else f
            files_text.append(f"  📝 {short}\n", style="green")
    else:
        files_text.append("  No files modified yet", style="dim")
    
    layout["activity"].update(Panel(files_text, title="[bold green]Recent Files[/]", border_style="green"))
    
    # Overseer panel
    overseer_content = Text()
    
    enabled = overseer_cfg.get("enabled", False)
    overseer_model = overseer_cfg.get("model", "unknown")
    
    if enabled:
        overseer_content.append("● ACTIVE\n", style="bold green")
        overseer_content.append(f"Model: {overseer_model}\n\n", style="dim")
    else:
        overseer_content.append("○ DISABLED\n", style="bold red")
        overseer_content.append("Enable in config.yaml\n\n", style="dim")
    
    # Show overseer evaluations
    evals = data.get("overseer_evals", [])
    if evals:
        overseer_content.append("Recent Evaluations:\n", style="bold white")
        for ev in evals[-5:]:
            msg = ev.get("message", "")
            ts = ev.get("timestamp", "")
            
            if "COMPLETE" in msg.upper():
                overseer_content.append(f"  ✓ ", style="green")
            else:
                overseer_content.append(f"  ⚡ ", style="yellow")
            
            overseer_content.append(f"{ts} ", style="dim")
            # Truncate long messages
            msg_short = msg[:40] + "..." if len(msg) > 40 else msg
            overseer_content.append(f"{msg_short}\n", style="white")
    else:
        overseer_content.append("No evaluations yet.\n", style="dim")
        overseer_content.append("Complete a turn to see\n", style="dim")
        overseer_content.append("Zeus's assessment.", style="dim")
    
    layout["overseer"].update(Panel(
        overseer_content, 
        title="[bold white]👁 ZEUS OVERSEER[/]", 
        border_style="white"
    ))
    
    return layout


def run_monitor():
    """Run the Zeus monitor dashboard."""
    console = Console()
    
    console.print("\n[bold yellow]⚡ ZEUS MONITOR[/] — Watching Hermes activity")
    console.print("[dim]Press Ctrl+C to exit[/]\n")
    
    overseer_cfg = get_overseer_config()
    last_mtime = 0
    
    try:
        with Live(console=console, refresh_per_second=0.5, screen=True) as live:
            while True:
                data = get_latest_session_notes()
                
                # Check if file changed
                current_mtime = data.get("file_mtime", 0)
                if current_mtime != last_mtime:
                    last_mtime = current_mtime
                    # Reload overseer config in case it changed
                    overseer_cfg = get_overseer_config()
                
                layout = build_layout(data, overseer_cfg)
                live.update(layout)
                
                time.sleep(2)
    except KeyboardInterrupt:
        console.print("\n[dim]Zeus Monitor stopped.[/]")


def main():
    """Entry point for the zeus command."""
    run_monitor()


if __name__ == "__main__":
    main()
