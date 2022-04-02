from django.core.files import File
from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('event_file', '0001_initial'),
        ('users', '0003_createsuperuser'),
        ('events', '0004_add_event_participant_test_data')
    ]

    def generate_event_file_test_data(apps, schema_editor):
        from event_file.models import EventFile
        from events.models import EventParticipant

        test_file1 = File(open("media/test_files/test_file1.txt"))
        test_file2 = File(open("media/test_files/test_file2.txt"))
        test_file3 = File(open("media/test_files/test_file3.txt"))

        reminder_data = [
            (EventParticipant.objects.get(event_id__title="event1", user_id__username="testUser1"), test_file1),
            (EventParticipant.objects.get(event_id__title="event2", user_id__username="testUser3"), test_file2),
            (EventParticipant.objects.get(event_id__title="event1", user_id__username="testUser2"), test_file3)
        ]

        with transaction.atomic():
            for participant_id, file in reminder_data:
                reminder = EventFile(participant_id=participant_id, file=file)
                reminder.save()

    operations = [
        migrations.RunPython(generate_event_file_test_data),
    ]
