from unittest.mock import patch, PropertyMock
from memsource import api, models, constants
import requests
import datetime
import api as api_test


class TestApiDomain(api_test.ApiTestCase):
    def setUp(self):
        self.url_base = 'https://cloud1.memsource.com/web/api/v3/project'
        self.project = api.Project(None)

    @patch.object(requests, 'request')
    def test_create(self, mock_request):
        type(mock_request()).status_code = PropertyMock(return_value=200)
        returning_id = self.gen_random_int()
        mock_request().json.return_value = {
            'id': returning_id
        }

        name = 'test project'
        source_lang = 'en'
        target_lang = 'ja'
        client = self.gen_random_int()
        domain = self.gen_random_int()

        self.assertEqual(
            self.project.create(name, source_lang, target_lang, client, domain),
            returning_id,
            "create function returns id value of JSON"
        )
        mock_request.assert_called_with(
            constants.HttpMethod.post.value,
            '{}/create'.format(self.url_base),
            params={
                'token': self.project.token,
                'name': name,
                'sourceLang': source_lang,
                'targetLang': target_lang,
                'client': client,
                'domain': domain,
            },
            files={},
            timeout=constants.Base.timeout.value
        )

    @patch.object(requests, 'request')
    def test_list(self, mock_request):
        type(mock_request()).status_code = PropertyMock(return_value=200)

        mock_request().json.return_value = [
            {
                'id': self.gen_random_int(),
                'name': 'test project 1',
                'status': 'NEW',
                'sourceLang': 'en',
                'targetLangs': ['ja'],
                'dateDue': None,
                'dateCreated': '2013-05-10T15:31:31Z',
                'note': 'test project note 1'
            },
            {
                'id': self.gen_random_int(),
                'name': 'test project 2',
                'status': 'NEW',
                'sourceLang': 'en',
                'targetLangs': ['cs'],
                'dateDue': None,
                'dateCreated': '2013-05-10T15:31:31Z',
                'note': 'test project note 2'
            }
        ]

        for project in self.project.list():
            self.assertIsInstance(project, models.Project)
            self.assertIsInstance(project.date_created, datetime.datetime)

        mock_request.assert_called_with(
            constants.HttpMethod.post.value,
            '{}/list'.format(self.url_base),
            params={
                'token': self.project.token,
            },
            files={},
            timeout=constants.Base.timeout.value
        )

    @patch.object(requests, 'request')
    def test_get_trans_memories(self, mock_request):
        type(mock_request()).status_code = PropertyMock(return_value=200)
        project_id = self.gen_random_int()

        mock_request().json.return_value = [{
            'writeMode': True,
            'transMemory': {
                'id': 1,
                'targetLangs': ['ja'],
                'sourceLang': 'en',
                'name': 'transMem'
            },
            'targetLang': 'ja',
            'penalty': 0,
            'readMode': True,
            'workflowStep': None
        }]

        returned_values = self.project.getTransMemories(project_id)

        mock_request.assert_called_with(
            constants.HttpMethod.post.value,
            '{}/getTransMemories'.format(self.url_base),
            params={
                'token': self.project.token,
                'project': project_id
            },
            files={},
            timeout=constants.Base.timeout.value
        )

        self.assertEqual(len(returned_values), len(mock_request().json()))

        for translation_memory in returned_values:
            self.assertIsInstance(translation_memory, models.TranslationMemory)
