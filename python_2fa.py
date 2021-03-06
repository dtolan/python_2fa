"""
https://github.com/tadeck/onetimepass

import onetimepass as otp
my_secret = 'MFRGGZDFMZTWQ2LK'
my_token = 123456 # should be probably from some user's input
isValid = otp.valid_totp(token=my_token, secret=my_secret)
"""
from getpass import getpass
from os import path

import base64
import onetimepass as otp


class Python2FA:
    """
    A simple implementation of the ontimepass python module (pip install onetimepass)
    Allows for the passing of either a secret or filename containing the secret in the 
    """

    def __init__(self, secret=None, filename=None):

        if secret is not None:
            self.secret = secret.encode('utf-8')
        elif filename is not None:
            self.secret = self.__get_secret__(filename)
        if self.secret is not None:
            self.secret = self.__padding__(self.secret)
            self.secret = base64.b32encode(base64.b32decode(self.secret))

    @staticmethod
    def __padding__(data):
        missing_padding = len(data) % 8
        if missing_padding:
            data += b'=' * (8 - missing_padding)
        return data

    @staticmethod
    def __get_secret__(filename):
        if not path.exists(filename):
            print("did not find file")
            return None

        try:
            with open(filename, "r", encoding="utf8") as file:
                line = file.readline()
                return line.encode('utf-8')

        except IOError:
            print("Failed to Open file")
            return None

    def response(self, tries=3):
        """ Need Documentation Here """
        count = 0
        is_valid = False
        while count < tries and is_valid is False:
            count = count + 1
            token = getpass("2FA Authentication: ")
            if len(token) > 1:
                is_valid = otp.valid_totp(token=token, secret=self.secret)
        return is_valid


if __name__ == "__main__":
    authenticator = Python2FA(filename='example/secret')  # secret=secret)
    authenticator.response()
