# Log100Days

This is a small Quart app to render a #100DayOfCode markdown journal as a HTML page.
Quart is an async-enabled version of Flask.

## Usage

So far, this repo has not been turned into a package that you can install from PyPi (via pip).
Therefore, as a first step in any case is you need to clone the repository to your machine (local or server).

Depending on your usecase, follow the steps in the Development or Deployment section.

## Development

Install the app in editable mode.
```sh
$ python -m pip install -e .
```

You can run the app with Hypercorn.
Hypercorn is an ASGI (the asynchronous pendant to WSGI) server and is automatically installed with Quart.

```sh
$ hypercorn log100days:app
```

During development it is probably easier to use the quart development server.
```sh
$ export QUART_APP=log100days:app
$ export QUART_DEBUG=1
$ quart run
```

## Deployment

*For more information of how to deploy Flask/Quart apps, see the [Flask tutorial section on deployment](https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/).*

### Build
Build the wheel for distribution on your development machine.
```sh
$ python setup.py bdist_wheel
```

### Install
Copy the resulting `.whl` file from the `/dist` directory to the server (e.g. with scp).
On the server, install the wheel in a virtual environment.
*The directories for the installation are only examples. You only need to make sure your paths are consistent.*
```sh
$ cd /srv/www/<appname>
$ python -m venv venv
$ /srv/www/<appname/venv/bin/python -m pip install <filename>.whl
```
This should install the app and all it's dependencies in the virtual environment.

The next step is to configure the app for your usecase.
This app is configured with the idea of a config file in the [Flask instance folder](https://flask.palletsprojects.com/en/1.1.x/config/#instance-folders).
If not configured otherwise, you should find the instance folder in the virtual environment folder (e.g. `/srv/www/<appname>/venv/var/<appname>-instance/`).
Change into that folder and create a `config.py` in which you define your Markdown log repo.
Be sure to use the URL of the raw markdown files!
**Do not provide a filename.**

```shell
$ cd /srv/www/<appname>/venv/var/<appname>-instance/
$ nano config.py
```

With nano, add your config settings.
```python
SECRET_KEY = b"something-secret"
LOG_REPO = https://raw.githubusercontent.com/tbrlpld/100-days-of-code/master/
```

That's it.

### Run
When running it in production, use the following.
```sh
$ hypercorn --workers 3 --bind 127.0.0.1:5000 log100days:app
```

This is better done as a service, so that it runs in the background and automatically starts with the server.
To create a service on a Ubuntu server copy the `log100days.service` file to `/etc/systemd/system/log100days.service`.
Once this file is created, you can manage the service with `systemctl`.

```sh
$ systemctl enable log100days
$ systemctl start log100days
$ systemctl status log100days
```

The filename in `/etc/systemd/system/` without the `.service` extension defines the name of the service.