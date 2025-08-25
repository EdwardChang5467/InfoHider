import re

# 加密字典
encode_dict = {
    '0': '\u200b',  
    '1': '\u200c',
    ' ': '\u200d',
}

# 解密字典
decode_dict = {
    '\u200b': '0',  
    '\u200c': '1',
    '\u200d': ' ',
}

#求char中二进制值作为ASCII码对应的字符
def bin_2_str(char):
    # 每次接受一个字符
    return ''.join([chr(i) for i in [int(b, 2) for b in char.split(' ')]])


def text_to_zero(text):
    
    #求字符串ASCII码的二进制值，并把'0b'去掉,每个二进制值中间用空格分割
    text = ' '.join([bin(ord(c)).replace('0b', '') for c in text])
    text = ''.join([encode_dict[k] for k in text])
    return text


def zero_to_text(zero):

    #将零宽字符串替换为二进制串
    zero = re.sub(encode_dict['0'], "0", zero)
    zero = re.sub(encode_dict['1'], "1", zero)
    zero = re.sub(encode_dict[' '], " ", zero)

    # 匹配加密文本，二进制串+空格
    encrypted_text = re.findall(r'[0,1,\s]+', zero)
    raw = dict()
    for k in encrypted_text:
        k = k.strip() 
        if k:
            raw[k] = bin_2_str(k)
    for k in raw:
        zero = re.sub(k, raw[k], zero)

    return zero