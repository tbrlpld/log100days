# Log100Days

This is a small Quart app to render a #100DayOfCode markdown journal as a HTML page.

Quart is an async-enabled version of Flask.

To run the app, use Hypercorn. It comes with Quart.
```sh
$ hypercorn log100days:app
```


## Deployment

See the [Flask tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/) more info on the deployment.

Build the wheel for distribution with
```sh
$ python setup.py bdist_wheel
```

Copy the resulting `.whl` file from the `/dist` directory to the server.
On the server, install the wheel in a virtual environment.
```sh
$ pip install <filename>.whl
```

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