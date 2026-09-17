from django.test import TestCase
from django.test import Client
from wake.models import Server
import unittest.mock as mock

class ServerTests(TestCase):
    def setUp(self):
        self.c = Client()

    def testAdd(self):
        response = self.c.post("/add/", {"name": "test-1", "ip_address": "0.0.0.0", "mac_address": "0:0:0:0:0:0"})
        self.assertEqual(response.status_code, 200)

        item = Server.objects.get(name="test-1")
        self.assertEqual(item.ip_address, "0.0.0.0")
        self.assertEqual(item.mac_address, "0:0:0:0:0:0")
        self.assertEqual(item.is_on, True)

    def testDelete(self):
        Server.objects.create(name="test-1", ip_address="0.0.0.0", mac_address="0:0:0:0:0:0")
        response = self.c.post("/delete/", {"name": "test-1"})
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Server.DoesNotExist):
            Server.objects.get(name="test-1")

    def testPowerOff(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.connect.return_value = None
            mock_socket.return_value.send.return_value = None
            Server.objects.create(name="test-1", ip_address="0.0.0.0", mac_address="0:0:0:0:0:0", is_on=True)

            response = self.c.post("/power/", {"name": "test-1"})
            self.assertEqual(response.status_code, 200)
            item = Server.objects.get(name="test-1")
            self.assertEqual(item.is_on, None)

    def testPowerOn(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.connect.return_value = None
            mock_socket.return_value.send.return_value = None
            Server.objects.create(name="test-1", ip_address="0.0.0.0", mac_address="0:0:0:0:0:0", is_on=False)

            response = self.c.post("/power/", {"name": "test-1"})
            self.assertEqual(response.status_code, 200)
            item = Server.objects.get(name="test-1")
            self.assertEqual(item.is_on, None)

    def testReboot(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.connect.return_value = None
            mock_socket.return_value.send.return_value = None
            Server.objects.create(name="test-1", ip_address="0.0.0.0", mac_address="0:0:0:0:0:0", is_on=True)

            response = self.c.post("/power/", {"name": "test-1"})
            self.assertEqual(response.status_code, 200)
            item = Server.objects.get(name="test-1")
            self.assertEqual(item.is_on, None)

    def testPowerFailConnect(self):
        Server.objects.create(name="test-1", ip_address="0.0.0.0", mac_address="0:0:0:0:0:0", is_on=True)

        response = self.c.post("/power/", {"name": "test-1"})
        self.assertEqual(response.status_code, 502)




    




