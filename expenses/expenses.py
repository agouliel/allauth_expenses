import datetime
from .models import Expense

def insert_to_db(service, user_id):
    # sync current month every time
    month_start = datetime.datetime.today().date().replace(day=1).replace(month=1).isoformat() + 'T00:00:00.000000Z'
    month_end = datetime.datetime.today().date().isoformat() + 'T00:00:00.000000Z'

    events_result = service.events().list(calendarId='primary',
                                            timeMin=month_start,
                                            timeMax=month_end,
                                            singleEvents=True,
                                            orderBy='startTime').execute()

    events = events_result.get('items', [])
    print(events)

    events_with_expenses = []

    for event in events:
        parts = event.get("summary", "").split()
        
        # Check if we have enough parts and if the first part is numeric
        if parts:
            first_word = parts[0]
            last_word = parts[-1]
            
            # This check handles both integers and decimals
            if first_word.replace('.', '', 1).isdigit() and last_word.startswith('#'):
                print(event)
                amount = float(first_word)
                hashtag = parts[-1]
                
                event_with_expense = {
                    'id': event.get('id'),
                    'user': user_id,
                    'date_start': event['start']['dateTime'][:10],
                    'hashtag': hashtag[1:],
                    'summary': ' '.join(parts[1:-1]),
                    'amount': amount,
                    'url': event.get('htmlLink')
                }
                events_with_expenses.append(event_with_expense)
    # end for event in events

    for event in events_with_expenses:
        # Use update_or_create to prevent duplicates based on the Google Event ID
        Expense.objects.update_or_create(
            id=event['id'],
            defaults={
                'user': event.get('user'),
                'date_start': event.get('date_start'),
                'hashtag': event.get('hashtag'),
                'summary': event.get('summary', 'No Title'),
                'amount': event.get('amount'),
                'url': event.get('url'),
            }
        )