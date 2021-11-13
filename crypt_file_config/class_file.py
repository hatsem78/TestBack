import ast
import pickle
import hashlib
import json
import hmac
import binascii
from pprint import pprint
import os

from crypt_file_config.class_crypt import Crypt


class FileConfig(Crypt):

    __dict_file = {}
    __secret_key = "!QAZWSX$%&/(UHJNBVC[]"
    __name_file = 'file_dat'

    def load_data(self, name_file=None):
       self.__load_file()

    def __load_file(self):
        if os.path.exists("file_dat"):

            try:
                file = open(self.name_file, 'rb+')
                file.seek(0)
                self.dict_file = json.loads(self.decrypt(pickle.load(file)))

                if self.dict_file['secret_key'] != self.get_key_secret():
                    print('File is not correct, it can be malicious')

            except EOFError as error:
                print(error)
                self.dict_file = {}
            except TypeError as error:
                print('pedro', error)
                file.close()
        else:
            self.set_file_dat()
        #finally:
        #    file.close()
        #    del file

    @property
    def name_file(self):
        return self.__name_file

    @name_file.setter
    def name_file(self, value=None):
        if not isinstance(value, (str,)):
            raise TypeError("file should is str")
        self.__name_file = value

    @property
    def dict_file(self):
        return self.__dict_file

    @dict_file.setter
    def dict_file(self, value=None):
        if not isinstance(value, (dict,)):
            raise TypeError("file should is list")
        self.__dict_file = value

    @property
    def file_name_dat(self):
        return self.__file_name_dat

    @property
    def secret_key(self):
        return self.__secret_key

    def get_key_secret(self):
        byte_key = binascii.unhexlify("E49756B4C8FAB4E48222A3E7F3B97CC3")
        message = self.secret_key.encode()
        return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()

    def set_info_file(self, key=None, value=None):
        self.dict_file[key] = value
        self.__save()

    def get_key_value(self, key):
        self.load_data()
        return self.dict_file[key]

    def set_file_dat(self, name_file=None):
        try:
            file = open(self.name_file, "wb+")
            file.seek(0)
            pickle.dump(self.encrypt(json.dumps({"secret_key": self.get_key_secret()})), file)
            file.close()
        except IOError as error:
            print(error)
        except TypeError as error:
            print(error)
            file.close()
        finally:
            file.close()
            del file

    def print_info(self):
        self.load_data()
        pprint(self.dict_file)

    def view_data_file(self):
        self.load_data()
        try:
            data_file = open(self.name_file + ".txt", "w+")
            data_file.write(json.dumps(self.dict_file))
            data_file.close()
        except IOError as error:
            print(error)
            data_file.close()

    def save_data_file(self):
        try:
            data_file = open(self.name_file + ".txt", "r")
            contents = data_file.read()
            data_file.close()
            self.dict_file = ast.literal_eval(contents)
            self.__save()
            os.remove(self.name_file + ".txt")
        except TypeError as error:
            print(error)

    def __save(self):
        try:
            file = open(self.name_file, "wb+")
            self.dict_file["secret_key"] = self.get_key_secret()
            pickle.dump(self.encrypt(json.dumps(self.dict_file)), file)
            file.close()
        except IOError as error:
            print(error)
            file.close()
            del file
        finally:
            file.close()
            del file

    def __exit__(self):
        self.__save()  # guardado automático

