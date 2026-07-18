# grimnir cheat sheet

Quick reference for every command, option, and behavior. `grimnir` is the Allfather's high seat — one
command center **over the whole estate** and the four beasts (huginn/muninn/geri/freki) that run it. It
consolidates their views, provisions the pack, and runs the routines; it never just aliases them.

For the narrative version see the [README](README.md); for per-command detail in the terminal, run
`grimnir <command> help`.

---

## At a glance

| Command | Aliases | What it does | Options |
|---------|---------|--------------|---------|
| [`survey`](#survey) | *(default menu; see note)* | One consolidated all-realms briefing — present · past · threats · cruft | |
| [`brief`](#brief) | `morning` | The deltas since your last brief — a lean daily digest | `--since <window>`, `--no-save` |
| [`rally`](#rally) | | Assemble the pack — clone the four beasts + wire them up | `--update`/`-u`, `--force`/`-f`, `--dry-run`/`-n` |
| [`install`](#install) | | Symlink the present beasts into `$GRIMNIR_BIN` | `--force`/`-f`, `--dry-run`/`-n` |
| [`summon`](#summon) | | Clone every repo you own into the estate | `--update`/`-u`, `--agent[=…]`, `--force`/`-f`, `--skip-archived`, `--skip-forks`, `--limit N`, `--dry-run`/`-n` |
| [`config`](#config) | | The shared estate config — owner · root · exemptions | `show` · `init [--force]` · `set <k> <v>` · `edit` · `path` |
| [`schedule`](#schedule) | | Cron a daily brief to a logfile (+ opt-in digest / hunt) | `show` · `install [opts]` · `remove`, `--dry-run`/`-n` |
| [`doctor`](#doctor) | | Pack health — installed · on PATH · linked · current | |
| [`version`](#version--help) | `-V`, `--version` | Every beast's version, at a glance | |
| [`help`](#version--help) | `-h`, `--help` | The command menu | |

- **Read-only** views (`survey` `brief` `doctor` `version`) inspect and report — they change nothing on
  disk (`brief` does advance a small saved snapshot unless you pass `--no-save`).
- **Provision / change** commands are `rally` `install` `summon` (clone + symlink + scaffold) and
  `config` / `schedule` (write your config file / your crontab block). All are additive or idempotent;
  each takes `--dry-run` where it acts, and nothing is overwritten without `--force`.
- Running `grimnir` with no command prints the **menu** (same as `grimnir help`) — not `survey`.

---

## Requirements & global behavior

- **Requires** `bash` + `git` + `gh` (authenticated) + `jq`. It also *invokes the beasts* off your
  `PATH` — `huginn` / `muninn` / `geri` / `freki`. **Graceful degradation is the whole design:** a beast
  missing from `PATH` is skipped with a quiet note rather than failing the command, so grimnir is useful
  with only one beast installed and more useful as you add the rest.
- **Config model — shared estate identity.** Settings resolve **env var → grimnir's config file →
  huginn's config → smart default**, so a huginn user gets a working grimnir with zero setup. Config
  file: `${XDG_CONFIG_HOME:-~/.config}/grimnir/config` (override with `GRIMNIR_CONFIG`). Keys:

  | Key / env var | Default | Purpose |
  |---|---|---|
  | `GRIMNIR_OWNER` | `HUGINN_OWNER`, else your `gh` login | GitHub owner of the estate repos |
  | `GRIMNIR_ROOT` | `HUGINN_ROOT`, else `~/github-repos` | directory of repos to manage |
  | `GRIMNIR_BIN` | `~/.local/bin` | where `install` / `rally` symlink the beasts |
  | `GRIMNIR_PACK_OWNER` | `brett-buskirk` | canonical source `rally` clones the beasts from |
  | `GRIMNIR_CONVENTIONS` | `repo-conventions` | dir under the root holding `exemptions.json` |
  | `GRIMNIR_CONFIG` | `~/.config/grimnir/config` | the config file path itself |

- **Exemptions.** `exemptions.json` lives in the conventions repo (`<root>/repo-conventions/`) — the
  estate-wide standard the whole pack reads. It governs **management, not presence**: the ravens/wolves
  skip exempt repos when acting, but `summon` / `rally` still bring them down. (`$HUGINN_FAMILY` and the
  exemption set are honored *by the beasts* grimnir marshals, not re-implemented here.)
- **`NO_COLOR`** — set it (`NO_COLOR=1 grimnir …`) to disable color. Output is also automatically plain
  when piped or redirected (not a TTY).
- **No machine-readable output flag.** grimnir has **no `--json` and no `--md`** — it's a human-facing
  console over the pack. When you want structured data, reach for the individual beast that emits it
  (e.g. `geri hunt --md`, `muninn digest --md`); grimnir consolidates their *human* views.
- **Two-level help** — `grimnir help` for the menu, `grimnir <command> help` (or `-h` / `--help`) for
  one command.
- **Exit codes** — `0` on success; `1` on an unknown command (which also prints the menu).

---

## Survey the estate

### `survey`

The flagship — one consolidated all-realms briefing that marshals every installed beast into a single
view, each under a labeled heading, then synthesizes a top-line `estate:` headline (dirty repos,
compliance gaps, open alerts, reapable cruft) from whatever ran. `all clear` when every number is zero.

| Section | Beast command |
|---------|---------------|
| **present** | `huginn status` (state) + `huginn doctor` (compliance summary) |
| **past** | `muninn digest --since 1w` (what shipped lately) |
| **threats** | `geri hunt` (alerts · deps · actions) |
| **cruft** | `freki reap` (dry-run cruft summary) |

```sh
grimnir survey
NO_COLOR=1 grimnir survey   # plain output for a log/pipe
```

This runs the **heaviest** command each installed beast has, so a full sweep can take a minute or two on
a big estate (network). A beast absent from `PATH` is skipped with a quiet note. No options.

---

### `brief`

The stateful counterpart to `survey` — not the whole estate, just what *changed* since you last looked.
It runs the fast-moving beasts and diffs their numbers against a saved snapshot (`▲` up · `▼` down),
shows `muninn digest` for the window since your last brief, and headlines what's new — `all quiet` when
nothing moved. Built to run each morning, by hand or from cron ([`schedule`](#schedule)).

```sh
grimnir brief              # deltas since last brief; window auto-sizes to elapsed time
grimnir morning            # alias
grimnir brief --since 3d   # override just the 'shipped' window
grimnir brief --no-save    # peek without advancing the baseline
```

| Option | Effect |
|--------|--------|
| `--since <window>` | Override the *shipped* window (e.g. `1d`, `3d`, `1w`); default is the elapsed time since your last brief |
| `--no-save` | Peek without advancing the baseline — next brief still measures deltas from the same point |

First run saves a baseline (no deltas yet); a beast that's absent is skipped and keeps its prior
snapshot value. State: `${XDG_STATE_HOME:-~/.local/state}/grimnir/brief-state`. Same network cost class
as `survey`.

---

## Provision

### `rally`

The one-command onboarding — assemble the pack. Clones any of the four beasts missing from the estate
(from `$GRIMNIR_PACK_OWNER`, default `brett-buskirk`), then runs the same wiring `install` does
(deps · symlink · config). Install grimnir, run `grimnir rally`, and the suite is ready.

```sh
grimnir rally              # clone missing beasts + wire the pack up (idempotent)
grimnir rally --update     # also fast-forward beasts already present
grimnir rally --force      # relink a beast whose symlink points elsewhere
grimnir rally --dry-run    # print the plan — clone · pull · link — change nothing
grimnir rally -u -n        # short flags
```

| Option | Effect |
|--------|--------|
| `--update`, `-u` | Also pull beasts already present — fast-forward only, skipping any with uncommitted changes |
| `--force`, `-f` | Relink a name whose symlink points somewhere other than the estate |
| `--dry-run`, `-n` | Print the whole plan and change nothing |

Idempotent by default — a beast already present is reported and left untouched; only missing ones are
cloned. The pack source (`$GRIMNIR_PACK_OWNER`) needn't be your own estate owner. Network — one clone per
missing beast, plus a pull per present beast under `--update`.

---

### `install`

The local half of provisioning — symlink each beast script already present in the estate
(`$GRIMNIR_ROOT/<beast>/<beast>`) into `$GRIMNIR_BIN` (default `~/.local/bin`), check deps, and scaffold
grimnir's config. It links what's *on disk*; `rally` fetches what isn't first.

```sh
grimnir install            # link present beasts + scaffold config (idempotent)
grimnir install --force    # relink a beast whose symlink points elsewhere
grimnir install --dry-run  # print what would be linked/scaffolded, change nothing
```

| Option | Effect |
|--------|--------|
| `--force`, `-f` | Relink a name whose symlink points somewhere other than the estate |
| `--dry-run`, `-n` | Print the plan and change nothing |

A link that's already correct is left alone. Make sure `$GRIMNIR_BIN` is on your `$PATH`.

---

### `summon`

Gather the realms — clone every repo you own into the estate. Lists all your repos (`gh repo list`),
clones any not yet under `$GRIMNIR_ROOT`, and by default leaves the ones already there untouched.
Cloning is additive and safe, so there's **no `--apply` gate** — but updating existing repos is opt-in
(`--update`), so a summon never disturbs unpushed work.

```sh
grimnir summon                       # clone every owned repo that's missing
grimnir summon --update              # also fast-forward repos already present
grimnir summon --skip-archived --skip-forks
grimnir summon --limit 200
grimnir summon --dry-run             # print the plan, change nothing
grimnir summon --agent               # …then seat an operator (writes AGENTS.md + CLAUDE.md)
grimnir summon --agent=agents        # canonical AGENTS.md only, no CLAUDE.md shim
grimnir summon --agent --force       # overwrite an existing agent doc
```

| Option | Effect |
|--------|--------|
| `--update`, `-u` | Also pull repos already present — fast-forward only, skipping any with uncommitted changes |
| `--agent[=mode]` | After summoning, seat an operator at the estate root: write an `AGENTS.md` personalized to your owner/root/installed beasts, plus a `CLAUDE.md` `@AGENTS.md` shim. `mode` ∈ `agents` (canonical only) · `claude` (shim only) · `both` (default) |
| `--force`, `-f` | Overwrite an existing `AGENTS.md` / custom `CLAUDE.md` (with `--agent`) |
| `--skip-archived` | Don't clone archived repos |
| `--skip-forks` | Don't clone forks |
| `--limit N` | Cap how many repos to list (default `1000`) |
| `--dry-run`, `-n` | Print the plan — clone/pull/write — and change nothing |

The agent doc is idempotent: an existing `AGENTS.md` is never clobbered without `--force`. Template:
grimnir's bundled `templates/AGENTS.md`, overridable at `<conventions>/templates/AGENTS.md`. Exemptions
govern management, not presence — summon brings down everything you own, even repos the ravens/wolves
skip when acting. Network — one `gh repo list`, then one clone or pull per repo.

---

## Configure

### `config`

One front-end for the shared estate config every beast reads — owner, root, and the exemptions the
ravens/wolves honor. grimnir's own config lives at `~/.config/grimnir/config`; when a key is unset there,
the whole pack falls back to `~/.config/huginn/config`, so you set the estate identity once.

```sh
grimnir config             # 'show' is the default
grimnir config show        # resolve owner · root · config path · exemptions · beast configs
grimnir config init        # scaffold the config file with detected defaults
grimnir config init --force
grimnir config set owner brett-buskirk
grimnir config set root ~/github-repos
grimnir config edit        # open in $EDITOR (scaffolds first if absent)
grimnir config path        # print the config file path
```

| Subcommand | Effect |
|--------|--------|
| `show` *(default)* | Resolve and print owner · root · config path · exemptions · which beast configs exist |
| `init [--force]` | Scaffold the config file with detected defaults (`--force` overwrites) |
| `set <key> <value>` | Set `owner` or `root` in the config file |
| `edit` | Open the config in `$EDITOR` (scaffolds it first if absent) |
| `path` | Print the config file path |

Exemptions themselves are read from the conventions repo
(`<root>/repo-conventions/exemptions.json`) — edit them *there*, since they're the estate-wide standard
the beasts share.

---

### `schedule`

Cron the pack's routines so they run on their own. By default `install` adds one job — a daily
`grimnir brief` — whose output appends to a logfile under `${XDG_STATE_HOME:-~/.local/state}/grimnir/`
(cron has no terminal). grimnir manages **only its own block** in your crontab, delimited by
`# >>> grimnir schedule >>>` markers — your other cron jobs are never touched.

```sh
grimnir schedule                    # 'show' is the default — print grimnir's cron entries
grimnir schedule install            # add the daily brief (07:00)
grimnir schedule install --at 06:30
grimnir schedule install --weekly-digest --daily-hunt
grimnir schedule install --dry-run  # print the crontab lines, change nothing
grimnir schedule remove             # delete grimnir's block, leave the rest intact
```

| Subcommand | Effect |
|--------|--------|
| `show` *(default)* | Print grimnir's current cron entries |
| `install` | Add them — idempotent, replaces grimnir's existing block |
| `remove` | Delete grimnir's block, leaving the rest of your crontab intact |

| `install` option | Effect |
|--------|--------|
| `--at HH:MM` | Time of day for the daily brief (default `07:00`) |
| `--weekly-digest` | Also schedule a weekly `muninn digest` (Mondays 08:00) |
| `--daily-hunt` | Also schedule a daily `geri hunt` (06:00) |
| `--dry-run`, `-n` | Print the crontab lines and change nothing |

Needs the `crontab` command; jobs fire only while the cron service is running.

---

## Inspect the pack

### `doctor`

Health-check the pack *itself* — distinct from `huginn doctor`, which audits your repos against
conventions. A member on `PATH` but pointing somewhere other than the estate is flagged (repair with
`grimnir install --force`); one missing entirely points you at `grimnir rally`.

```sh
grimnir doctor
```

| Section | Reports |
|---------|---------|
| **deps** | `bash` · `git` · `gh` · `jq` present |
| **gh** | Authenticated, and as who |
| **config** | grimnir's config present (or falling back to huginn's) |
| **bin** | `$GRIMNIR_BIN` is on your `$PATH` |
| **the pack** | Per member — in the estate · version · on `PATH` and linked to the estate |

Local — reads git tags + symlink targets; one `gh api user` for the auth line. No options.

---

### `version` & `help`

`version` shows every pack member's version at a glance — grimnir and the four beasts, each derived from
its latest git tag (newest by semver). A repo with commits since its last tag shows `+N since`; one with
no tags shows `(dev)`; one not in the estate is marked so. "Derive, don't store" — no stored version
string.

```sh
grimnir version        # every beast's version at a glance
grimnir --version      # same
grimnir -V             # same
grimnir help           # the command menu
grimnir -h             # same
grimnir <command> help # detail for one command (e.g. grimnir summon help)
```

Neither takes options.

---

## Recipes

```sh
# How is my whole estate, right now? (the flagship)
grimnir survey

# Just what changed since yesterday — the morning glance
grimnir brief

# Peek at the deltas without advancing the baseline
grimnir brief --no-save

# Fresh machine: install grimnir, then bring down and wire up the whole pack
grimnir rally

# Pull the whole pack to latest and repair any stray symlinks
grimnir rally --update --force

# Bring down every repo you own (dry-run first to see the plan)
grimnir summon --dry-run
grimnir summon --skip-archived --skip-forks

# Summon the estate and seat an agent operator at the root
grimnir summon --agent

# Update existing repos too, fast-forward only (never touches unpushed work)
grimnir summon --update

# Where does the estate identity resolve? (owner · root · exemptions)
grimnir config show

# Set the estate owner once — the whole pack follows
grimnir config set owner brett-buskirk

# Cron a daily brief at 6:30, plus the weekly digest and daily hunt
grimnir schedule install --at 06:30 --weekly-digest --daily-hunt

# Is the pack healthy — installed, on PATH, linked, current?
grimnir doctor

# What version is everything?
grimnir version

# Plain output for a log/pipe (no color)
NO_COLOR=1 grimnir survey
```
