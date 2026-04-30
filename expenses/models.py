from django.db import models
from django.conf import settings

class Expense(models.Model):
    id = models.TextField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses",
    )
    date_start = models.TextField(blank=True, null=True)
    hashtag = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tbl_expenses"

    def __str__(self):
        return f"{self.summary} ({self.amount})"