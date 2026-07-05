# Changelog

All notable changes to grimnir are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial scaffold.
- **`survey`** — the flagship consolidated estate briefing: present (`huginn status` + `huginn
  doctor`), past (`muninn digest --since 1w`), threats (`geri hunt`), cruft (`freki reap`), each
  under a labeled section, with a synthesized top-line `estate:` headline. Detects each beast via
  `command -v` and degrades gracefully — a missing beast is skipped with a quiet note rather than
  failing the survey.
- **Config-driven** — settings resolve env → config file → smart defaults: `GRIMNIR_OWNER`,
  `GRIMNIR_ROOT`. Config lives at `~/.config/grimnir/config`. Falls back to
  `~/.config/huginn/config`'s `HUGINN_ROOT`/`HUGINN_OWNER` when its own config is unset, so a huginn
  user gets a working grimnir with zero setup.
- **`summon`** — gather the realms: `gh repo list` every repo you own, clone the ones missing from
  `$GRIMNIR_ROOT`, and (with `--update`) fast-forward the ones already present, skipping any with
  uncommitted changes (mirrors `huginn sync`). Flags: `--update`/`-u`, `--skip-archived`,
  `--skip-forks`, `--limit N`, `--dry-run`/`-n`. Cloning is additive/safe — no `--apply` gate;
  updating is opt-in so a summon never disturbs unpushed work. Exemptions govern management, not
  presence: summon brings down everything you own, even repos the ravens/wolves skip when acting.
- **`config`** — one front-end for the shared estate config every beast reads. `config show`
  (default) resolves owner · root · config-path · exemptions (from the conventions repo) · which
  beast configs exist on disk; `config init [--force]` scaffolds grimnir's config with detected
  defaults; `config set <owner|root> <value>` upserts a key; `config edit` opens it in `$EDITOR`;
  `config path` prints the file path. Any key unset here falls back to `~/.config/huginn/config`.
- **`install`** — the local half of provisioning: symlink each beast script present in
  `$GRIMNIR_ROOT` into `$GRIMNIR_BIN` (default `~/.local/bin`), check deps (`bash`/`git`/`gh`/`jq`),
  and scaffold grimnir's config. Idempotent — a correct link is left alone; `--force` relinks a name
  whose symlink points elsewhere; `--dry-run` previews.
- **`rally`** — assemble the pack, the one-command onboarding. Clones any of the four beasts
  (`huginn`/`muninn`/`geri`/`freki`) missing from the estate — from `$GRIMNIR_PACK_OWNER` (default
  `brett-buskirk`), the canonical pack source, which needn't be your own estate owner — then wires the
  whole pack up via the same provisioner `install` uses. Idempotent by default (present beasts are
  reported and left untouched); `--update` fast-forwards present beasts to latest (skipping dirty
  ones), `--force` repairs stray symlinks, `--dry-run` previews the clone · pull · link plan.
- Two-level help: `grimnir help` overview + `grimnir <command> help` per-command detail.
