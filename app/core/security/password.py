#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/16 23:39
@Author   : wiesZheng
@Software : PyCharm
"""
import hashlib
import bcrypt
import base64

from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from loguru import logger
from config import AppConfig

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2YZVJzRrn1kyJHZS+7O5/oteO
YOkbiNk3ndRLQscgdDf3k+RaRomzvHro5w2h6T9A5rd45vM0kyKcBezE/Za1pOKq
meovah1zxxoofQJ8k91ybVFXYJx99k9ravCMr+wKuCpuuwPe8he10iBZ465vVZ6g
5Nbg4gM2PcV7OMVLaQIDAQAB
-----END PUBLIC KEY-----"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQC2YZVJzRrn1kyJHZS+7O5/oteOYOkbiNk3ndRLQscgdDf3k+Ra
RomzvHro5w2h6T9A5rd45vM0kyKcBezE/Za1pOKqmeovah1zxxoofQJ8k91ybVFX
YJx99k9ravCMr+wKuCpuuwPe8he10iBZ465vVZ6g5Nbg4gM2PcV7OMVLaQIDAQAB
AoGABgNhutMngjyVcta4omgOhS3jLcjJ8sbrA4Y220w5DhvALc+7XBMejpWmAfMT
8YekAWGsq7CwqjDON7Gge3kRdz7PDwjaPBwkOebD1aYNWDM0TfQiINVxCkZpPoKg
KTpIELQUoD6KMWw8NUwcasqHcz1HCC6DnRYpG3XJXYhdJDECQQDCvQ/tkHOi92He
RioTHSiJd/5TvgPgBH7dqsldT6mwS67EbrWFEiSSRbzref6wv+r8sXb9d436Ltno
4lngQWZZAkEA78FX7EzS/TAV/PDfWh/ncozY9tFqfPNk4w96LVb5wy8oc9M419K9
yLWeSfiBcXK2l+S2XYk49OhuznklZWiLkQJAL1c+1AXV1rxE8oAkIlloTWL6VOlQ
j9kH7mNiaGjBW7ZKWj5/qkXq1hRWBPi3TciaG6wYvS2fOj7BgrfkGXxMoQJBAIbT
zNUHEvPtMcBP2Nr+7BJgILcUZ3UjDw4dqxCKQ+S+xVn1Y5cDXVTcxcpFZM3eu85J
gUCypYQcngug1yXjF/ECQQCBZZAZ+GhpzqwerwqyfNHvrahSrfp14l6STktaCjKy
IR4n5TomCkHRaeXPgn1YVIhz5/LaVZJuKK3eiN2Wbdwy
-----END RSA PRIVATE KEY-----"""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    correct_password: bool = bcrypt.checkpw(
        plain_password.encode(), hashed_password.encode()
    )
    return correct_password


def get_password_hash(password: str) -> str:
    hashed_password: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password


async def hash_psw(password: str) -> str:
    # 每次加密都进行一次salt生成, 让每次加密的hash都不同
    salt_ = bcrypt.gensalt(rounds=AppConfig.BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode(), salt_)
    return hashed.decode()


async def verify_psw(plain_psw: str, hashed_psw: str) -> bool:
    try:
        result = bcrypt.checkpw(plain_psw.encode(), hashed_psw.encode())
        return result
    except Exception as e:
        logger.error(f"Error occurred during password verification: {str(e)}")
        return False


def add_salt(password: str) -> str:
    m = hashlib.md5()
    bt = f"{password}{AppConfig.SALT}".encode("utf-8")
    m.update(bt)
    return m.hexdigest()


def generate_secret_key() -> tuple[str, str]:
    """
    公钥私钥生成
    :return:
    """
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
    private_key = rsa.exportKey()
    public_key = rsa.publickey().exportKey()
    return private_key.decode("utf8"), public_key.decode("utf8")


async def encrypt_rsa_password(password: str) -> bytes | str:
    """
    密码加密
    :param password:
    :return:
    """
    try:
        public_key = RSA.import_key(PUBLIC_KEY)
        cipher = PKCS1_v1_5.new(public_key)
        text = cipher.encrypt(password.encode("utf8"))
        return base64.b64encode(text)
    except Exception as err:
        print(err)
        return password


async def decrypt_rsa_password(password) -> str:
    """
    密码解密
    :param password:
    :return:
    """
    try:
        private_key = RSA.import_key(PRIVATE_KEY)
        cipher = PKCS1_v1_5.new(private_key)
        text = cipher.decrypt(base64.b64decode(password), b"")
        return text.decode()
    except Exception as err:
        print(err)
        return password
