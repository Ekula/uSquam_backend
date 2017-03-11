# uSquam - procrastinate productively, anywhere and anytime

uSquam (Latin: "anywhere") is a crowdsourcing platform foccussing on full flexibility and 
easy access such that you can use any spare minute to do some good and earn a buck or two 
while your at it. 

That is why we focus on easy interface through chatbots. Currently the following systems
are implemented: 

* Telegram - uSquam-bot

Just download the app and start a chat, it's super simple!

## Installation (for developers)
The backend requires the [flask](http://flask.pocoo.org) framework to be installed which is
a python library. 

```shell
$ pip install flask flask-restful
```

For testing you can either use ```nose``` which outputs just plain text or 
[```green```](https://github.com/CleanCut/green) which 
outputs beautifully colored code. You have to install either of those as well 

```shell
$ pip install nose
$ pip install green
```

## Testing (for developers)
All methods that we write should be tested. There is a ```test``` folder. Its contents are 
structured in the same way as the rest of the root of the package. Each file should have a
corresponding test_MODULENAME.py file. You can run tests either like this:

```shell
$ python setup.py test # runs tests with nose
$ green -vvv
```