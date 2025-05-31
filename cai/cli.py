#!/usr/bin/env python3
"""
Command AI (cai) - CLI tool for AI-powered error analysis
"""
import sys
import subprocess
import argparse
import os
from anthropic import Anthropic


def analyze_error_with_claude(command, stdout, stderr, exit_code):
    """Use Claude to analyze the command error and provide suggestions."""
    try:
        # Check for API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return "❌ No ANTHROPIC_API_KEY environment variable found. Please set it to use AI analysis."
        
        client = Anthropic(api_key=api_key)
        
        prompt = f"""I ran this command and it failed:
Command: {' '.join(command)}
Exit code: {exit_code}

STDOUT:
{stdout or '(empty)'}

STDERR:
{stderr or '(empty)'}

Please analyze this error and provide:
1. A brief explanation of what went wrong
2. Specific suggestions to fix the issue
3. Any relevant context or common causes

Keep your response concise and practical."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"❌ Error calling Claude API: {e}"


def run_command_with_ai_analysis(command_args):
    """Run a command and provide AI analysis if it fails."""
    try:
        # Execute the command
        result = subprocess.run(
            command_args,
            capture_output=True,
            text=True,
            check=False
        )
        
        # If command succeeded, just show output
        if result.returncode == 0:
            if result.stdout:
                print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, end='', file=sys.stderr)
            return result.returncode
        
        # Command failed - show error and provide AI analysis
        print(f"Command failed with exit code {result.returncode}")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print("\n🤖 AI Analysis:")
        analysis = analyze_error_with_claude(command_args, result.stdout, result.stderr, result.returncode)
        print(analysis)
        
        return result.returncode
        
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
        prog="cai"
    )
    parser.add_argument(
        "command",
        nargs="+",
        help="Command and arguments to execute"
    )
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    
    args = parser.parse_args()
    
    # Run the command with AI analysis
    return run_command_with_ai_analysis(args.command)


if __name__ == "__main__":
    sys.exit(main())