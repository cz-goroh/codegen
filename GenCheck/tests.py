from uuid import uuid4
from faker import Faker
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from random import randint
import json

class BaseTestSetUp(APITestCase):
    def create_user(self, name, password):
        return User.objects.create_user(name, password=password)

    def setUp(self):
        self.fake = Faker()
        self._username = self.fake.first_name()
        self._userpass = str(uuid4())
        self.user = self.create_user(self._username, self._userpass)
        auth_url = '/api/api-token-auth/'
        auth_resp = self.client.post(auth_url, {
            'username': self._username,
            'password': self._userpass
        })
        self.client.force_authenticate(user=self.user, token=None)

    def generate_data(self):
        url = f"/api/generate/"

        data = [
            {
                'group': self.fake.first_name(), 'amount': randint(20, 40)
            } for r in range(10)
        ]
        resp = self.client.post(url, data, format='json')
        return data, resp

    def test_generate_view(self):
        data, resp = self.generate_data()
        self.assertEqual(resp.status_code, 200)
        rjson = resp.json()
        fl = open('groups.json', 'r')
        fl_cont = json.load(fl)
        for gr, uid_list in fl_cont.items():
            for uid in rjson['groups_dict'][gr]:
                self.assertTrue(uid in fl_cont[gr])
        fl.close()


    def test_check_code_view(self):
        self.generate_data()
        fl = open('groups.json', 'r')
        fl_cont = json.load(fl)
        for gr, uid_list in fl_cont.items():
            uid_test = uid_list[0]
            test_gr = gr
            break
        resp = self.client.get('/api/check_code/', {'key': uid_test})
        self.assertEqual(resp.json()['is_exists'], True)
        self.assertEqual(resp.json()['group'], test_gr)
        fake_uid = str(uuid4())
        resp = self.client.get('/api/check_code/', {'key': fake_uid})
        self.assertEqual(resp.json()['is_exists'], False)
