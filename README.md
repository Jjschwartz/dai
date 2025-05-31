# cai

**Command AI** - A simple CLI tool that can be invoked in front of any of your normal terminal commands. When your program encounters an error, cai will automatically prompt an AI (Claude, GPT) with the error details and provide useful debugging information. Otherwise it will just run the command as normal.

## Installation

### Install as CLI tool

To install `cai` as a global CLI tool using uv:

```bash
uv tool install .
# or to reinstall
uv tool install --force .
```

### Development setup

This project uses `uv` for managing installation and dependencies.

```bash
uv sync
# for development
uv sync --dev
```

## Usage

Simply prefix any command with `cai` to get AI-powered error analysis:

```bash
cai your normal command here
```

For example:

```bash
cai git status
cai python my_program.py
# you can even do, but things get weird
cai cai python my_program.py
```

Normal shell syntax is supported, including pipes, redirects, and complex commands by using quotes.

```bash
cai "git status | grep 'modified'"
cai "python -c 'print(1/0)'"
# without quotes things work as normal, with each command separate
# e.g. cai will only run for the first and third command
cai which python && python --version && cai python main.py
```

When the command fails, cai will capture the error and provide intelligent debugging suggestions using Claude.

## Setup

You'll need to set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```
