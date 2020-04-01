# Log100Days

This is a small Quart app to render a #100DayOfCode markdown journal as a HTML page.
Quart is an async-enabled version of Flask.


## Usage

This app is designed to be pointed at the raw files of #100DayOfCode markdown journal repository.
You can clone/fork [@kallaway's original journal repo](https://github.com/kallaway/100-days-of-code) to start your log.

To find the URL for the raw files click one of the files and then the "Raw" button.
This will give you a URL like this: `https://raw.githubusercontent.com/kallaway/100-days-of-code/master/README.md`

You only need the part until the filename: `https://raw.githubusercontent.com/kallaway/100-days-of-code/master/`

The app will generate a HTML based on the content of the Markdown files in the repo.
You can see a [live implementation on my website](https://log100days.lpld.io).

## Requirements

Requires a host (or local machine) with [Docker](https://docs.docker.com/install/) installed.

## Installation

If you have `docker` installed, you don't really need to install anything.
All you need is to pull the Docker image.
```sh
$ docker pull tbrlpld/log100days
```

Depending on your OS and setup, you might have to run the docker with `sudo`.


## Configuration

If you try to run the app container with out configuring the app first, you will get an error message.
```sh
$ docker run tbrlpld/log100days
...
KeyError: 'The environment variable SECRET_KEY is missing. Be sure to configure it and try again.'
```

To enable configuration of the app running in the container, we are using environment variables.
The advantage over file based configuration is that environment variables can be created in the
container in different ways.

You can [pass environment variables to the container via the `docker-compose` file](https://docs.docker.com/compose/compose-file/#environment),
or directly [to the `docker run` command](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file).
Instead of creating each environment variable separately, you can also make use of [environment files](https://docs.docker.com/compose/compose-file/#environment#env_file) in either of these cases.

To make the environment variables easy to reuse, we use the environment file approach.
This can be done by creating a `.env` file with the following content:
```
SECRET_KEY=this-needs-to-be-something-safe
MARKDOWN_LOG_URL=https://raw.githubusercontent.com/kallaway/100-days-of-code/master/
HOME_URL=https://example.com
```

Make sure to use a safe value for the `SECRET_KEY` environment variable and **do not commit it to version control**.

The `MARKDOWN_LOG_URL` settings defines the repository where the markdown files can be found.
It does not have to be a GitHub repo.
Any URL which is extended with the Markdown filenames works.

The `HOME_URL` defines which site the "Home" link in the navigation menu should point to.
If this setting is not defined, the menu entry is omitted.

Now the use of the environment file needs to be passed to docker.
To do so, just add the `env_file` key to the `docker-compose.yml`.
```yml
        ...
        env_file:
          - .env
        ...
```

**Alternative Configuration**

The more Flask typical way of configuring through a `config.py` file in the "instance" folder is still possible.
The values defined in the `config.py` will override what is defined in the environment variables.

Since the configuration file is a Python file, use the appropriate syntax to define the values.
See the Flask documentation on [more information on how to use these configuration files](https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-files).

Copy the `config.py` file to the `/usr/src/app/instance` folder on the container.
This can be achieved by [mounting a volume](https://docs.docker.com/compose/compose-file/#volumes) at the appropriate location.

## Run the App

With the configuration file in place, you can run the app like so:
```sh
$ docker run -d --env-file .env -p 127.0.0.1:5000:5000 tbrlpld/log100days
```

To document this command and simplify how to start the app, you can use a `docker-compose.yml` file.
Just like the [`docker-compose.yml` file](./docker-compose.yml) here in this repo.

This simplifies the start up command to the following, when you are in the working directory of the `docker-compose.yml` file.
```sh
$ docker-compose up -d
```

To stop the service, run the following in the directory with the `docker-compose.yml` file.
```
$ docker-compose stop
```

*Attention* The `docker-compose.yml` file in this repo makes the container only available from the host.
This is, because I think this is a good security practice.
If you do not define the host do be only localhost, then Docker will adjust your IP tables and let outside traffic through to the container.

To achieve outside access to the app while running it only for the localhost, you can use a [reverse proxy like NGINX](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/).


## Development

### Configure and Run the App in Development

This app utilizes Docker containers for development and deployment.

During development you are going to want to update the source code often and see the changes on the page.
To achieve this with a containerized app, you want to override the source directory in the container with the one on your machine (the docker host).

```sh
$ docker run -v /Users/tibor/1-Projects/log100days:/usr/src/app -p 127.0.0.1:5000:5000 tbrlpld/log100days:latest
```

In the above example, the app directory in the container (`/usr/src/app`) is overridden by mounting the source directory on the host (e.g. `/Users/tibor/1-Projects/log100days`) to its location.

Now you can change the source code locally and the the changes are immediately available in the container.

You might not see the changes populate through to the app in the browser.
This is because, by default, the container is running the production server.
The production loads the app once on start up.
Further changes do no go through.

To see the changes during without having the stop and start the server, or container, you can run the development server.
The development server in the container can be started with the `--entrypoint` command line flag.

```sh
$ docker run  --entrypoint quart -v /Users/tibor/1-Projects/log100days:/usr/src/app -p 127.0.0.1:5000:5000 tbrlpld/log100days run -h 0 -p 5000
```

Note that the executable (`quart`) and the arguments (in this case `run`) are not written directly after one another.
Be sure to also configure the `quart` development server to accept connections from other hosts than localhost.
Only accepting connections from localhost would mean only accepting from inside the container.

The `quart` development server also requires the environment variables `QUART_APP` and `QUART_DEBUG` to be present.
For this app and development, set `QUART_APP=log100days:app` and `QUART_DEBUG=1`.
These environment variables can be added to the environment file `.env` used for configuration of the app (see the [Configuration section](#configuration) for more information).
Use the `--env-flag` to pass the environment variables from the environment file to the container.

```sh
$ docker run  --entrypoint quart --env-file .env -v /Users/tibor/1-Projects/log100days:/usr/src/app -p 127.0.0.1:5000:5000 tbrlpld/log100days run -h 0 -p 5000
```

Since this is quite the line, you might want to save this somehow.
This is where [`docker-compose`](https://docs.docker.com/compose/compose-file/) comes in.

There already is a `docker-compose.yml` file in the repo for production use.
But you can go ahead an create your own file with settings for local development.
See [`docker-compose document`](https://docs.docker.com/compose/compose-file/) for the syntax and available options.

You can run `docker-compose` with a different file than the default (`docker-compose.yml`) by using the `-f` flag.

```sh
$ docker-compose -f docker-compose-dev.yml up
```

### Build and Distribute

Run the following command to build the latest image version using the production settings.
```sh
$ docker-compose build
...
Successfully tagged tbrlpld/log100days:latest
```

Then tag this image with a version.
Make sure this is a new unused version number.
```sh
$ docker tag tbrlpld/log100days:latest tbrlpld/log100days:0.1
```

Push all the latest build images to DockerHub.
```sh
$ docker push tbrlpld/log100days
```

Builds can also be automated on [DockerHub](https://docs.docker.com/docker-hub/builds/) by following a certain branch on GitHub.

