from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test that the homepage is accessible and displays the Boggle board."""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<form', response.data)

    def test_valid_word(self):
        """Test that a valid word is recognized."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["T", "E", "S", "T", "T"],
                                 ["E", "S", "T", "E", "S"],
                                 ["S", "T", "E", "S", "T"],
                                 ["T", "E", "S", "T", "E"],
                                 ["E", "S", "T", "E", "S"]]
                
            response = self.client.get('/check-word?word=test')
            self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test that an invalid word is rejected."""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')
        
    def test_post_score(self):
        """Test updating score and games played count."""

        with self.client:
            response = self.client.post("/post-score", json={"score": 5})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            self.assertEqual(data["games_played"], 1)
            self.assertEqual(data["high_score"], 5)

            # Now let's send a new score which is lower than the high score and check that high score doesn't change
            response = self.client.post("/post-score", json={"score": 3})
            data = response.get_json()
            self.assertEqual(data["games_played"], 2)
            self.assertEqual(data["high_score"], 5)

            # Now let's send a new score which is higher than the high score and check that high score changes
            response = self.client.post("/post-score", json={"score": 7})
            data = response.get_json()
            self.assertEqual(data["games_played"], 3)
            self.assertEqual(data["high_score"], 7)
