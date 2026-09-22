"""Tests for user_agent_parser.core."""

import unittest

from user_agent_parser import UserAgent, parse


class TestParse(unittest.TestCase):
    def test_chrome_windows_desktop(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        result = parse(ua)
        self.assertEqual(result.browser, "Chrome")
        self.assertEqual(result.browser_version, "120.0.0.0")
        self.assertEqual(result.engine, "WebKit")
        self.assertEqual(result.engine_version, "537.36")
        self.assertEqual(result.operating_system, "Windows 10/11")
        self.assertEqual(result.device_type, "desktop")

    def test_edge_priority_over_chrome(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.61"
        result = parse(ua)
        self.assertEqual(result.browser, "Edge")
        self.assertEqual(result.browser_version, "120.0.2210.61")

    def test_safari_macos(self):
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
        result = parse(ua)
        self.assertEqual(result.browser, "Safari")
        self.assertEqual(result.browser_version, "17.2")
        self.assertEqual(result.engine, "WebKit")
        self.assertEqual(result.engine_version, "605.1.15")
        self.assertEqual(result.operating_system, "macOS")
        self.assertEqual(result.device_type, "desktop")

    def test_firefox_linux(self):
        ua = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
        result = parse(ua)
        self.assertEqual(result.browser, "Firefox")
        self.assertEqual(result.browser_version, "120.0")
        self.assertEqual(result.engine, "Gecko")
        self.assertEqual(result.engine_version, "20100101")
        self.assertEqual(result.operating_system, "Linux")
        self.assertEqual(result.device_type, "desktop")

    def test_android_mobile_chrome(self):
        ua = "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        result = parse(ua)
        self.assertEqual(result.browser, "Chrome")
        self.assertEqual(result.operating_system, "Android")
        self.assertEqual(result.device_type, "mobile")

    def test_iphone_safari(self):
        ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
        result = parse(ua)
        self.assertEqual(result.browser, "Safari")
        self.assertEqual(result.operating_system, "iOS")
        self.assertEqual(result.device_type, "mobile")

    def test_ipad_tablet(self):
        ua = "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
        result = parse(ua)
        self.assertEqual(result.operating_system, "iPadOS")
        self.assertEqual(result.device_type, "tablet")

    def test_bot_detection(self):
        ua = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        result = parse(ua)
        self.assertEqual(result.device_type, "bot")
        self.assertEqual(result.browser, None)

    def test_unknown_user_agent(self):
        ua = "curl/8.1.2"
        result = parse(ua)
        self.assertEqual(result.browser, None)
        self.assertEqual(result.browser_version, None)
        self.assertEqual(result.engine, None)
        self.assertEqual(result.engine_version, None)
        self.assertEqual(result.operating_system, None)
        self.assertEqual(result.device_type, None)

    def test_empty_string(self):
        result = parse("")
        self.assertIsInstance(result, UserAgent)
        self.assertIsNone(result.browser)
        self.assertIsNone(result.device_type)

    def test_type_error_on_non_string(self):
        with self.assertRaises(TypeError):
            parse(123)  # type: ignore[arg-type]

    def test_ios_safari_without_engine(self):
        ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Version/16.0 Mobile/15E148"
        result = parse(ua)
        self.assertEqual(result.browser, "Safari")
        self.assertEqual(result.operating_system, "iOS")
        self.assertEqual(result.device_type, "mobile")


if __name__ == "__main__":
    unittest.main()
