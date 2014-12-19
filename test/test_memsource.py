import unittest
from unittest.mock import patch, PropertyMock
from memsource import Memsource, constants
import requests


class TestMemsource(unittest.TestCase):
    def setUp(self):
        self.url_base = 'https://cloud1.memsource.com/web/api/v3/auth/login'

    def check_token(self, m, token):
        for api in ('client', 'domain', 'project', 'job', ):
            self.assertEqual(getattr(m, api).token, token)

    @patch.object(requests, 'request')
    def test_init_with_user_name_and_password(self, mock_request):
        type(mock_request()).status_code = PropertyMock(return_value=200)

        token = 'test_token'
        mock_request().json.return_value = {
            'token': token,
            'user': {},
        }

        username = 'test_username'
        password = 'test_password'
        self.check_token(Memsource(user_name=username, password=password), token)

        mock_request.assert_called_with(
            constants.HttpMethod.post.value,
            self.url_base,
            params={
                'userName': username,
                'password': password,
                'token': None,
            },
            files={},
            timeout=constants.Base.timeout.value
        )

    @patch.object(requests, 'request')
    def test_init_with_token(self, mock_request):
        token = 'test_token'
        self.check_token(Memsource(token=token), token)

        # When token is given as parameter, never send http request.
        self.assertFalse(mock_request.called)

    @patch.object(requests, 'request')
    def test_init_with_user_name_and_password_and_token(self, mock_request):
        token = 'test_token'
        m = Memsource(user_name='test user name', password='test password', token=token)
        self.check_token(m, token)

        # When token is given as parameter, never send http request.
        self.assertFalse(mock_request.called)
