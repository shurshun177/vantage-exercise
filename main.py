import itertools
from aiohttp import web
import string
import re


def xor_encrypt(text, key):
    text_list = (i for i in text)
    pares = zip(text_list, itertools.cycle(key))
    result = (ord(i) ^ ord(j) for i, j in pares)
    return list(result)


def xor_decrypt(encrypted_text, key):
    pares = zip(encrypted_text, itertools.cycle(key))
    result = ''.join((chr(i ^ ord(j)) for i, j in pares))
    return result


def guess_key(encrypted_text, key_size):
    pattern = r'[a-zA-Z0-9-_"\'\?\!\s]+'
    key_letters = string.ascii_lowercase
    text_list = [int(i) for i in encrypted_text.split(',')]
    keys = (''.join(i) for i in itertools.permutations(key_letters, key_size))
    result = [[i, xor_decrypt(text_list, i)] for i in keys if xor_decrypt(text_list, i)]
    return result


async def post_handler(request):
    cont = await request.json()
    text = cont.get('text')
    size = cont.get('size')
    data = guess_key(text, size)
    return web.json_response(data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = web.Application()
    app.router.add_post(path='/bruteforce/', handler=post_handler)
    web.run_app(app, port=5000)
