"""Command-line interface: argument parsing and command handlers."""
import argparse
import logging
import sys
from datetime import datetime

from .logger import setup_logging
from .manager import ExpenseManager
from .reports import export_csv, format_summary, format_table, monthly_summary
from .storage import JsonStorage
from .validators import CATEGORIES, ValidationError, validate_month

log = logging.getLogger(__name__)


def cmd_add(args, manager):
    e = manager.add(args.amount, args.category, args.note, args.date)
    print(f"Added expense #{e.id}: Rs {e.amount:.2f} on {e.category} ({e.date})")


def cmd_list(args, manager):
    month = validate_month(args.month) if args.month else None
    print(format_table(manager.list(args.category, month, args.sort)))


def cmd_delete(args, manager):
    manager.delete(args.id)
    print(f"Deleted expense #{args.id}.")


def cmd_search(args, manager):
    rows = manager.search(args.keyword)
    print(format_table(rows) if rows else "No matching expenses.")


def cmd_budget(args, manager):
    print(f"Monthly budget set to Rs {manager.set_budget(args.amount):.2f}")


def cmd_summary(args, manager):
    month = validate_month(args.month) if args.month else datetime.now().strftime("%Y-%m")
    rows = manager.list(month=month)
    print(format_summary(monthly_summary(rows, month, manager.budget)))


def cmd_export(args, manager):
    month = validate_month(args.month) if args.month else None
    count = export_csv(manager.list(month=month), args.output)
    print(f"Exported {count} expenses to {args.output}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="expense-tracker", description="Command-line expense tracker"
    )
    parser.add_argument("--data-file", default="expenses.json", help="storage file (default: expenses.json)")
    parser.add_argument("--log-file", default="expense_tracker.log", help="log file path")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="add an expense")
    p.add_argument("amount", help="amount spent")
    p.add_argument("category", help=f"one of: {', '.join(CATEGORIES)}")
    p.add_argument("--note", default="", help="short description")
    p.add_argument("--date", help="YYYY-MM-DD (default: today)")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="list expenses")
    p.add_argument("--category")
    p.add_argument("--month", help="YYYY-MM")
    p.add_argument("--sort", choices=["date", "amount"], default="date")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("delete", help="delete an expense by ID")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("search", help="search expenses by note keyword")
    p.add_argument("keyword")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("budget", help="set the monthly budget")
    p.add_argument("amount")
    p.set_defaults(func=cmd_budget)

    p = sub.add_parser("summary", help="category-wise monthly summary")
    p.add_argument("--month", help="YYYY-MM (default: current month)")
    p.set_defaults(func=cmd_summary)

    p = sub.add_parser("export", help="export expenses to a CSV file")
    p.add_argument("--month", help="YYYY-MM (default: all months)")
    p.add_argument("--output", default="expenses.csv", help="CSV path (default: expenses.csv)")
    p.set_defaults(func=cmd_export)

    return parser


def run(argv=None):
    """Run the CLI and return an exit code (0 = success)."""
    args = build_parser().parse_args(argv)
    setup_logging(args.log_file)
    try:
        manager = ExpenseManager(JsonStorage(args.data_file))
        args.func(args, manager)
        return 0
    except ValidationError as err:
        log.warning("Validation error: %s", err)
        print(f"Error: {err}", file=sys.stderr)
        return 1
    except OSError as err:
        log.error("File error: %s", err)
        print(f"File error: {err}", file=sys.stderr)
        return 2
