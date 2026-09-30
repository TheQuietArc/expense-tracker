# Problem Statement

## Problem
Students on a limited budget often do not know where their money goes. Small daily
expenses (food, travel, books) are forgotten, and by the end of the month the budget
is already exhausted. Paper notes and memory are unreliable, and many spreadsheet
solutions are too heavy for quick daily entry.

## Scope
**In scope**
- Recording expenses with amount, category, date and a short note
- Viewing, filtering, sorting, searching and deleting expenses
- Setting a monthly budget and receiving alerts as it is approached or exceeded
- Monthly category-wise summary and CSV export
- Runs entirely from the command line, stores data locally in a JSON file

**Out of scope**
- Multi-user accounts, cloud sync, graphical or web interface
- Bank integration and automatic expense import
- Multiple currencies

## Target Users
- College students managing a monthly allowance
- Anyone who wants a quick, private, offline expense log from the terminal

## High-Level Features
1. **Expense management** - add, list, search, delete (CRUD) with input validation
2. **Budget tracking** - monthly budget with OK / warning (80%) / over-budget alerts
3. **Reports and export** - category-wise summary with percentage share, CSV export
4. **Reliability** - atomic saves, corrupt-file recovery, file logging
