# BudgetMgt – Ad Campaign Budget Management System

## Overview

This system manages advertising campaign budgets for brands. Each brand has:
- Daily and monthly budget limits.
- Campaigns with allowed time windows (dayparting).

The backend ensures:
- Spend tracking in real-time.
- Campaigns pause when budget is exhausted.
- Campaigns reactivate when budget resets.
- Campaigns only run during allowed hours.

## Stack

- Django (ORM, Admin, Business Logic)
- Celery (Task Scheduling)
- SQLite (Database)
- Static Typing (mypy, Python type hints)

## Setup Instructions

```bash
# Clone the repository
git clone https://github.com/UyiEke/BudgetMgt.git
cd BudgetMgt

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the Django server
python manage.py runserver

# Start Celery worker (in another terminal)
celery -A ad_agency worker --loglevel=info

# Start Celery beat for periodic tasks
celery -A ad_agency beat --loglevel=info
```

## Daily Workflow

1. Celery runs spend checks every minute.
2. If a campaign exceeds budget or is out of its scheduled time, it is paused.
3. At midnight, daily budgets reset.
4. On the 1st of each month, monthly budgets reset.
5. If budgets allow, eligible campaigns are reactivated.

## Assumptions & Simplifications

- All times are treated as UTC.
- Spend increments are simulated (no real ad spend tracking).
- Campaign run logic is simplified — a boolean field controls if a campaign is "active".
