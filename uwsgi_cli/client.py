#coding:utf-8

import sys
import socket
import argparse

import requests


def sz(x):
    s = hex(x if isinstance(x, int) else len(x))[2:].rjust(4, '0')
    s = bytes.fromhex(s) if sys.version_info[0] == 3 else s.decode('hex')
    return s[::-1]


def pack_uwsgi_vars(var):
    pk = b''
    for k, v in var.items() if hasattr(var, 'items') else var:
        pk += sz(k) + k.encode('utf8') + sz(v) + v.encode('utf8')
    return b'\x00' + sz(pk) + b'\x00' + pk


def parse_addr(addr, default_port=None):
    port = default_port
    if isinstance(addr, str):
        if addr.isdigit():
            addr, port = '', addr
        elif ':' in addr:
            addr, _, port = addr.partition(':')
    elif isinstance(addr, (list, tuple, set)):
        addr, port = addr
    port = int(port) if port else port
    return (addr or '127.0.0.1', port)


def get_host_from_url(url):
    if '//' in url:
        url = url.split('//', 1)[1]
    host, _, url = url.partition('/')
    return (host, '/' + url)


def fetch_data(uri, body):
    if 'http' not in uri:
        uri = 'http://' + uri
    s = requests.Session()
    if body:
        import urlparse
        body_d = dict(urlparse.parse_qsl(urlparse.urlsplit(body).path))
        d = s.post(uri, data=body_d)
    else:
        d = s.get(uri)
    return {
        'code': d.status_code,
        'text': d.text,
        'header': d.headers
    }


def ask_uwsgi(addr_and_port, mode, var, body=''):
    if mode == 'tcp':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(parse_addr(addr_and_port))
    elif mode == 'unix':
        s = socket.socket(socket.AF_UNIX)
        s.connect(addr_and_port)
    s.send(pack_uwsgi_vars(var) + body.encode('utf8'))
    response = []
    while 1:
        data = s.recv(4096)
        if not data:
            break
        response.append(data)
    s.close()
    return b''.join(response).decode('utf8')


def curl(mode, addr_and_port, url, body):
    host, uri = get_host_from_url(url)
    path, _, qs = uri.partition('?')
    if mode == 'http':
        return fetch_data(addr_and_port+uri, body)
    elif mode == 'tcp':
        host = host or parse_addr(addr_and_port)[0]
    else:
        host = addr_and_port
    var = {
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': path,
        'REQUEST_URI': uri,
        'QUERY_STRING': qs,
        'SERVER_NAME': host,
        'HTTP_HOST': host,
    }
    if body:#
        var['REQUEST_METHOD'] = 'POST'
        var['HTTP_CONTENT_LENGTH'] = str(len(body))
        var['HTTP_CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
    return ask_uwsgi(addr_and_port, mode, var, body=body)


def cli(*args):
    parser = argparse.ArgumentParser()

    parser.add_argument('mode', nargs='?', default='tcp',
                        help='Uwsgi mode: 1. http 2. tcp 3. unix')

    parser.add_argument('uwsgi_addr', nargs='?', default='127.0.0.1:5000',
                        help='Uwsgi server  127.0.0.1:5000 ; /tmp/uwsgi.sock')

    parser.add_argument('url', nargs='?', default='/',
                        help='Request URI optionally containing hostname')

    parser.add_argument('body', nargs='?', default='',
                        help='Post body params')

    args = parser.parse_args(args or sys.argv[1:])
    print curl(args.mode, args.uwsgi_addr, args.url, args.body)


if __name__ == '__main__':
    cli()
