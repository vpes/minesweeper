from django.contrib.auth.models import User as BaseUser
from django.db import models


class User(BaseUser):
    """
        User model for persisting and resume methods
    """
    pass

    class Meta:
        managed = True
        db_table = "user"

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def name(self):
        return '{pre}{first_name} {last_name}'.format(
            pre='Admin: ' if self.is_admin else '',
            first_name=self.first_name,
            last_name=self.last_name
        )

    def get_short_name(self):
        if self.first_name and self.last_name:
            return "{first_name} {first_letter}.".format(
                first_name=self.first_name,
                first_letter=self.last_name[0].upper()
            )
        else:
            return self.username

    def __str__(self):
        return self.name