import unittest
from app import app

class FlaskURLTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form', response.data)

    def test_index_post(self):
        response = self.app.post('/', data={'url': 'https://example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shortened URL:', response.data)

    def test_shorten_post(self):
        response = self.app.post('/shorten', json={'url': 'https://example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'short_url', response.data)

    def test_shorten_post_missing_url(self):
        response = self.app.post('/shorten', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing URL', response.data)

    def test_redirect_short_url_not_found(self):
        response = self.app.get('/s/invalidid')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'URL not found', response.data)

    def test_analytics_get(self):
        response = self.app.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form', response.data)

    def test_analytics_post_missing_short_url(self):
        response = self.app.post('/analytics', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing short_url', response.data)

if __name__ == '__main__':
    unittest.main()
