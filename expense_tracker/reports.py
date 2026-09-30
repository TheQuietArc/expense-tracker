"""Analytics, text formatting and CSV export."""
import csv


def category_totals(expenses):
    totals = {}
    for e in expenses:
        totals[e.category] = round(totals.get(e.category, 0) + e.amount, 2)
    return totals


def monthly_summary(expenses, month, budget=None):
    """Return a dictionary describing spending for one month."""
    totals = category_totals(expenses)
    total = round(sum(totals.values()), 2)
    summary = {
        "month": month,
        "count": len(expenses),
        "total": total,
        "totals": totals,
        "top_category": max(totals, key=totals.get) if totals else None,
        "budget": budget,
        "remaining": None,
        "percent_used": None,
        "alert": None,
    }
    if budget:
        summary["remaining"] = round(budget - total, 2)
        summary["percent_used"] = round(total / budget * 100, 1)
        if total > budget:
            summary["alert"] = "OVER"
        elif total >= 0.8 * budget:
            summary["alert"] = "WARNING"
        else:
            summary["alert"] = "OK"
    return summary


def format_summary(s):
    if s["count"] == 0:
        return f"No expenses recorded for {s['month']}."
    line = "-" * 44
    out = [f"Summary for {s['month']}", line]
    for cat, amt in sorted(s["totals"].items(), key=lambda x: x[1], reverse=True):
        share = amt / s["total"] * 100
        out.append(f"{cat:<14} Rs {amt:>9.2f} {share:>5.1f}% {'#' * int(share // 5)}")
    out += [
        line,
        f"{'Total':<14} Rs {s['total']:>9.2f}",
        f"Transactions: {s['count']}",
        f"Highest spending category: {s['top_category']}",
    ]
    if s["budget"]:
        out.append(
            f"Budget: Rs {s['budget']:.2f} | Used: {s['percent_used']}% "
            f"| Remaining: Rs {s['remaining']:.2f}"
        )
        out.append({
            "OVER": "ALERT: budget exceeded!",
            "WARNING": "Warning: 80% or more of the budget is used.",
            "OK": "Within budget.",
        }[s["alert"]])
    return "\n".join(out)


def format_table(expenses):
    if not expenses:
        return "No expenses found."
    line = "-" * 58
    out = [f"{'ID':<4} {'Date':<11} {'Category':<14} {'Amount':>10}  Note", line]
    for e in expenses:
        out.append(f"{e.id:<4} {e.date:<11} {e.category:<14} {e.amount:>10.2f}  {e.note}")
    out += [line, f"Total: Rs {sum(e.amount for e in expenses):.2f}"]
    return "\n".join(out)


def export_csv(expenses, path):
    """Write expenses to a CSV file and return the number of rows written."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "category", "amount", "note"])
        for e in expenses:
            writer.writerow([e.id, e.date, e.category, f"{e.amount:.2f}", e.note])
    return len(expenses)
