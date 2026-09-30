"""Entry point: python main.py <command> [options]"""
import sys

from expense_tracker.cli import run

if __name__ == "__main__":
    sys.exit(run())
