# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/16 10:40
@Author   : wiesZheng
@Software : PyCharm
"""
import jwt
import pytz
from typing import Dict, Any, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidSignatureError, DecodeError, ExpiredSignatureError

from app.exceptions.exception import AuthException
from config import JwtConfig
import base64

from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA

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

# 设置时区
ChinaTimeZone = pytz.timezone("Asia/Shanghai")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/system/user/login')


async def create_access_token(sub: str) -> str:
    """
    根据登录信息创建当前用户token

    :param sub: 用户信息
    :return: token
    """
    current_time = datetime.now(ChinaTimeZone)
    new_data = {
        "jti": current_time.strftime("%Y%m%d%H%M%f"),
        "iss": JwtConfig.JWT_ISS,
        "iat": current_time,
        "exp": current_time + timedelta(minutes=JwtConfig.JWT_EXPIRE_MINUTES),
        "sub": sub}

    # 生成并返回jwt
    return jwt.encode(new_data,
                      key=JwtConfig.JWT_SECRET_KEY,
                      algorithm=JwtConfig.JWT_ALGORITHM)


async def decode_jwt_token(token: str) -> int:
    if not token:
        raise AuthException(message="用户信息身份认证失败, 请检查")
    try:
        payload = jwt.decode(token, JwtConfig.JWT_SECRET_KEY, algorithms=[JwtConfig.JWT_ALGORITHM])
        user_id = int(payload.get('sub'))
        if not user_id:
            raise AuthException(message='Token 无效')
    except (InvalidSignatureError, DecodeError):
        raise AuthException(message="无效认证，请重新登录")

    except ExpiredSignatureError:
        raise AuthException(message="过期")
    return user_id


# async def get_current_user(db: AsyncSession, data: dict) -> User:
#     """
#     Get the current user through token
#
#     :param db:
#     :param data:
#     :return:
#     """
#     user_id = data.get('sub')
#     from backend.app.admin.crud.crud_user import user_dao
#
#     user = await user_dao.get_with_relation(db, user_id=user_id)
#     if not user:
#         raise TokenError(msg='Token 无效')
#     if not user.status:
#         raise AuthorizationError(msg='用户已被锁定，请联系系统管理员')
#     if user.dept_id:
#         if not user.dept.status:
#             raise AuthorizationError(msg='用户所属部门已锁定')
#         if user.dept.del_flag:
#             raise AuthorizationError(msg='用户所属部门已删除')
#     if user.roles:
#         role_status = [role.status for role in user.roles]
#         if all(status == 0 for status in role_status):
#             raise AuthorizationError(msg='用户所属角色已锁定')
#     return user


def generate_secret_key() -> tuple[str, str]:
    """
    公钥私钥生成
    :return:
    """
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
    private_key = rsa.exportKey()
    public_key = rsa.publickey().exportKey()
    return private_key.decode('utf8'), public_key.decode('utf8')


async def encrypt_rsa_password(password: str) -> bytes | str:
    """
    密码加密
    :param password:
    :return:
    """
    try:
        public_key = RSA.import_key(PUBLIC_KEY)
        cipher = PKCS1_v1_5.new(public_key)
        text = cipher.encrypt(password.encode('utf8'))
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
        text = cipher.decrypt(base64.b64decode(password), b'')
        return text.decode()
    except Exception as err:
        print(err)
        return password
