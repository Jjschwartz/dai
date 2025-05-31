"""
Command AI (cai) - CLI tool for AI-powered error analysis
"""

import os
import select
import shlex
import subprocess
import sys

from anthropic import Anthropic
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown


def analyze_error_with_claude(command: str, stdout: str, stderr: str, exit_code: int):
    """Use Claude to analyze the command error and provide suggestions."""
    print("\n🤖 AI Analysis:")
    try:
        # Check for API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print(
                "❌ No ANTHROPIC_API_KEY environment variable found. Please set it to use AI analysis."
            )
            return

        client = Anthropic(api_key=api_key)

        prompt = f"""I ran this command and it failed:
Command: {command}
Exit code: {exit_code}

STDOUT:
{stdout or "(empty)"}

STDERR:
{stderr or "(empty)"}

Please analyze this error and provide:
1. A brief explanation of what went wrong
2. Specific suggestions to fix the issue
3. Any relevant context or common causes

Format your response using markdown with **bold** for key points and *italics* for emphasis. Keep your response concise and practical."""

        response_text = ""
        console = Console()

        with Live(Markdown(""), console=console, refresh_per_second=10) as live:
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                for text in stream.text_stream:
                    response_text += text
                    # Update the live display with current markdown
                    live.update(Markdown(response_text))

        return response_text

    except Exception as e:
        return f"❌ Error calling Claude API: {e}"


def run_command_with_ai_analysis(command_string):
    """Run a command and provide AI analysis if it fails."""
    try:
        # Execute the command through shell to handle pipes, redirects, and complex syntax
        process = subprocess.Popen(
            command_string,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Capture output for AI analysis while streaming
        stdout_lines = []
        stderr_lines = []

        # Stream output in real-time
        # Use polling to read from both stdout and stderr
        while process.poll() is None:
            # Check if there's data to read
            ready, _, _ = select.select([process.stdout, process.stderr], [], [], 0.1)

            for stream in ready:
                if stream == process.stdout:
                    line = stream.readline()
                    if line:
                        print(line, end="")
                        stdout_lines.append(line)
                elif stream == process.stderr:
                    line = stream.readline()
                    if line:
                        print(line, end="", file=sys.stderr)
                        stderr_lines.append(line)

        # Read any remaining output
        remaining_stdout = process.stdout.read()  # type: ignore
        remaining_stderr = process.stderr.read()  # type: ignore

        if remaining_stdout:
            print(remaining_stdout, end="")
            stdout_lines.append(remaining_stdout)
        if remaining_stderr:
            print(remaining_stderr, end="", file=sys.stderr)
            stderr_lines.append(remaining_stderr)

        # Get the exit code
        exit_code = process.returncode
        # If command succeeded, we're done
        if exit_code == 0:
            return exit_code

        # Command failed - provide AI analysis
        stdout_text = "".join(stdout_lines)
        stderr_text = "".join(stderr_lines)

        print(f"\nCommand failed with exit code {exit_code}")
        analyze_error_with_claude(command_string, stdout_text, stderr_text, exit_code)
        return exit_code
    except FileNotFoundError:
        print("Error: Command not found")
        return 127
    except Exception as e:
        print(f"Error executing command: {e}")
        return 1


def main():
    """Main entry point for the cai CLI tool."""
    args = sys.argv[1:]
    if not args:
        print("Usage: cai <command>")
        return 0

    # Join all arguments back into a single command string to preserve quotes, pipes, etc.
    command_string = shlex.join(args)
    # Run the command with AI analysis
    return run_command_with_ai_analysis(command_string)
