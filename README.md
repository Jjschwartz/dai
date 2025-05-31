# cai

**Command AI** - A simple CLI tool that can be invoked in front of any of your normal terminal commands. When your program encounters an error, cai will automatically prompt an AI (Claude, GPT) with the error details and provide useful debugging information.

## Installation

### Install as CLI tool

To install `cai` as a global CLI tool using uv:

```bash
uv tool install .
```


### Development setup

This project uses `uv` for managing installation and dependencies.

```bash
uv sync
```

## Usage

Simply prefix any command with `cai` to get AI-powered error analysis:

```bash
cai your-normal-command
```

When the command fails, cai will capture the error and provide intelligent debugging suggestions using Claude.

## Setup

You'll need to set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```