# coding:utf-8
import hashlib
from configs import PASSWORD_SALT

class HashHelper(object):

    @classmethod
    def hash_password(cls,raw_pwd,salt=PASSWORD_SALT):
        hash_pwd=hashlib.sha1(salt+raw_pwd).hexdigest()
        return hash_pwd

    @classmethod
    def check_password(cls,raw_pwd,hash_pwd):
        if not raw_pwd:
            return False
        return cls.hash_password(raw_pwd)==hash_pwd