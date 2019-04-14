# -*- coding: utf-8 -*-

"""
hdu_api._internal_utils
-----------------------


"""
import sys

from hdu_api import _pyDes

_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)


def encrypt(data, first_key, second_key, third_key):
    bts_data = extend_to_16bits(data)
    bts_first_key = extend_to_16bits(first_key)
    bts_second_key = extend_to_16bits(second_key)
    bts_third_key = extend_to_16bits(third_key)
    i = 0
    bts_result = []
    while i < len(bts_data):
        # 将data分成每64位一段，分段加密
        bts_temp = bts_data[i:i + 8]
        j, k, z = 0, 0, 0
        while j < len(bts_first_key):
            # 分别取出 first_key 的64位作为密钥
            des_k = _pyDes.des(bts_first_key[j: j + 8], _pyDes.ECB)
            bts_temp = list(des_k.encrypt(bts_temp))
            j += 8
        while k < len(bts_second_key):
            des_k = _pyDes.des(bts_second_key[k:k + 8], _pyDes.ECB)
            bts_temp = list(des_k.encrypt(bts_temp))
            k += 8
        while z < len(bts_third_key):
            des_k = _pyDes.des(bts_third_key[z:z + 8], _pyDes.ECB)
            bts_temp = list(des_k.encrypt(bts_temp))
            z += 8

        bts_result.extend(bts_temp)
        i += 8
    str_result = ''
    for each in bts_result:
        if is_py2:
            each = ord(each)
        # 分别加密data的各段，串联成字符串
        str_result += '%02X' % each
    return str_result


def extend_to_16bits(data):
    """
    将字符串的每个字符前插入 0，变成16位，并在后面补0，使其长度是64位整数倍
    :param data:
    :return:
    """
    bts = data.encode()
    c = 0
    if is_py2:
        c = chr(c)
    filled_bts = []
    for each in bts:
        # 每个字符前插入 0
        filled_bts.extend([c, each])
    # 长度扩展到8的倍数，若不是8的倍数，后面添加0，便于DES加密时分组
    while len(filled_bts) % 8 != 0:
        filled_bts.append(c)
    return filled_bts
