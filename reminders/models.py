from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from events.models import EventParticipant
from datetime import datetime
from events.models import time_format

# def validate_date(date_time):
#     if timezone.now() < date_time:
#         pass
#     else:
#         raise ValidationError(
#             _('%(date_time)s is not a valid date_time'),
#             params={'date time': date_time}, )

def validate_date(date_time):
    if timezone.now() > date_time:
        raise ValidationError(f'{time_format(date_time)} is not a valid date_time')


class Reminder(models.Model):
    class EMethods(models.TextChoices):
        WEBSITE = "web", "Website"
        EMAIL = "ema", "Email"
        WEBSITE_EMAIL = "wae", "Website and Email"

    participant_id = models.ForeignKey(EventParticipant, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now, validators=[validate_date])
    messages = models.TextField(null=True, blank=True)

    method = models.CharField(
        max_length=3,
        choices=EMethods.choices,
        default=EMethods.WEBSITE,
    )

    def validate_unique_reminder(self, participant, date_time):
        if Reminder.objects.filter(participant_id__user_id=participant.user_id,
                                   participant_id__event_id=participant.event_id, 
                                   date_time=date_time):
            raise ValidationError('reminder already exists')

    def __str__(self):
        return f"{self.participant_id} - {self.date_time}"

    def clean(self):
        validate_date(self.date_time)
        self.validate_unique_reminder(self.participant_id, self.date_time)
        return super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)