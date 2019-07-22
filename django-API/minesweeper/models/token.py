from django.conf import settings
from django.db import models
from django.utils import timezone

from datetime import timedelta
import string

class Token(models.Model):
    """Access token keys model."""

    key = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    expiration_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    # Metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "token"
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def save(self, *args, **kwargs):
        """Overwrite save function.

        Add key value, update expiration date and
        activate/deactivate other owner's keys.
        """
        if not self.key:
            self.key = self.generate_key()
        if not self.pk:
            self.reload_expiration_date()
            q = Token.objects.filter(user=self.user, is_active=True)
            if q:
                for _ in q:
                    _.is_active = False
                    _.save()
        return super(Token, self).save(*args, **kwargs)

    def __str__(self):
        """Return key value."""
        return self.key

    def reload_expiration_date(self):
        """Add 30 days to key expiration."""
        ed = timezone.now() + timedelta(days=30)
        # Add expiration_date
        self.expiration_date = ed
        # re-active token
        self.is_active = True

    def generate_key(self):
        """Create key value.

        Generate key by choosing N characters inside
        a pool containing upper and lower case letters
        and digits from 0 to 9. The key lenght is a
        value between 120 and 200.
        """
        from Crypto.Random import random
        pool = string.ascii_letters + ''.join([str(x) for x in range(10)])
        key = ''.join([random.choice(pool) for x in range(random.randint(120, 200))]) # NOQA
        return key

