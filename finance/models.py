from django.db import models
from django.conf import settings


class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        unique_together = ['name', 'type']

    def __str__(self):
        return f"{self.name} ({self.type})"


class Record(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='records'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='records'
    )

    is_deleted = models.BooleanField(default=False)

    date = models.DateField(db_index=True)

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
       return f"{self.user.email} - {self.category.name} - {self.amount}"