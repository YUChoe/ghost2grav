# Ghost(1.0 JSON) to GRAV  
* Grav is a modern open source flat-file CMS [https://getgrav.org/](https://getgrav.org/)
* Ghost is a professional publishing platform [https://ghost.org/](https://ghost.org/)

### Features
* **Ghost2Grav** is a simple migration tool from Ghost to Grav.
* wrapping Hyperlink to [oEmbed format](http://www.oembed.com/) for [grav-plugin-mediaembed](https://github.com/sommerregen/grav-plugin-mediaembed)

### Requirements
* python 3.4+
* jinja2 

## Installing and Running

```
$ git clone https://github.com/YUChoe/ghost2grav.git
$ cd ghost2grav
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ python ghost2grav.py ~/ghost.json
```

### Limitation
* It migrates only posts. 
* Grav doesn't support UTF8 slug. 
* It does't migrate links and images automatically. 

### Tip - Wordpress to Grav Migration
1. Wordpress to Ghost [https://github.com/jonhoo/wp2ghost](https://github.com/jonhoo/wp2ghost)
2. Ghost to Grav 

## TODO
* test 
* pypi

## License
Ghost2Grav is MIT-licensed, as found in the LICENSE.txt file.
