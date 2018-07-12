# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
import json

# Create your tests here.

class gpgDecryptTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = None
        
    def tearDown(self):
        TestCase.tearDown(self)

    def test_valid_gpg_encrypted_message(self):
        '''
        Proper passphrase and proper message. Should decrypt and status should be 200.
        '''
        passphrase = "topsecret"
        message = '''-----BEGIN PGP MESSAGE-----
Version: GnuPG v2
jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
-----END PGP MESSAGE-----'''
        
        data = {"Passphrase": passphrase, "Message": message}
        
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(data['DecryptedMessage'], "Nice work!\n")
        
    def test_valid_gpg_encrypted_message_another_passphrase(self):
        '''
        Proper passphrase and proper message. Should decrypt and status should be 200.
        '''
        passphrase = "my passphrase"
        message = '''-----BEGIN PGP MESSAGE-----
Version: GnuPG v1

hQEMA8ME3tuSWYSuAQf/a1HAJkI6xACRe4NsZFqp5PFHX0SRlFBylJJyykUEMiw6
eEJp+YsSwAbQm5NmSgXkKUT0JnABhMqgvZag8aj3qvzzVZlPC0NFLFgDBzSyoAxN
1vqba/Tj8O3eKAKxKsD44HwO5JtWNwy2jSnQNcw/s7rx8HAWpq4nfpe+dhxu8exI
ivtd0hzte4J8HJIrrJve6mQWa/LxIV3cICAN+ZpqD+zUdRWtoCqcYOfv2qnuc3tZ
H9iqyLkUHCrqffVKUIOB72lj0j0CRC12CLsHntcBQaZWreb9xlZWGq2Zq4eOXrbD
IB28hkQXUgdnX+ZUCUUP4g4SdZoL175Ejovv+y4fL9JiAYZIOoUHazPWKcpSor+p
gL9xe9iXePLcnbl0MmwABwnUj5z2ZcrcO0dldpuGLx0f+O0LFEa/MFpOWlqvHjXD
T2N6Z1Kp8dQ/9IvAo1cbZZCfAyvYcEBpFYQED0xyvYH83Kc=
=KeLG
-----END PGP MESSAGE-----'''
        
        data = {"Passphrase": passphrase, "Message": message}
        
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(data['DecryptedMessage'], "Who are you? How did you get in my house?")
        
    def test_invalid_gpg_key_for_message(self):
        '''
        Invalid passphrase and proper message. Should decrypt to Empty string and status should be 200.
        '''
        passphrase = "my passphrase"
        message = '''-----BEGIN PGP MESSAGE-----
Version: GnuPG v2
jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
-----END PGP MESSAGE-----'''
        
        data = {"Passphrase": passphrase, "Message": message}
        
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(data['DecryptedMessage'], "")
        
    def test_invalid_parameter_missing_passphrase_key(self):
        '''
        Json data does not contain passphrase. Should get an error message with 400 Bad request.
        '''
        message = '''-----BEGIN PGP MESSAGE-----
Version: GnuPG v2
jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
-----END PGP MESSAGE-----'''
        
        data = {"Message": message}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
        
    def test_invalid_parameter_empty_passphrase_value(self):
        '''
        Json data does not contain passphrase value. Should get an error message with 400 Bad request.
        '''
        passphrase = ""
        message = '''-----BEGIN PGP MESSAGE-----
Version: GnuPG v2
jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
-----END PGP MESSAGE-----'''
        
        data = {"Message": message, "Passphrase": passphrase}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
    
    def test_invalid_parameter_empty_passphrase_value_multiple_spaces(self):
        '''
        Json data does not contain passphrase value. Should get an error message with 400 Bad request.
        '''
        passphrase = "             "
        message = '''-----BEGIN PGP MESSAGE-----
Version: GnuPG v2
jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
-----END PGP MESSAGE-----'''
        
        data = {"Message": message, "Passphrase": passphrase}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
        
    def test_invalid_parameter_missing_message_key(self):
        '''
        Json data does not contain message key. Should get an error message with 400 Bad request.
        '''
        passphrase = "my passphrase"
        
        data = {"Passphrase": passphrase}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
        
    def test_invalid_parameter_empty_message_value(self):
        '''
        Json data does not contain message value. Should get an error message with 400 Bad request.
        '''
        passphrase = "my passphrase"
        message = ""
        
        data = {"Message": message, "Passphrase": passphrase}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
    
    def test_invalid_parameter_empty_message_value_multiple_spaces(self):
        '''
        Json data contain message value as multiple spaces. Should get an error message with 400 Bad request.
        '''
        passphrase = "my passphrase"
        message = "         "
        
        data = {"Message": message, "Passphrase": passphrase}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
        
    def test_invalid_parameter_empty_message_value_bad_format_missing_begin_part(self):
        '''
        Json data contain invalid format for message. Should get an error message with 400 Bad request.
        '''
        passphrase = "my passphrase"
        message = '''
Version: GnuPG v2
jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
-----END PGP MESSAGE-----'''
        
        data = {"Message": message, "Passphrase": passphrase}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
        
    def test_invalid_parameter_empty_message_value_bad_format_missing_end_part(self):
        '''
        Json data contain invalid format for message where end part is missing. Should get an error message with 400 Bad request.
        '''
        passphrase = "my passphrase"
        message = '''-----BEGIN PGP MESSAGE-----
Version: GnuPG v2
jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
'''
        
        data = {"Message": message, "Passphrase": passphrase}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
        
    def test_invalid_parameter_empty_message_value_bad_format_missing_version(self):
        '''
        Json data contain invalid format for message where end part is missing. Should get an error message with 400 Bad request.
        '''
        passphrase = "my passphrase"
        message = '''-----BEGIN PGP MESSAGE-----

jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
-----END PGP MESSAGE-----'''
        
        data = {"Message": message, "Passphrase": passphrase}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])

    def test_invalid_parameter_empty_message_value_bad_format_version_in_lowercase(self):
        '''
        Json data contain invalid format for message where end part is missing. Should get an error message with 400 Bad request.
        '''
        passphrase = "my passphrase"
        message = '''-----BEGIN PGP MESSAGE-----
version: GnuPG v2
jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
-----END PGP MESSAGE-----'''
        
        data = {"Message": message, "Passphrase": passphrase}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
        
    def test_post_without_data(self):
        '''
        Post without any data.
        '''
        data = {}
        self.response =  self.client.post(reverse('decrypt_message'), data=data)
        data = json.loads(self.response.content)
        print data
        self.assertEqual(self.response.status_code, 400)
        self.assertIsNotNone(data['Error'])
        
    def test_try_get_with_same_url(self):
        '''
        Try Get request.
        '''
        self.response = self.client.get(reverse('decrypt_message'))
        self.assertEqual(self.response.status_code, 405)
        