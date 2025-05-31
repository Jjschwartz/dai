#!/usr/bin/env python3
"""
Command AI (cai) - CLI tool for AI-powered error analysis
"""
import sys
import subprocess
import argparse


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
        
        # Command failed - show error and provide AI analysis placeholder
        print(f"Command failed with exit code {result.returncode}")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print("\n🤖 AI Analysis (placeholder - not yet implemented):")
        print("The command failed. Here's where AI would analyze the error and provide suggestions.")
        
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