from django.db import models
from django.utils import timezone
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from events.models import EventParticipant


class Method(models.TextChoices):
    SITE =  "st", _("site")
    EMAIL = "em", _("email")
    BOTH =  "bt", _("both")


class Reminder(models.Model):
    participant_id = models.ForeignKey(EventParticipant, on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=2, choices=Method.choices, default=Method.SITE)
    date_time = models.DateTimeField()
    message = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.participant_id} - {self.date_time}"
    
    def check_date(self, date_time):
        
        if date_time is not None:
            if date_time < timezone.now():
                raise ValidationError("the reminder should be to a future event and not a past event")
        else:
            raise ValidationError("date time field should not be left blank")

    def clean(self) -> None:
        self.check_date(self.date_time)
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
