from datetime import datetime
from users.tests import user0  # noqa: F401
from django.utils import timezone
from .event_tests import new_event  # noqa: F401
from django.core.exceptions import ValidationError
from ..models import PossibleMeeting, EventParticipant
from .participent_tests import event_participant_not_creator  # noqa: F401

import pytest


DATE_TIME_START = datetime(2022, 3, 24, 12, 12, 12, 0, tzinfo=timezone.utc)
DATE_TIME_END = datetime(2022, 3, 24, 14, 12, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def possible_meeting0(event_participant_not_creator):  # noqa: F811
    return PossibleMeeting(participant_id=event_participant_not_creator,
                           date_time_start=DATE_TIME_START, date_time_end=DATE_TIME_END)


@pytest.fixture
def persist_possible_meeting(possible_meeting0):
    possible_meeting0.participant_id.user_id.save()
    possible_meeting0.participant_id.event_id.save()
    possible_meeting0.participant_id.save()
    possible_meeting0.save()
    return possible_meeting0


@pytest.mark.django_db
def test_persist_possible_meeting(persist_possible_meeting):
    assert persist_possible_meeting in PossibleMeeting.objects.all()


@pytest.mark.django_db
def test_delete_persist_possible_meeting(persist_possible_meeting):
    persist_possible_meeting.delete()
    assert persist_possible_meeting not in PossibleMeeting.objects.all()


@pytest.mark.django_db
def test_delete_participant_deletes_possible_meeting(persist_possible_meeting):
    persist_possible_meeting.participant_id.delete()
    assert persist_possible_meeting not in PossibleMeeting.objects.all()


@pytest.mark.django_db
def test_persist_possible_meeting_Validation_Error(persist_possible_meeting):
    with pytest.raises(ValidationError):
        persist_possible_meeting.date_time_start = DATE_TIME_END
        persist_possible_meeting.date_time_end = DATE_TIME_START
        persist_possible_meeting.save()


def get_event_participant_from_db():
    return EventParticipant.objects.filter(is_creator=True)[0]


@pytest.mark.django_db
def test_persist_possible_meeting_in_db():
    assert PossibleMeeting.objects.filter(participant_id=get_event_participant_from_db())


@pytest.mark.django_db
def test_duplicate_possible_meeting(persist_possible_meeting):
    with pytest.raises(Exception, match='meeting hours already exists'):
        persist_possible_meeting.save()