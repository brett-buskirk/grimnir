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
- Two-level help: `grimnir help` overview + `grimnir <command> help` per-command detail.
