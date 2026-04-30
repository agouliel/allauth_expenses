from django.shortcuts import render
from .gcal import get_calendar_service
from .expenses import insert_to_db
from .models import Expense
from collections import defaultdict
from calendar import month_abbr
import json

def serialize_expense(e):
    return {
        "id": e.id,
        "summary": e.summary,
        "amount": e.amount,
        "url": e.url,
    }

def show_calendar(request):
    service = get_calendar_service(request.user)
    
    if not service:
        return render(request, 'error.html', {'message': 'Google account not linked'})
    
    insert_to_db(service, request.user)

    # Fetch the newly saved expenses to show in the template
    expenses = Expense.objects.filter(user=request.user)
    #print(expenses)

    # https://chatgpt.com/c/69ef68dc-8920-8332-aca8-efc06fde66b2
    year = request.GET.get("year")

    # Filter by year (since date_start is text, we assume format "YYYY-MM-DD")
    if year:
        expenses = expenses.filter(date_start__startswith=year)

    # Build pivot: {category: {month: total}}
    pivot = defaultdict(lambda: {m: 0 for m in range(1, 13)})
    expense_map = defaultdict(list)

    for exp in expenses:
        if not exp.date_start:
            continue

        try:
            month = int(exp.date_start[5:7])
        except:
            continue

        category = exp.hashtag or "Uncategorized"

        pivot[category][month] += exp.amount or 0
        expense_map[(category, month)].append(exp)
    
    expense_map_serialized = {
        f"{category}|{month}": [serialize_expense(e) for e in expenses]
        for (category, month), expenses in expense_map.items()
    }

    # Totals
    totals_by_month = {m: 0 for m in range(1, 13)}
    totals_by_category = {}

    for category, months in pivot.items():
        totals_by_category[category] = sum(months.values())
        for m, val in months.items():
            totals_by_month[m] += val

    MONTHS = [(i, month_abbr[i]) for i in range(1, 13)]
    
    context = {
        "pivot": dict(pivot),
        "expense_map": dict(expense_map),
        "totals_by_month": totals_by_month,
        "totals_by_category": totals_by_category,
        "year": year,
        "years": sorted(
            set(
                e.date_start[:4]
                for e in Expense.objects.exclude(date_start__isnull=True)
            )
        ),
        "months": MONTHS,
        "expense_map_json": json.dumps(expense_map_serialized),
    }

    return render(request, 'expenses.html', context)