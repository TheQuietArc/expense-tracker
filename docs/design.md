# Design Document

Diagrams are written in Mermaid, which GitHub renders automatically.
Copy each into https://mermaid.live to export it as an image for the report.

## 1. System Architecture
```mermaid
flowchart LR
    U[User / Terminal] --> M[main.py]
    M --> C[cli.py<br/>parse and dispatch]
    C --> V[validators.py]
    C --> MG[manager.py<br/>business logic]
    C --> R[reports.py<br/>summary / table / CSV]
    MG --> V
    MG --> ST[storage.py]
    MG --> MD[models.py]
    ST --> F[(expenses.json)]
    R --> CSV[(expenses.csv)]
    C --> L[logger.py]
    L --> LF[(expense_tracker.log)]
```

## 2. Workflow Diagram
```mermaid
flowchart TD
    A([Start]) --> B[User runs a command]
    B --> C{Arguments valid?}
    C -- No --> X[Show usage error]
    C -- Yes --> D[Load data from JSON]
    D --> E{Input passes validation?}
    E -- No --> F[Print error, log warning, exit 1]
    E -- Yes --> G{Command type}
    G -- add/delete/budget --> H[Update data and save atomically]
    G -- list/search --> I[Filter / sort / match]
    G -- summary --> J[Aggregate by category, compare to budget]
    G -- export --> K[Write CSV file]
    H --> L[Print result]
    I --> L
    J --> L
    K --> L
    L --> M([End])
    F --> M
    X --> M
```

## 3. Use Case Diagram
```mermaid
flowchart LR
    S((Student))
    subgraph Expense Tracker
        UC1[Add expense]
        UC2[List / filter / sort expenses]
        UC3[Search expenses]
        UC4[Delete expense]
        UC5[Set monthly budget]
        UC6[View monthly summary]
        UC7[Export to CSV]
    end
    S --> UC1
    S --> UC2
    S --> UC3
    S --> UC4
    S --> UC5
    S --> UC6
    S --> UC7
```

## 4. Sequence Diagram (adding an expense)
```mermaid
sequenceDiagram
    actor User
    participant CLI as cli.py
    participant Mgr as ExpenseManager
    participant Val as validators.py
    participant Sto as JsonStorage
    User->>CLI: add 120 food --note "lunch"
    CLI->>Mgr: add(amount, category, note, date)
    Mgr->>Val: validate amount, category, date, note
    Val-->>Mgr: cleaned values (or ValidationError)
    Mgr->>Mgr: create Expense with next ID
    Mgr->>Sto: save(data)
    Sto-->>Mgr: written atomically
    Mgr-->>CLI: Expense
    CLI-->>User: Added expense #1
```

## 5. Class / Component Diagram
```mermaid
classDiagram
    class Expense {
        +int id
        +str date
        +float amount
        +str category
        +str note
        +to_dict()
        +from_dict(data)
    }
    class ExpenseManager {
        -list expenses
        +float budget
        +add(amount, category, note, date)
        +list(category, month, sort)
        +search(keyword)
        +delete(expense_id)
        +set_budget(amount)
    }
    class JsonStorage {
        +str path
        +load()
        +save(data)
    }
    class ValidationError
    class ExpenseNotFoundError
    ExpenseManager "1" o-- "*" Expense
    ExpenseManager --> JsonStorage
    ExpenseNotFoundError --|> ValidationError
```

## 6. Storage Design / ER Diagram
Data is stored in one JSON file (`expenses.json`).
```mermaid
erDiagram
    STORE ||--o{ EXPENSE : contains
    STORE {
        float budget
    }
    EXPENSE {
        int id PK
        string date
        float amount
        string category
        string note
    }
```
Schema:
```json
{
  "budget": 5000.0,
  "expenses": [
    {"id": 1, "date": "2026-09-10", "amount": 120.0, "category": "food", "note": "lunch"}
  ]
}
```

## 7. Non-Functional Requirements
| Requirement | How it is met |
|---|---|
| Reliability | Atomic writes (temp file + replace); corrupt file is backed up, never crashes the tool |
| Usability | Clear commands, `--help`, plain-language error messages, exit codes |
| Maintainability | Seven small modules with one responsibility each; unit tests |
| Error handling | Central validation; `ValidationError` and `OSError` handled in one place |
| Logging | Rotating log file records adds, deletes, saves, warnings and errors |
| Performance | All operations are linear scans over a small in-memory list |
| Security / safety | Input length and range limits; no network access, no code execution from input |

## 8. Design Decisions
- **JSON over a database:** data is small and single-user; JSON needs no setup and is human-readable.
- **Separate validation module:** one place for rules, reused by manager and CLI, easy to test.
- **Manager does not print:** the business logic returns data; the CLI and `reports.py` handle display, so each can change independently.
- **Standard library only:** anyone can run the project without installing anything.
