import unittest
from app import create_app, db

class MissionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.app_context().push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_mission(self):
        response = self.client.post("/missions", json={
            "name": "Apollo 11",
            "launch_date": "1969-07-16",
            "destination": "Moon",
            "status": "Completed",
            "crew": "Neil Armstrong, Buzz Aldrin",
            "payload": "Lunar Module",
            "duration": "8 days",
            "cost": 1000000.0,
            "mission_status": "Successful"
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
