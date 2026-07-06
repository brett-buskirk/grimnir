# Contributing

- **No direct commits to `main`** — branch → PR (`gh pr create`) → green checks → merge. **Stop at
  the PR and let Brett merge** — don't self-merge unless told. One command per PR.
- **AgentGate runs on every PR** — `secrets` + `dangerous_patterns` block; `scope` is advisory.
- Commits are signed & Verified; never commit secrets (`.env`, keys are gitignored).

## Working on the script

`grimnir` is a single Bash script. Keep it dependency-light: `bash`, `git`, `gh`, `jq` — plus the
beasts (`huginn`/`muninn`/`geri`/`freki`) it invokes off your `PATH`.

- **Syntax-check before pushing:** `bash -n grimnir`.
- **Run `shellcheck`:** `shellcheck grimnir` (CI runs both `bash -n` and `shellcheck` on every
  push/PR — see `.github/workflows/shellcheck.yml`). Known-intentional warnings are silenced the way
  geri/freki do — a file-level `# shellcheck disable=SC2059` (color vars in `printf` format strings)
  plus scoped inline `# shellcheck disable=...` comments (each with a reason: non-constant `source`,
  the literal `$HOME` in `homelit`, the shared `M` palette slot). Don't broaden them without a reason.
- Colors go through the `$R/$G/$Y/…` vars (empty when non-TTY / `NO_COLOR`) — don't hardcode escapes.
- Each subcommand is a `cmd_<name>` function with a matching `help_<name>`; wire new ones into the
  `case` dispatcher and the `cmd_help` menu, and give every command two-level help.

## The one rule that makes grimnir grimnir

**Consolidation, not aliasing.** Every command must do something no single beast can — unify their
views (`survey`, `brief`), provision the whole pack (`rally`, `install`), or govern it (`config`,
`schedule`, `doctor`, `version`). A command that just forwards to one beast doesn't belong here.

- **Detect beasts, degrade gracefully.** Reach a beast through `have <beast>` (`command -v`); if it's
  absent, skip its section with a quiet note rather than failing. grimnir must stay useful with only
  some of the pack installed.
- **Capture, don't re-color.** Running a beast in `"$(...)"` already strips its ANSI (its own
  `[ -t 1 ]` sees a pipe), so parse its summary line with `grab`; grimnir supplies the section chrome.
- **Presence vs. management.** `summon`/`rally` bring repos/beasts *down* (never consult `is_exempt`);
  the beasts still skip exempt repos when *acting*. Keep that line.
- **Never disturb local work.** Mutating steps are opt-in and reversible-first — `--update` pulls
  ff-only and skips dirty; `--force` gates any overwrite; `--dry-run` previews. `schedule` touches
  only grimnir's own delimited crontab block.

## Paths & config

- `$HERE` = where the tool lives (and its bundled `templates/`); `$ROOT` = the estate it manages
  (`$GRIMNIR_ROOT`); `$CONV` = the conventions source, shared with huginn; `$BIN` = where the pack is
  symlinked (`$GRIMNIR_BIN`). Resolve template files with `first_of "$CONV/templates/<file>"
  "$HERE/templates/<file>"` so commands fall back to the bundled defaults.
- Config resolves **env → `~/.config/grimnir/config` → huginn's config → smart default**. Any key
  left unset falls back to huginn's, so the estate identity is set once for the whole pack.
