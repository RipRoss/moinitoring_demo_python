from datetime import timedelta
import random
from models import Address, User
from faker import Faker
import requests
from celery import Celery


FAKE = Faker()


APP = Celery('tasks', broker='redis://localhost:6379/0')

APP.conf.beat_schedule = {
    'create_new_users_task': {
        'task': 'tasks.create_new_users',
        'schedule': timedelta(minutes=1),
    },
}

APP.conf.timezone = 'UTC'


@APP.task
def create_new_users():
    num = random.randint(1, 10)
    for i in range(num):
        request_dict = _generate_fake_user().dict()
        response = requests.post('http://localhost:8000/data', json=request_dict)
        response.raise_for_status()

        # TODO: Make sure this is proper logging
        print(f"User {i+1}/{num} created")



def _generate_fake_user():
    return User(
        first_name=FAKE.first_name(),
        last_name=FAKE.last_name(),
        addresses=[_generate_fake_address()],
        username=FAKE.user_name(),
        password=FAKE.password(),
        email=FAKE.email()
    )



def _generate_fake_address():
    return Address(
        house_number=FAKE.building_number(),
        house_name=FAKE.street_name(),
        street_name=FAKE.street_name(),
        post_code=FAKE.postcode()
    )


if __name__ == '__main__':
    create_new_users()