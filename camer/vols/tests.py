from django.template import Origin
from django.test import TestCase,Client
from django.db.models import Max

from .models import Vols, Airport, Passenger

# Create your tests here.
class VolsTestCase(TestCase):

    def setUp(self):

        #create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        #Create a flights
        Vols.objects.create(origin=a1, destination=a2, duration=100)
        Vols.objects.create(origin=a1, destination=a1, duration=200)
        Vols.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_vols(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Vols.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_vols())
    
    def test_invalid_vols(self):
        a1 = Airport.objects.get(code="AAA")
        f = Vols.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_vols())

    def test_invalid_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Vols.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_vols())
    
    def test_index(self):
        c = Client()
        response = c.get("/vols/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["vols"].count(), 3)

    def test_valid_vol_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Vols.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/vols/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_vol_page(self):
        max_id = Vols.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/vol/{max_id + 1}")
        self.assertEqual(response.status_code, 404)
    
    def test_vol_page_passengers(self):
        f = Vols.objects.get(pk=1)
        p = Passenger.objects.create(firstname="Alice", lastname="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/vols/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_vol_page_non_passeneger(self):
        f = Vols.objects.get(pk=1)
        p = Passenger.objects.create(firstname="Alice", lastname="Adams")
       

        c = Client()
        response = c.get(f"/vols/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
