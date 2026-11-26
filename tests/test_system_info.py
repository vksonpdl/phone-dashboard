import unittest
from app import create_app
from modules.system_info import get_phone_ip, get_device

class TestSystemInfoPhoneIP(unittest.TestCase):
    def setUp(self):
        self.app = create_app() if hasattr(app := __import__('app'), 'create_app') else None
        # Alternatively test via Flask test client or direct function calls
        app_module = __import__('app', fromlist=['app'])
        self.client = app_module.app.test_client()

    def test_get_phone_ip_structure(self):
        ip_info = get_phone_ip()
        self.assertIn("ipv4", ip_info)
        self.assertIn("ipv6", ip_info)
        self.assertIsInstance(ip_info["ipv4"], str)
        self.assertIsInstance(ip_info["ipv6"], str)

    def test_get_device_includes_phone_ip(self):
        device = get_device()
        self.assertIn("phone_ip", device)
        self.assertIn("ipv4", device["phone_ip"])
        self.assertIn("ipv6", device["phone_ip"])

    def test_system_overview_endpoint(self):
        response = self.client.get("/api/system")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("device", data)
        self.assertIn("phone_ip", data["device"])
        self.assertIn("ipv4", data["device"]["phone_ip"])
        self.assertIn("ipv6", data["device"]["phone_ip"])

if __name__ == "__main__":
    unittest.main()
