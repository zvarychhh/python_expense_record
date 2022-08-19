import unittest
from unittest.mock import patch

from app import App


def get_input(text):
    return input(text)


class AppTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = App()

    def test_default_name(self):
        self.assertEqual(self.app.u_name, None)

    def test_default_id(self):
        self.assertEqual(self.app.u_id, None)

    def test_validate(self):
        self.assertFalse(self.app.validate('asdasd'))
        self.assertFalse(self.app.validate('19.08.2002'))
        self.assertFalse(self.app.validate('2020-20-20'))
        self.assertTrue(self.app.validate('2023-05-18'))
        self.assertTrue(self.app.validate('2002-02-02'))

    @patch('builtins.input', return_value='bdsadas')
    def test_registration_positive(self, input):
        self.assertEqual(self.app.registration(), 'Cтворено')
        self.app.cur.execute('''DELETE FROM USERS where Username=?''', (self.app.u_name,))
        self.app.connection.commit()

    @patch('builtins.input', return_value='Andrew')
    def test_registration_negative(self, input):
        self.assertEqual(self.app.registration(), 'Користувач з іменем — Andrew вже існує.')

    @patch('builtins.input', return_value='Andrew')
    def test_authorization_positive(self, input):
        self.assertEqual(self.app.authorization(), 'Ви успішно ввійшли як Andrew')
        self.assertEqual(self.app.u_name, 'Andrew')
        self.assertEqual(self.app.u_id, 1)

    @patch('builtins.input', return_value='Igor')
    def test_authorization_negative(self, input):
        self.assertEqual(self.app.authorization(), 'Користувача з іменем — Igor неіснує.')
        self.assertEqual(self.app.u_name, None)
        self.assertEqual(self.app.u_id, None)


if __name__ == '__main__':
    unittest.main()
