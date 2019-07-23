"""
    py.test file configuration for reusing pre-populated test-urbvan
"""
import pytest
from django.db import connections
from django.db.utils import ConnectionDoesNotExist
from django.core.management import call_command

@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    import os

    homePath = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(os.path.split(__file__)[0])))
    )
    with django_db_blocker.unblock():
        with connections["local"].cursor() as cursor:
            cursor.execute('TRUNCATE TABLE subscriptions_subscription RESTART IDENTITY CASCADE')
        response = call_command(
            "loaddata", os.path.join(homePath, "fixtures", "initial_data.json")
        )
        print(response)


@pytest.fixture
def db_access_without_rollback_and_truncate(
    request, django_db_setup, django_db_blocker
):
    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
