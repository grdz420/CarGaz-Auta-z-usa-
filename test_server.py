import unittest
from server import extract,allowed
class Tests(unittest.TestCase):
 def test_bidcars(self):
  x=extract('<title>2019 Acura TLX</title><ul><li>Location: <b>Philadelphia (PA)</b></li><li>Shipping from: <b>Newark (NJ)</b></li></ul>');self.assertEqual(x['location'],'Philadelphia (PA)');self.assertEqual(x['port'],'Newark (NJ)')
 def test_pickup_priority(self):
  self.assertEqual(extract('<p>Sale Location: TX - HOUSTON</p><p>Pickup Location: FL - MIAMI</p>')['location'],'MIAMI (FL)')
 def test_no_guess(self):self.assertIsNone(extract('<p>Sale Document: Cert of salvage (PA)</p>'))
 def test_allowed(self):self.assertTrue(allowed('https://bid.cars/pl/lot/1-123/foo'));self.assertFalse(allowed('https://copart.com.evil.test/lot/123'));self.assertFalse(allowed('https://copart.com:444/lot/123'));self.assertFalse(allowed('https://copart.com/other'))
if __name__=='__main__':unittest.main()
