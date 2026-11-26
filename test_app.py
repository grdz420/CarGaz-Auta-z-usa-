import unittest,json
from unittest.mock import patch
from urllib.parse import urlencode
from app import application
class Tests(unittest.TestCase):
 def request(self,path,query=''):
  status=[]; body=b''.join(application({'REQUEST_METHOD':'GET','PATH_INFO':path,'QUERY_STRING':query},lambda s,h:status.append(s)));return status[0],body
 def test_home(self):
  status,body=self.request('/');self.assertEqual(status,'200 OK');self.assertIn(b'CAR GAZ',body)
 def test_invalid(self):self.assertEqual(self.request('/api/vehicle','url=https://evil.test/lot/123')[0],'400 Bad Request')
 def test_lookup(self):
  with patch('app.lookup',return_value={'location':'Miami (FL)'}):
   status,body=self.request('/api/vehicle',urlencode({'url':'https://bid.cars/pl/lot/1-123/foo'}));self.assertEqual(status,'200 OK');self.assertEqual(json.loads(body)['location'],'Miami (FL)')
 def test_health(self):self.assertEqual(self.request('/health')[0],'200 OK')
if __name__=='__main__':unittest.main()
