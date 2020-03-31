# Log100Days

This is a small Quart app to render a #100DayOfCode markdown journal as a HTML page.
Quart is an async-enabled version of Flask.

## Usage

So far, this repo has not been turned into a package that you can install from PyPi (via pip).
Therefore, as a first step in any case is you need to clone the repository to your machine (local or server).

Depending on your use case, follow the steps in the [Development](#development) or [Deployment](#deployment) section.


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
The `MARKDOWN_LOG_URL` settings defines the repository where the markdown files can be found.
It does not have to be a GitHub repo.
Any URL which is extended with the Markdown filenames works.

The `HOME_URL` defines which site the "Home" link in the navigation menu should point to.
If this setting is not defined, the menu entry is omitted.

```python
SECRET_KEY = b"something-secret"
MARKDOWN_LOG_URL = "https://raw.githubusercontent.com/tbrlpld/100-days-of-code/master/"
HOME_URL = "https://lpld.io"
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


## Development

This app utilizes Docker containers for development and deployment.

During development you are going to want to update the source code often and see the changes on the page.
To achieve this with a containerized app, you want to override the source directory in the container with the one on your machine (the docker host).

```sh
docker run -v /Users/tibor/1-Projects/log100days:/usr/src/app -p 127.0.0.1:5000:5000 tbrlpld/log100days:latest
```

In the above example, the app directory in the container (`/usr/src/app`) is overridden by mounting the source directory on the host (`/Users/tibor/1-Projects/log100days`) to its location.

Now you can change the source code locally and the the changes are immediately available in the container.

You might not see the changes populate through to the app in the browser.
This is because, by default, the container is running the production server.
The production loads the app once on start up.
Further changes do no go through.

To see the changes during without having the stop and start the server, or container, you can run the development server.
The development server in the container can be started with the `--entrypoint` command line flag.

```sh
docker run  --entrypoint quart -v /Users/tibor/1-Projects/log100days:/usr/src/app -p 127.0.0.1:5000:5000 tbrlpld/log100days run -h 0 -p 5000
```

Note that the executable (`quart`) and the arguments (in this case `run`) are not written directly after one another.



Then in the repo, create a `/instance` folder and place a `/config.py` inside.
Add the configuration variables as seen in the [Deployment](#deployment) section to this file.

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