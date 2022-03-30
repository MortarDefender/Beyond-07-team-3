from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import validate_email
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    User._meta.get_field('email')._unique = True

    phone_number = PhoneNumberField(blank=True, unique=True)

    profile_pic = models.ImageField(upload_to="images", default="avatar.svg")

    def __str__(self) -> str:
        return f"{self.user.username}"

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    def clean(self) -> None:
        # validate_email(self.email)
        return super().clean()
    
    def save(self, *args, **kwargs):
        print(self.user.username)
        print(self.user.password)
        print(self.user.email)
        print(self.phone_number)
        print(self.profile_pic)
        self.clean()
        return super().save(*args, **kwargs)
