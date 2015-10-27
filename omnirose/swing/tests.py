import json
from datetime import datetime
import pytz

from django.test import TestCase, Client

from .models import SunSwing, SunSwingReading
from accounts.models import User

test_data = {
    # Real data from the first test swing of Olga
    "pelorus_correction": 156,
    "compass_video_start_time": 1444644781.875,
    # 2015-10-12 10:13:01.875000+00:00
    "latitude": 59.270133,
    "longitude": 18.790867,
    "readings": [
        { "compass": 20,    "shadow": 307.5,    "time": 70.6875   },
        { "compass": 30,    "shadow": 296,      "time": 74.9375   },
        { "compass": 40,    "shadow": 285.5,    "time": 78.46875  },
        { "compass": 50,    "shadow": 271,      "time": 83.46875  },
        { "compass": 60,    "shadow": 259,      "time": 87.75     },
        { "compass": 70,    "shadow": 246,      "time": 92.03125  },
        { "compass": 80,    "shadow": 235.5,    "time": 95.40625  },
        { "compass": 90,    "shadow": 224,      "time": 99.40625  },
        { "compass": 100,   "shadow": 213.5,    "time": 103.40625 },
        { "compass": 110,   "shadow": 203,      "time": 106.4375  },
        { "compass": 120,   "shadow": 191,      "time": 110.6875  },
        { "compass": 130,   "shadow": 179.5,    "time": 114.6875  },
        { "compass": 140,   "shadow": 168,      "time": 119.875   },
        { "compass": 150,   "shadow": 159.5,    "time": 122.5625  },
        { "compass": 160,   "shadow": 149,      "time": 126.9375  },
        { "compass": 170,   "shadow": 140.5,    "time": 129.78125 },
        { "compass": 180,   "shadow": 131,      "time": 133.625   },
        { "compass": 190,   "shadow": 124,      "time": 137.28125 },
        { "compass": 200,   "shadow": 115,      "time": 140.5625  },
        { "compass": 210,   "shadow": 104,      "time": 145.875   },
        { "compass": 220,   "shadow": 93,       "time": 151.15625 },
        { "compass": 230,   "shadow": 83,       "time": 156.28125 },
        { "compass": 240,   "shadow": 74.5,     "time": 161.09375 },
        { "compass": 250,   "shadow": 66,       "time": 165.46875 },
        { "compass": 260,   "shadow": 54,       "time": 170.71875 },
        { "compass": 280,   "shadow": 37.5,     "time": 177.84375 },
        { "compass": 290,   "shadow": 29.5,     "time": 181.53125 },
        { "compass": 300,   "shadow": 18,       "time": 186.375   },
        { "compass": 310,   "shadow": 10.5,     "time": 189.125   },
        { "compass": 320,   "shadow": 2,        "time": 192.625   },
        { "compass": 330,   "shadow": 354.5,    "time": 195.125   },
        { "compass": 340,   "shadow": 342.5,    "time": 198.96875 },
        { "compass": 350,   "shadow": 333.5,    "time": 202.78125 },
        { "compass": 0,     "shadow": 323,      "time": 206.5     },
        { "compass": 10,    "shadow": 312,      "time": 211.125   },
        { "compass": 20,    "shadow": 302.5,    "time": 215.28125 },
        { "compass": 30,    "shadow": 294,      "time": 218.25    },
    ]
}

class SunSwingTestsBase(object):
    fixtures = ['test_user_data']

    def test_swing_and_readings(self):
        swing = self.swing

        # Test that the variation has been correctly filled in
        self.assertEqual(swing.variation, 6.02)

        self.assertEqual(swing.reading_set.all().count(), len(test_data["readings"]))

        south = swing.reading_set.filter(compass_reading=180)[0]

        # test against known good values
        self.assertEqual(south.utc_datetime, datetime(2015, 10, 12, 10, 15, 15, 500000, tzinfo=pytz.utc))
        self.assertAlmostEqual(south.solar_azimuth, 175.63660700)
        self.assertAlmostEqual(south.angle_to_sun, 335)
        self.assertAlmostEqual(south.true_bearing, 200.63660700)
        self.assertAlmostEqual(south.magnetic_bearing, 194.616607)
        self.assertAlmostEqual(south.deviation, -14.616607)

        # for r in swing.reading_set.all():
        #     print r.true_bearing, "," , r.deviation


class ModelTests(SunSwingTestsBase, TestCase):
    def setUp(self):
        swing = SunSwing.objects.create(
            user=User.objects.get(pk=1),
            vessel="Test",
            note="test",
            video_start_time=datetime.fromtimestamp(test_data["compass_video_start_time"], pytz.utc),
            latitude=test_data["latitude"],
            longitude=test_data["longitude"],
            pelorus_correction=test_data["pelorus_correction"],
        )

        for reading in test_data['readings']:
            swing.reading_set.create(
                video_time=reading["time"],
                compass_reading=reading["compass"],
                shadow_reading=reading["shadow"],
            )

        self.swing = swing


class JsonPostTests(SunSwingTestsBase, TestCase):

    def setUp(self):
        c = Client()

        self.assertTrue(c.login(username="bob@test.com", password="secret"))

        self.response = c.post('/swing/sun_json/', content_type='application/json', data=json.dumps(test_data) )
        self.assertEqual(self.response.status_code, 200)

        self.swing = SunSwing.objects.all()[0]








