# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).


# 0.5.4 - 2021-06-24
## Added
- Message text can now be anything that can be converted to a string

## Fixed
- Support exceptions with non-string values

## Changed


# 0.5.3 - 2021-06-23
## Added
- Ability to left/right align scopes and tags.

## Fixed

## Changed


# 0.5.2 - 2021-06-22
## Added

## Fixed
- Flush even `stderr`. Needed for Docker.

## Changed


# 0.5.1 - 2021-06-22
## Added

## Fixed
- Images should work in PyPI as well.
- Use `stderr` for logging due to convention and to avoid buffering problems.
  (`ask()` continues to use `stdin`/`stdout`.)

## Changed
- Align symbol widths.
- Determine screen size without calling `stty` (speed, portability).


# 0.5.0 - 2021-06-22
## Added
- `warn` and `colored` aliases to `warning` and `coloured`.
- `exception`, an `error` with a stack trace.
- `xdebug` (excessive debug).
- Logging levels and thresholds; see README.

## Fixed

## Changed
- Moved to [Gitmoji](https://gitmoji.dev/) style commits, using Unicode.
- Completed classifiers.
- Logging thresholds can also be set as strings, to simplify parametrization.


# 0.4.0 - 2021-06-21
## Added
- Supports plaintext output using `opts={'ansi': True|False|None}`, `None`
  (=auto) being the default. In automatic mode, color is enabled exactly for
  TTY output.
- Running `python3 signale/__init__.py` results in sample output.

## Fixed

## Changed
- Forked from [archived repository](https://github.com/ShardulNalegave/signale.py)
  (read-only, no pull requests accepted) by Shardul Nalegave.
- Default output on non-terminals is now plain text.
- Published on PyPI as `signale-logging`.
- Library directory is now `signale`.
- Simplified formatting logic, reducing the number of ANSI escape sequences
  and changing output format spacing.
