from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import Profile


def validate_date_time(starting_date, ending_date):

    if starting_date is not None and ending_date is not None:
        if starting_date >= ending_date:
            raise ValidationError("the statring date time should be greater then the ending date time")
    else:
        raise ValidationError("date time fileds should not be left empty")


class Colors(models.TextChoices):
    RED = 'rd', _("Red")
    BLUE = 'bl', _("Blue")
    GREEN = 'gr', _("Green")
    BLACK = 'bc', _("Black")
    YELLOW = 'ye', _("Yellow")


class Event(models.Model):

    title = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    date_time_start = models.DateTimeField()
    date_time_end = models.DateTimeField()
    description = models.TextField()

    color = models.CharField(max_length=2, choices=Colors.choices, default=Colors.BLUE)

    def __str__(self) -> str:
        return f"{self.title} - {self.date_time_start}"

    def clean(self) -> None:
        if self.title is None or self.title == "":
            raise ValidationError("title cannot be blank")

        validate_date_time(self.date_time_start, self.date_time_end)
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class EventParticipant(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_creator = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.user_id} - {self.event_id}"


class PossibleMeeting(models.Model):
    prticipant_id = models.ForeignKey(EventParticipant, on_delete=models.CASCADE)
    date_time_start = models.DateTimeField()
    date_time_end = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.prticipant_id} - {self.date_time_start}"

    def clean(self) -> None:
        validate_date_time(self.date_time_start, self.date_time_end)
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
