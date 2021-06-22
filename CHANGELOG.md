# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).


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
