import unittest
import json
from app_3Context import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_service(self):
        payload = {
            'codigo': 6,
            'aplicacion': 'Manos',
            'servicio': 'Manicura',
            'precio': 2500
        }
        response = self.app.post('/servicios', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Servicio agregado correctamente.')

    def test_modify_service(self):
      payload = {
          'aplicacion': 'Mano',
          'servicio': 'Manicur',
          'precio': 90000
      }
      response = self.app.put('/servicios/6', json=payload)
      data = json.loads(response.data)
      print('Response Status Code:', response.status_code)
      print('Response Data:', data)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(data['message'], 'Servicio modificado correctamente.')


    def test_delete_service(self):
        response = self.app.delete('/servicios/6')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Servicio eliminado correctamente.')

    def test_list_services(self):
        response = self.app.get('/servicios')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
