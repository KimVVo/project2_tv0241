import unittest
from http.server import HTTPServer
from datetime import datetime, timezone
import threading
import requests
import jwt

# Import the server code here
from main import MyServer, init_db, hostName, serverPort

class TestHTTPServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the database and start the server
        init_db()
        cls.server = HTTPServer((hostName, serverPort), MyServer)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()
        # Optionally add cleanup for the database here

    def test_jwks_endpoint(self):
        url = f"http://{hostName}:{serverPort}/.well-known/jwks.json"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        keys = response.json()
        self.assertIn("keys", keys)
        self.assertGreater(len(keys["keys"]), 0)

    def test_auth_endpoint(self):
        url = f"http://{hostName}:{serverPort}/auth"
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
        token = response.text
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        self.assertIn("user", decoded)
        self.assertEqual(decoded["user"], "username")
        self.assertIn("exp", decoded)
        self.assertGreater(decoded["exp"], datetime.now(timezone.utc).timestamp())

    def test_auth_endpoint_expired(self):
        url = f"http://{hostName}:{serverPort}/auth?expired=true"
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
        token = response.text
        decoded = jwt.decode(token, options={"verify_signature": False})

        self.assertIn("user", decoded)
        self.assertEqual(decoded["user"], "username")
        self.assertIn("exp", decoded)
        self.assertLess(decoded["exp"], datetime.now(timezone.utc).timestamp())

    def test_invalid_methods(self):
        url = f"http://{hostName}:{serverPort}/auth"
        methods = ["PUT", "PATCH", "DELETE", "HEAD"]
        for method in methods:
            response = requests.request(method, url)
            self.assertEqual(response.status_code, 405)

    def test_keys_endpoint(self):
        url = f"http://{hostName}:{serverPort}/keys"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        keys = response.json()
        self.assertGreater(len(keys), 0)
        for key in keys:
            self.assertIn("kid", key)
            self.assertIn("key", key)
            self.assertIn("exp", key)

if __name__ == "__main__":
    unittest.main()
