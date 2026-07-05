# Roadmap

_What's planned for grimnir — check items off as they ship. Each phase is a version milestone._

## Phases

- [x] **v0.1.0 — Scaffold + `survey`.** Dispatcher, config (huginn-config fallback), beast-detection
      + graceful degradation, and the flagship consolidated briefing.
- [x] **v0.2.0 — `summon`.** Clone-or-update every owned repo into the estate.
- [x] **v0.3.0 — Pack governance.** `install` (symlink beasts + dep check + config scaffold),
      `rally` (fetch the beasts + wire them up), `config`, `doctor` (self) + `version`.
- [ ] **v0.4.0 — `brief` / `morning`.** A lean daily digest — the deltas worth your attention (new
      alerts, fresh drift, cruft crossing a threshold).
- [ ] **v0.5.0 — `schedule` + CI & docs.** Wire the routines via cron (weekly `muninn digest`, daily
      `geri hunt`, a `grimnir brief`); `shellcheck` gate; consolidated README.
- [ ] **v1.0.0 — Release.** Symlink install to `~/.local/bin/grimnir`, tagged `v1.0.0`, Definition of
      Done met.

## Deferred (do NOT build before v1.0)

- **A live TUI dashboard** — the true high seat, a refreshing whole-estate panel.
- **`--json` / report export** — HTML/Markdown estate report drawing all beasts.
- **Remediation flows** — `grimnir tend`: survey → propose fixes (huginn `doctor --fix`, freki
  `--apply`, geri PRs) behind a single guarded confirm.
- **Going public** — like the rest of the pack, once solid.
