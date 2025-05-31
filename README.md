# dai

**Debug AI** - A simple CLI tool that can be invoked in front of any of your normal terminal commands. When your program encounters an error, debugai will automatically prompt an AI (Claude, GPT) with the error details and provide useful debugging information. Otherwise it will just run the command as normal.

## Installation

First clone the repo:

```bash
# e.g. using https
git clone https://github.com/Jjschwartz/dai.git
cd dai
```

### Install as CLI tool

To install `dai` as a global CLI tool using uv:

```bash
uv tool install .
# or to reinstall
uv tool install --force .
```

This will install `dai` as a tool globally for the current user. You may need to create a new terminal session for the tool to be available.

### Development setup

This project uses `uv` for managing installation and dependencies.

```bash
uv sync
# for development (installs additionaldev dependencies)
uv sync --dev
```

## Usage

Simply prefix any command with `dai` to get AI-powered error analysis:

```bash
dai your normal command here
```

For example:

```bash
dai git status
dai python my_program.py
# you can even do the following (but things get weird)
dai dai python my_program.py
```

Normal shell syntax is supported, including pipes, redirects, and complex commands by using quotes.

```bash
dai "git status | grep 'modified'"
dai "python -c 'print(1/0)'"
# without quotes things work as normal, with each command separate
# e.g. dai will only run for the first and third command
dai which python && python --version && dai python main.py
```

When the command fails, dai will capture the error and provide intelligent debugging suggestions using Claude.

## Setup

You'll need to set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```
