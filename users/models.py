from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )

    phone_number = models.CharField(max_length=10)

    profile_pic = models.ImageField(upload_to="images", default="")

    def __str__(self) -> str:
        return self.user.username

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
    
    def phone_validation(self, phone_number):

        if phone_number is not None:
            pass

    def clean(self) -> None:
        self.phone_validation(self.phone_number)
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
