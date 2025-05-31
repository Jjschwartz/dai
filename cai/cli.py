"""
Command AI (cai) - CLI tool for AI-powered error analysis
"""

import argparse
import os
import select
import subprocess
import sys

from anthropic import Anthropic


def analyze_error_with_claude(command, stdout, stderr, exit_code):
    """Use Claude to analyze the command error and provide suggestions."""
    try:
        # Check for API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return "❌ No ANTHROPIC_API_KEY environment variable found. Please set it to use AI analysis."

        client = Anthropic(api_key=api_key)

        prompt = f"""I ran this command and it failed:
Command: {" ".join(command)}
Exit code: {exit_code}

STDOUT:
{stdout or "(empty)"}

STDERR:
{stderr or "(empty)"}

Please analyze this error and provide:
1. A brief explanation of what went wrong
2. Specific suggestions to fix the issue
3. Any relevant context or common causes

Keep your response concise and practical."""

        response_text = ""
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                response_text += text

        print()  # Add newline after streaming
        return response_text

    except Exception as e:
        return f"❌ Error calling Claude API: {e}"


def run_command_with_ai_analysis(command_args):
    """Run a command and provide AI analysis if it fails."""
    try:
        # Execute the command with streaming output
        process = subprocess.Popen(
            command_args,
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
        remaining_stdout = process.stdout.read()
        remaining_stderr = process.stderr.read()

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
        print("\n🤖 AI Analysis:")
        analyze_error_with_claude(command_args, stdout_text, stderr_text, exit_code)
        return exit_code
    except FileNotFoundError:
        print(f"Error: Command '{command_args[0]}' not found")
        return 127
    except Exception as e:
        print(f"Error executing command: {e}")
        return 1


def main():
    """Main entry point for the cai CLI tool."""
    parser = argparse.ArgumentParser(
        description="Command AI - Run commands with AI-powered error analysis",
        prog="cai",
    )
    parser.add_argument("command", nargs="+", help="Command and arguments to execute")

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    args = parser.parse_args()

    # Run the command with AI analysis
    return run_command_with_ai_analysis(args.command)


if __name__ == "__main__":
    sys.exit(main())
