from audit_log.models.managers import AuditLog
from django.db import models


class MyModel(models.Model):
    """A model that uses both audit log and model translation."""

    title = models.CharField(max_length=50)
    text = models.TextField()

    audit_log = AuditLog()
