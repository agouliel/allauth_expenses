# https://chatgpt.com/c/69ef68dc-8920-8332-aca8-efc06fde66b2
# no custom filter:

# pivot_items = [
#    {"category": category, "months": months, "total": sum(months.values())}
#    for category, months in pivot.items()
#]

# Then in template:
# {% for row in pivot_items %}
# <tr>
#    <td>{{ row.category }}</td>

#    {% for m, val in row.months.items %}
#        <td>{{ val }}</td>
#    {% endfor %}

#    <td>{{ row.total }}</td>
# </tr>
# {% endfor %}

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
