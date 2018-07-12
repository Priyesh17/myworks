'''
Created on 17-Jun-2018

@author: priyesh
'''
import gnupg
import json

class gpgDecrypt(object):
    def __init__(self, data):
        self.data = data
        self.message = None
        self.passphrase = None
        self.errors = []
        
    def _validate_message(self):
        if self.data.get("Message", None) is None:
            self.errors.append({"error2": "Message is missing"})
        else:
            self.message = self.data.get("Message")
            if self.message.strip() == "":
                self.errors.append({"error2": "Message is missing."})
                
            if not self.message.startswith("-----BEGIN PGP MESSAGE-----"):
                self.errors.append({"error2": "Encrypted message has bad format for a GPG encryption. -----BEGIN PGP MESSAGE----- is missing."})
    
            if not self.message.endswith("-----END PGP MESSAGE-----"):
                self.errors.append({"error2": "Encrypted message has bad format for a GPG encryption. It should end with -----END PGP MESSAGE-----."})
                
            if "Version" not in self.message:
                self.errors.append({"error2": "Encrypted message has bad format for a GPG encryption. It should contain version information with proper casing."})
                
    def _validate_passphrase(self):
        if self.data.get("Passphrase", None) is None:
            self.errors.append({"error1": "Passphrase is missing"})
        else:
            self.passphrase = self.data.get("Passphrase")
            if self.passphrase.strip() == "":
                self.errors.append({"error1": "Passphrase is missing."})
    
    def is_valid(self):
        self._validate_message()
        self._validate_passphrase()
        if len(self.errors) != 0:
            return False
        else:
            return True
    
    
    def decrypt(self):
        gpg = gnupg.GPG()
        decrypted_data = gpg.decrypt(message=self.message, passphrase=self.passphrase)    
        return decrypted_data
    