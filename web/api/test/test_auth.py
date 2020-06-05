from unittest import TestCase

from api.models import PersonSchema
from api.test.dummy_data import *
from api.test.tests import get_test_app


class ApiAuthTest(TestCase):
    def setUp(self) -> None:
        self.app = get_test_app()

    def test_register_user(self):
        with self.app.test_client() as app:
            person1 = DummyPerson.create_random()
            person_json = PersonSchema(exclude=['id', 'person_type']).dumps(person1)

            response = app.post('api/auth/register', json=person_json)
            self.assertEqual(201, response.status_code)
            new_person = Person.query.filter_by(username=person1.username).first()
            self.assertNotEqual(person1.password_hashed, new_person.password_hashed)

    def test_registered_user_can_log_in(self):
        with self.app.test_client() as app:

            person1 = DummyPerson.create_random()
            person_json = PersonSchema(exclude=['id', 'person_type']).dumps(person1)

            response = app.post('api/auth/register', json=person_json)
            self.assertEqual(201, response.status_code)

            data = {
                'username': person1.username,
                'password': person1.password_hashed  # note: this is the unhased password
            }
            response = app.post('api/auth/login', json=data)
            self.assertTrue('access_token' in response.get_json())

    def test_registered_user_can_access_protected_endpoint(self):
        with self.app.test_client() as app:
            person1 = DummyPerson.create_random()
            person_json = PersonSchema(exclude=['id', 'person_type']).dumps(person1)
            response = app.post('api/auth/register', json=person_json)
            data = {
                'username': person1.username,
                'password': person1.password_hashed  # note: this is the unhased password
            }
            response = app.post('api/auth/login', json=data)
            token = response.get_json().get('access_token')

            response = app.get('api/auth/protected', headers={'Authorization': 'Bearer ' + token})
            self.assertEqual(200, response.status_code)
