from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        """Test that the homepage loads correctly and initializes the session."""
        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'board', response.data)
            self.assertIn(b'form', response.data)
            self.assertIn('board', session)
            self.assertIn('score', session)
            self.assertIn('played', session)
            self.assertIn('high_score', session)
            self.assertEqual(session['score'], 0)
            self.assertEqual(session['played'], 0)
            self.assertEqual(session['high_score'], 0)

    def test_check_word_ok(self):
        """Test that a valid word on the board is recognized."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "N", "P"],
                                 ["D", "O", "G", "L", "Q"],
                                 ["M", "A", "T", "S", "B"],
                                 ["R", "E", "Z", "H", "C"],
                                 ["W", "X", "Y", "U", "V"]]
            response = client.get('/check-word?word=cat')
            self.assertEqual(response.json['result'], 'ok')

    def test_check_word_not_on_board(self):
        """Test that a valid word not on the board is recognized."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "N", "P"],
                                 ["D", "O", "G", "L", "Q"],
                                 ["M", "A", "T", "S", "B"],
                                 ["R", "E", "Z", "H", "C"],
                                 ["W", "X", "Y", "U", "V"]]
            response = client.get('/check-word?word=dog')
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_check_word_not_a_word(self):
        """Test that an invalid word is recognized."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "N", "P"],
                                 ["D", "O", "G", "L", "Q"],
                                 ["M", "A", "T", "S", "B"],
                                 ["R", "E", "Z", "H", "C"],
                                 ["W", "X", "Y", "U", "V"]]
            response = client.get('/check-word?word=xyz')
            self.assertEqual(response.json['result'], 'not-word')

    def test_post_score(self):
        """Test posting the score updates session and returns correct data."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['score'] = 0
                sess['played'] = 0
                sess['high_score'] = 0

            response = client.post('/post-score', json={'score': 10})
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['played'], 1)
            self.assertEqual(data['high_score'], 10)
            self.assertEqual(session['played'], 1)
            self.assertEqual(session['high_score'], 10)

            response = client.post('/post-score', json={'score': 5})
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['played'], 2)
            self.assertEqual(data['high_score'], 10)
            self.assertEqual(session['played'], 2)
            self.assertEqual(session['high_score'], 10)
