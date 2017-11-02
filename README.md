# uwsgi_cli

match uwsgi protocol, support http get、post requests uwsgi server.

`to do list:`

* add debug mode, print uwsgi body

## install
```
pip install uwsgi_cli
```

## help
```
uwsgi_cli -h
```

if not found uwsgi_cli bin, please set PATH . ( /usr/local/bin/ )


### http mode
```
uwsgi_cli http 127.0.0.1:5000 /blog
```

### unix socket mode
```
uwsgi_cli unix /tmp/xiaorui.sock /
```

### tcp socket mode
```
uwsgi_cli tcp 127.0.0.1:5000 /mp/article
```
### post
```
uwsgi_cli tcp 127.0.0.1:5000 /cool/fetch "url=xiaorui.cc&name=fengyun"
```
