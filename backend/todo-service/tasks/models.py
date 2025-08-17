from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # This field will store the ID of the user who owns this todo.
    # We are simply storing an integer because the actual user data
    # resides in a completely separate database (User Service).
    user_id = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
