# grimnir

The Allfather's high seat — one command center over the four beasts that run a personal GitHub
**estate**. Odin's byname ("the masked one"), from Hliðskjálf, sees into all realms at once and
commands the ravens and wolves. `grimnir` is that seat.

| Beast | Myth | Does |
|---|---|---|
| [huginn](https://github.com/brett-buskirk/huginn) | raven — thought | present state + convention compliance |
| [muninn](https://github.com/brett-buskirk/muninn) | raven — memory | history: what shipped, and when |
| [geri](https://github.com/brett-buskirk/geri) | wolf — hunter | threats: security alerts, stale deps, drift |
| [freki](https://github.com/brett-buskirk/freki) | wolf — reaper | cruft: stale branches, dead PRs, old artifacts |

grimnir's value is consolidation, not aliasing — every command marshals two or more beasts (or
governs the pack itself) into a view none of them can produce alone.

> **Note:** config-driven like the rest of the pack — falls back to huginn's config (owner, root)
> when its own is unset, so a huginn user gets a working grimnir with zero setup. See the
> [Roadmap](ROADMAP.md) for what's next.

## Install

Requirements: `bash`, `git`, [`gh`](https://cli.github.com) (authenticated), `jq` — plus whichever
of `huginn`/`muninn`/`geri`/`freki` you want surveyed (grimnir degrades gracefully if one's missing).

```bash
git clone git@github.com:brett-buskirk/grimnir.git ~/github-repos/grimnir
ln -s ~/github-repos/grimnir/grimnir ~/.local/bin/grimnir   # ~/.local/bin must be on your PATH
```

Then let grimnir bring down and wire up the rest of the pack for you:

```bash
grimnir rally      # clone the four beasts + symlink them into ~/.local/bin
```

`rally` is the one-command onboarding: install grimnir, run `grimnir rally`, and the whole suite
(huginn/muninn/geri/freki) is cloned from `brett-buskirk` and ready. It's idempotent — a beast
already present is left untouched; `rally --update` pulls the pack to latest.

## Commands

```
survey the estate
  survey                 one consolidated briefing — present · past · threats · cruft
provision
  rally [--update]       assemble the pack — clone the four beasts + wire them up
  install [--force]      symlink the present beasts into ~/.local/bin
  summon [--update]      clone every repo you own into the estate (--update pulls existing)
configure
  config [set|edit]      the shared estate config — owner · root · exemptions
reference
  help                   this menu
```

Run **`grimnir <command> help`** for details and options on any command.

## How it works

- **`survey`** runs each installed beast's heaviest summary command — `huginn status` + `huginn
  doctor`, `muninn digest --since 1w`, `geri hunt`, `freki reap` — under a labeled section, then
  synthesizes a top-line `estate:` headline (dirty repos, compliance gaps, open alerts, reapable
  cruft) from their own output. A beast missing from `PATH` is skipped with a quiet note rather than
  failing the whole survey.
- **`summon`** gathers the realms — `gh repo list` every repo you own, clone the ones missing from
  `$GRIMNIR_ROOT`, and (with `--update`) fast-forward the ones already there (skipping any with
  uncommitted changes). Cloning is additive, so there's no `--apply` gate; updating is opt-in so a
  summon never disturbs unpushed work. Exemptions govern *management*, not *presence* — summon brings
  down everything you own, even repos the ravens/wolves skip when acting.
- **`rally`** assembles the pack — clones any of the four beasts missing from `$GRIMNIR_ROOT` (from
  `$GRIMNIR_PACK_OWNER`, default `brett-buskirk`), then runs the same wiring `install` does. Idempotent
  by default (present beasts are left alone); `--update` fast-forwards them, `--force` repairs a
  symlink pointing elsewhere.
- **`install`** is the local half of provisioning — symlinks each beast script already present in the
  estate into `$GRIMNIR_BIN` (default `~/.local/bin`), checks deps, and scaffolds grimnir's config.
  Idempotent; `rally` builds on it by fetching what's missing first.
- **`config`** is one front-end for the shared estate identity every beast reads — `config show`
  resolves owner, root, exemptions, and which beast configs exist; `config init` / `set` / `edit`
  manage grimnir's own config file. Any key left unset falls back to huginn's config, so you set the
  estate identity once and the whole pack follows.
- **Graceful degradation is the whole design** — grimnir is useful with only one beast installed,
  and gets more useful as you add the rest.
- **Respects `NO_COLOR`** and non-TTY output.

## Configuration

Settings resolve **environment variable → config file → huginn's config → smart default**. Config
file: `${XDG_CONFIG_HOME:-~/.config}/grimnir/config` (override with `GRIMNIR_CONFIG`).

| Key / env var | Default | Purpose |
|---|---|---|
| `GRIMNIR_OWNER` | `HUGINN_OWNER`, else your `gh` login | GitHub owner of the estate repos |
| `GRIMNIR_ROOT` | `HUGINN_ROOT`, else `~/github-repos` | directory of repos to manage |

grimnir doesn't need its own config to be useful — if `~/.config/huginn/config` exists, it's used
automatically.

## Roadmap

The phased build-out — pack governance (`install` · `config` · `doctor` · `version`), a daily
`brief`, and scheduled routines — is tracked in [ROADMAP.md](ROADMAP.md).

## License

[MIT](LICENSE) © 2026 Brett Buskirk
