# CLAUDE.md — Grimnir Build Handoff
### The Allfather's high seat — the command center over the four beasts

> `huginn new` scaffolded this repo (guardrails, ruleset, labels, the full docs suite, a signed genesis
> commit). This file is the build brief for the agent that builds Grimnir. Read it top to bottom first.
> **huginn is your reference implementation** — read `~/github-repos/huginn/huginn` and match it. The
> four beasts it commands are already built and on your `PATH`: `huginn`, `muninn`, `geri`, `freki`.

---

## The concept

The estate has four beasts, each its own Bash CLI:

| Beast | Myth | Does |
|---|---|---|
| [`huginn`](https://github.com/brett-buskirk/huginn) | raven — thought | present state + convention compliance |
| [`muninn`](https://github.com/brett-buskirk/muninn) | raven — memory | history: what shipped, and when |
| [`geri`](https://github.com/brett-buskirk/geri) | wolf — hunter | threats: security alerts, stale deps, drift |
| [`freki`](https://github.com/brett-buskirk/freki) | wolf — reaper | cruft: stale branches, dead PRs, old artifacts |

**Grimnir is the Allfather** (a byname of Odin — *"the masked one"*; named this way on purpose, to
avoid colliding with the [Odin programming language](https://odin-lang.org) whose CLI is also `odin`).
In myth Odin sits on **Hliðskjálf**, the high seat from which he sees into all realms at once, sends the
ravens out each morning, and commands the wolves. Grimnir is that seat: **one command center over the
whole estate.**

**Design principle (the whole point):** Grimnir's value is *consolidation, pack-governance, and
routines* — **not** aliasing. A tool that only did `grimnir hunt → geri hunt` would be worthless. Every
command must do something no single beast can: unify their views, provision the pack, or run the
routines.

## The beasts' real command surfaces (call these — verify with `<beast> help`)

- **huginn** — `status` (dashboard) · `doctor [repo] [--fix]` (compliance) · `sync` · `prs` · `conventions`
- **muninn** — `log [--since]` · `releases` · `digest [--since] [--md]`
- **geri** — `alerts` · `deps` · `actions` · `hunt [--md]` (combined threat summary)
- **freki** — `branches` · `prs` · `artifacts` · `releases` · `reap` (dry-run cruft summary) — *reads are safe; freki never deletes without `--apply`*

## Scope — v0.1

### `survey` — the flagship (the high seat)
**One consolidated all-realms briefing** that marshals the beasts into a single view:
- **Present** — `huginn status` (state) + `huginn doctor` (compliance summary)
- **Past** — `muninn digest --since 1w` (what shipped lately)
- **Threats** — `geri hunt` (alerts · deps · actions)
- **Cruft** — `freki reap` (dry-run summary)

Run each installed beast under a labeled section, and synthesize a top-line **headline** parsed from
their summaries (e.g. `estate: 3 dirty · 1 compliance gap · 5 alerts · 12 reapable branches`). This is
the "how is my whole estate, right now" command — the reason Grimnir exists.

### `summon` — gather the realms *(your idea — feature it)*
**Clone-or-update every repo you own into the estate.** `gh repo list <owner> --limit <N>` → clone any
missing repo into `$ROOT`, and (with `--update`) `git pull` the ones already there. Flags:
`--skip-archived`, `--skip-forks`, `--dry-run` (list what it *would* clone). Cloning is additive/safe, so
no `--apply` gate needed — but default to showing the plan and cloning missing repos; make *updating*
existing ones opt-in so it never disturbs local work.
*Note: exemptions govern **management** (what the beasts touch), not **presence** — `summon` brings down
everything you own; the ravens/wolves still skip exempt repos when acting.*

### Pack governance
- **`install`** — provision the whole toolkit: for each beast repo present in `$ROOT`, symlink its
  script to `~/.local/bin`; check deps (`bash`/`git`/`gh`/`jq`); scaffold the shared config. (Pairs
  beautifully with `summon`: summon the repos, then install the pack.)
- **`config`** — one front-end for the shared estate config all beasts read (owner, root, exemptions).
- **`doctor` (self)** + **`version`** — health-check the *pack itself*: which beasts are installed, on
  `PATH`, and current; show all four versions at once. (Distinct from `huginn doctor`, which audits the
  *repos*.)

## Tech & architecture — mirror huginn

**huginn is the reference implementation.** Grimnir is the fifth tool of one coherent pack.

- **Single Bash script** named `grimnir`, `set -uo pipefail`. Deps: `bash`, `git`, `gh`, `jq` — and it
  *invokes* the beasts (`huginn`/`muninn`/`geri`/`freki`) off `PATH`.
- **Dispatcher + two-level help** (`grimnir help`, `grimnir <cmd> help`) — copy huginn's structure.
- **Config-driven**, same precedence (env → `~/.config/grimnir/config` → smart defaults): `GRIMNIR_ROOT`,
  `GRIMNIR_OWNER`. **Fall back to huginn's config** for `HUGINN_ROOT`/`HUGINN_OWNER` when unset — one
  shared estate identity across the whole pack (mirror how muninn/geri/freki do it).
- **Graceful degradation is mandatory.** Detect each beast with `command -v`; if one isn't installed,
  skip its section with a quiet note (`geri not installed — skipping threats`) rather than failing.
  Grimnir must be useful even with only huginn/muninn present.
- **Reuse `is_exempt`** where Grimnir reasons about managed repos (its beast calls already respect
  exemptions, since huginn/geri/freki do). Respect `NO_COLOR` and non-TTY.

## Working conventions (non-negotiable)

- **No direct commits to `main`.** Branch → PR → green checks → **stop at the PR and let Brett merge**
  (don't self-merge unless told). One command per PR.
- **Signed commits** (Verified); end messages with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **AgentGate on every PR** (scaffolded). **`brett-buskirk` must be the active gh account.**
- **Match huginn's voice** — terse, lowercase, a little wry.

## Docs suite

`huginn new` scaffolded README / LICENSE / CHANGELOG / ROADMAP / CONTRIBUTING. Flesh out the **README**
(lead with the pantheon: the four beasts + the Allfather that commands them — a table like the one
above reads great), keep the **CHANGELOG** current, grow the **ROADMAP** from the phased plan.

## Phased plan (each phase → a version milestone; create them when you start)

- **v0.1.0 — Scaffold + `survey`.** Dispatcher, config (huginn-config fallback), beast-detection +
  graceful degradation, and the flagship consolidated briefing.
- **v0.2.0 — `summon`.** Clone-or-update every owned repo into the estate.
- **v0.3.0 — Pack governance.** `install` (symlink beasts + dep check + config scaffold), `config`,
  `doctor` (self) + `version`.
- **v0.4.0 — `brief` / `morning`.** A lean daily digest — the *deltas* worth your attention (new alerts,
  fresh drift, cruft crossing a threshold), suitable to run each morning.
- **v0.5.0 — `schedule` + CI & docs.** Wire the routines via cron (weekly `muninn digest`, daily
  `geri hunt`, a `grimnir brief`); `shellcheck` gate; consolidated README.
- **v1.0.0 — Release.** Symlink install to `~/.local/bin/grimnir`, tagged `v1.0.0`, DoD met.

## Definition of Done

`grimnir survey` gives a real consolidated estate briefing across all installed beasts (degrading
gracefully when one is absent); `summon` clones/updates every owned repo into the estate; `install` and
`config` provision and configure the pack; `doctor`/`version` self-check it; config-driven with two-level
help; docs suite complete; passes `huginn doctor grimnir` clean; shipped as **v0.1.0**. It should read as
the Allfather of the pack — one seat from which the whole estate is legible.

## Deferred — Roadmap (do NOT build in v0.1)

- **A live TUI dashboard** (the true high seat — a refreshing whole-estate panel).
- **`--json` / report export** (HTML/Markdown estate report drawing all beasts).
- **Remediation flows** — `grimnir tend`: survey → propose fixes (huginn `doctor --fix`, freki
  `--apply`, geri PRs) behind a single guarded confirm.
- **Going public** — like the rest of the pack, once solid.

## Reference repos

- **`~/github-repos/huginn`** — the reference implementation; match its structure, config, and voice.
- **`~/github-repos/muninn`, `geri`, `freki`** — the beasts Grimnir marshals; read each one's `help`
  (and script) so `survey` calls the right commands and parses their summaries.
- **`~/github-repos/repo-conventions`** — the estate standard (labels, ruleset, docs-suite, exemptions).
