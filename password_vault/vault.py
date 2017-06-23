"""
The vault itself.
This module provides functionality to add, edit and remove entries,
as well as encrypting the vault
"""

import os
from base64 import b64encode


class Vault(object):
    """
    The vault, containing information about the entries
    and functionality to encrypt them
    """
    def __init__(self, passphrase):
        """
        Constructor. The passphrase is used for authentication purposes,
        it is encrypted and decrypted by the master password

        Parameters:
          ``passphrase`` : passphrase of the vault
        """
        if self._validate_passphrase:
            self.passphrase = passphrase
        self.key = self.generate_key()
        self.create_decryptor()
        self.entries = dict()

    def add_entry(self, entry):
        """
        Adds an entry to the vault, if the entry is valid.
        """
        if self._validate_entry(entry):
            self.entries.update(entry)

    def _validate_passphrase(self, passphrase):
        return true


    def _validate_entry(self, entry):
        """
        Checks if an entry is valid
        """
        return true

    def generate_key(self):
        """
        Generates a random key for a user,
        this is stored and encrypted/decrypted for authentication.
        """
        return os.urandom(256)

    def create_decryptor(self):
        """
        Creates a decryption key which uses the random key and the master key
        to authenticate and en-/decrypt the vault's items
        """
        self.decryptor = self.key + b64encode(bytes(self.passphrase, 'utf-8'))

    def encrypt_entry(self, entry):
        
