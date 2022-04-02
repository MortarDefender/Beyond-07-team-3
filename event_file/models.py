import os
from django.db import models
from events.models import EventParticipant


def upload_to_function(instance, filename):
    return os.path.join(f"files/{instance.participant_id.event_id.id}/", filename.split("/")[-1])


class EventFile(models.Model):
    participant_id = models.ForeignKey(EventParticipant, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_function)

    def __str__(self) -> str:
        return f"{self.file.name}"
