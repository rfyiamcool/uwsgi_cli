# uwsgi_cli

### http mode
uwsgi_cli http 127.0.0.1:5000 /blog

### unix socket mode
uwsgi_cli unix /tmp/xiaorui.sock /

### tcp socket mode
uwsgi_cli tcp 127.0.0.1:5000 /mp/article
