from django.test import TestCase


class UserTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_register(self):
        res = self.client.post('/user/register', {})
        self.assertEqual(res.status_code, 400)
        data = res.data
        self.assertEqual(data['status'], 'fail')
