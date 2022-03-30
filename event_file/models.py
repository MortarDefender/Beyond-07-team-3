from django.db import models

from events.models import EventParticipant


class EventFile(models.Model):
    participant_id = models.ForeignKey(EventParticipant, on_delete=models.CASCADE)
    file = models.FileField(upload_to="files")

    def __str__(self) -> str:
        return f"{self.file.name}"
