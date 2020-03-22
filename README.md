Log100Days
==========

This is a small Quart app to render my #100DayOfCode journal repo from Github.

Quart is an async-enabled version of Flask.

To run the app, use Hypercorn. It comes with Quart.
```bash
$ hypercorn log100days:app
```

When running it in production, use the following.
```bash
$ hypercorn --workers 3 --bind 127.0.0.1:5000 log100days:app
```
