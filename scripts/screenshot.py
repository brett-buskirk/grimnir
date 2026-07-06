#!/usr/bin/env python3
# screenshot.py — regenerate the README hero (docs/grimnir-survey.png).
#
# Renders a REPRESENTATIVE `grimnir survey` (illustrative fake acme-* data, not a
# live run — a real survey aggregates the beasts, exposing the estate's actual repos
# and open security alerts) into a clean terminal-window PNG matching the rest of the
# toolkit's shots. Uses the same acme-* example estate as huginn/muninn/geri/freki.
#
# Dev-only.  pip3 install --user rich cairosvg  &&  python3 scripts/screenshot.py
import os, tempfile
from rich.console import Console
from rich.text import Text
import cairosvg

LINES = [
    "",
    "  [bold]grimnir survey[/]  [dim]· consolidated estate briefing · ~/github-repos · Sun Jul 6, 09:14[/]",
    "",
    "  [bold cyan]── present ──[/]",
    "",
    "  [bold]git estate[/]  [dim]·  ~/github-repos  ·  Sun Jul 6, 09:14[/]",
    "",
    "  [bold]REPO         BRANCH              LAST  STATUS[/]",
    "  [dim]────────────────────────────────────────────────────────[/]",
    "  [bold]acme-web[/]     [green]main[/]                [dim]18h[/]  [green]✓ clean[/]",
    "  [bold]acme-api[/]     [green]main[/]                [dim]2h[/]   [yellow]● 1 changed[/]  [yellow]↑1[/]",
    "  [bold]acme-infra[/]   [bold cyan]feat/terraform-vpc[/]  [dim]5h[/]   [green]✓ clean[/]  [dim]+1 br[/]",
    "  [bold]acme-mobile[/]  [green]main[/]                [dim]2d[/]   [green]✓ clean[/]  [magenta]⚑1[/]",
    "  [dim]────────────────────────────────────────────────────────[/]",
    "  [bold]4 repos[/]  [dim]·[/]  [green]3 clean[/]  [dim]·[/]  [yellow]1 dirty[/]  [dim]·[/]  [cyan]1 on a feature branch[/]",
    "",
    "  [bold]huginn doctor[/]  [dim]· audit vs conventions[/]",
    "  [green]6 managed & compliant[/] [dim]·[/] [yellow]1 with gaps[/] [dim]·[/] [dim]0 dormant[/]",
    "",
    "  [bold cyan]── past ──[/]",
    "",
    "  [bold]muninn digest[/]  [dim]· Jun 29 – Jul 6, 2026[/]",
    "  [bold]Across 4 repos: 48 commits · 11 PRs merged · 2 releases[/]",
    "  [bold]acme-web[/]",
    "    [green]⚑[/] Released [bold]v1.4.0[/] — dark mode + a11y pass",
    "    [cyan]⑃[/] Merged #212 feat: theme switcher · #210 fix: focus traps",
    "  [bold]acme-infra[/]",
    "    [green]⚑[/] Released [bold]v0.9.0[/] — Terraform VPC + observability",
    "",
    "  [bold cyan]── threats ──[/]",
    "",
    "  [bold]geri hunt[/]  [dim]· what needs running down[/]",
    "  [bold]acme-api[/]",
    "    [red]●[/] 3 open alerts (worst: high)",
    "    [yellow]⚓[/] 2 unpinned action usages",
    "  [bold]acme-mobile[/]",
    "    [dim]∙ unmonitored (manifest, no dependabot.yml)[/]",
    "  [bold]4 alerts · 6 outdated dep signals · 3 unpinned actions[/]",
    "",
    "  [bold cyan]── cruft ──[/]",
    "",
    "  [bold]freki reap[/]  [dim]· estate cruft summary[/]",
    "  [bold]branches[/]    9 reapable [dim]across 3 repo(s)[/]",
    "  [bold]prs[/]         2 abandoned [dim](of 5 open)[/]",
    "  [bold]artifacts[/]   3 reapable [dim](48MB of 120MB across 11 total)[/]",
    "  [bold]14 thing(s) reapable[/] [dim]across the estate — apply per-command[/]",
    "",
    "  [bold]estate:[/] 1 dirty [dim]·[/] 1 compliance gap [dim]·[/] 4 alerts [dim]·[/] 14 reapable",
    "",
]

texts = [Text.from_markup(l) for l in LINES]
con = Console(record=True, width=max(t.cell_len for t in texts) + 2)
for t in texts:
    con.print(t)
svg = tempfile.mktemp(suffix=".svg")
con.save_svg(svg, title="grimnir survey")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "grimnir-survey.png")
cairosvg.svg2png(url=svg, write_to=out, scale=2)
os.unlink(svg)
print("wrote", os.path.normpath(out))
