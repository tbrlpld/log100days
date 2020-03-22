# Log100Days

This is a small Quart app to render my #100DayOfCode journal repo from Github.

Quart is an async-enabled version of Flask.

To run the app, use Hypercorn. It comes with Quart.
```bash
$ hypercorn log100days:app
```



## Deployment

When running it in production, use the following.
```bash
$ hypercorn --workers 3 --bind 127.0.0.1:5000 log100days:app
```

This is better done as a service, so that it runs in the background and automatically starts with the server.
To create a service on a Ubuntu server copy the `log100days.service` file to `/etc/systemd/system/log100days.service`.
Once this file is created, you can manage the service with `systemctl`.

```shell
systemctl enable log100days
systemctl start log100days
systemctl status log100days
```

The filename in `/etc/systemd/system/` without the `.service` extension defines the name of the service.