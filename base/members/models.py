from django.db import models
from django.contrib.auth.models import User
from synopsis.models import Book
from django.db.models.signals import post_save
from django.dispatch import receiver


class Member(models.Model):
    '''The member model is linked to the django user 
    model via a decorator,
    When a new user is created the new user is automatically 
    associated to a new member object
    the member object oprovides additional information to the standard 
    User model without the neeed for extra model in admin.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked_books = models.ManyToManyField(Book, symmetrical=False, blank=True)
    seen_instructions = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# automatically create a profile when user is created.


@receiver(post_save, sender=User)
def create_new_member(sender, instance, created, **kwargs):
    if created:
        member_profile = Member(user=instance)
        member_profile.save()


# post_save.connect(create_new_member, sender=User)  # alternate save method
