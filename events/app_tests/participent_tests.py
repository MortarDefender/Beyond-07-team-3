from users.tests import user0  # noqa: F401
from ..models import Event, EventParticipant
from .event_tests import new_event  # noqa: F401

import pytest


def create_event_participant(event, user, is_creator):
    return EventParticipant(event_id=event, user_id=user, is_creator=is_creator)


@pytest.fixture
def event_participant_creator(new_event, user0):  # noqa: F811
    return create_event_participant(new_event, user0, True)


@pytest.fixture
def event_participant_not_creator(new_event, user0):  # noqa: F811
    return create_event_participant(new_event, user0, False)


@pytest.fixture
def persist_event_participant(event_participant_creator):
    event_participant_creator.event_id.save()
    event_participant_creator.user_id.save()
    event_participant_creator.save()
    return event_participant_creator


@pytest.mark.django_db
def test_persist_event_participant(persist_event_participant):
    assert persist_event_participant in EventParticipant.objects.all()


@pytest.mark.django_db
def test_delete_event_participant(persist_event_participant):
    persist_event_participant.delete()
    assert persist_event_participant not in EventParticipant.objects.all()


@pytest.mark.django_db
def test_delete_user_deletes_participant(persist_event_participant):
    persist_event_participant.user_id.delete()
    assert persist_event_participant not in EventParticipant.objects.all()


@pytest.mark.django_db
def test_exist_event_participant():
    assert EventParticipant.objects.filter(event_id=Event.objects.get(title='event1'))
    assert EventParticipant.objects.filter(event_id=Event.objects.get(title='event2'))


@pytest.mark.django_db
def test_invalid_register_user_twice(persist_event_participant):
    with pytest.raises(Exception, match='user already exist in meeting'):
        persist_event_participant.save()
