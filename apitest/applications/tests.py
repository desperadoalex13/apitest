from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from applications.models import Application, ApplicationApiKey

User = get_user_model()


class ApplicationViewSetTest(TestCase):

    def setUp(self):
        self.rest_client = APIClient()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_crud_application(self):
        self.rest_client.force_authenticate(user=self.user)
        url = reverse('applications-list')

        data = {
            'name': 'Application test 1'
        }
        response = self.rest_client.post(url, data, format='json')
        answer = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1, msg='Creation doesn\'t work')
        self.assertEqual(Application.objects.get().user, self.user)
        self.assertEqual(Application.objects.get().name, data["name"])
        self.assertIn('api_key', answer)
        self.assertTrue(answer['api_key'])

        url_details = reverse('applications-detail', kwargs={'pk': answer['id']})

        response = self.rest_client.get(url_details)
        answer = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='Retrive doesn\'t work')
        self.assertIn('id', answer)
        self.assertIn('name', answer)

        edit_data = {
            'name': 'Application test edit'
        }
        response = self.rest_client.put(url_details, edit_data, format='json')
        answer = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='Update doesn\'t work')
        self.assertEqual(answer['name'], edit_data['name'])

        generate_key_url = reverse('applications-regenerate-token', kwargs={'pk': answer['id']})
        response = self.rest_client.post(generate_key_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='Generation api doesn\'t work')
        answer = response.json()
        current_api_key = answer['api_key']

        test_url = reverse('applications-test')
        clean_api_client = APIClient()
        clean_api_client.credentials(HTTP_AUTHORIZATION='Api-Key {}'.format(current_api_key))
        response = clean_api_client.get(test_url, format='json')
        answer = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='API key doesn\'t work')
        self.assertIn('id', answer)
        self.assertIn('name', answer)

        response = self.rest_client.delete(url_details, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg='Deletion doesn\'t work')
        self.assertEqual(Application.objects.count(), 0)
