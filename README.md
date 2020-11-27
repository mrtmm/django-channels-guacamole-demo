This repository contains the bare minimum for using [Guacamole](https://guacamole.apache.org/) from a Django project,
to connect to a remote `SSH` target.

`consumers.py` implements the [AsyncWebsocketConsumer](https://github.com/django/channels/blob/master/channels/generic/websocket.py#L150) from `channels` and uses [pyguacamole](https://pypi.org/project/pyguacamole/) library to connect to target.

To try out this repo, one needs a running `guacd` instance and a remote `SSH` target.

One option for `guacd` is to run it with [docker](https://hub.docker.com/r/guacamole/guacd):

    ```
    docker pull guacamole/guacd
    docker run -e GUACD_LOG_LEVEL=debug --name some-guacd -d -p 4822:4822 guacamole/guacd
    ```

Edit the `settings` accordingly:

    ```
    # guacd daemon host address and port
    GUACD_HOST = 'GUACD_IP'
    GUACD_PORT = 4822

    # ssh login settings
    SSH_HOST = 'SSH_TARGET_IP'
    SSH_PORT = 22
    SSH_USER = 'user'
    SSH_PASSWORD = 'password'
    SSH_PRIVATE_KEY = '<private_key>'
    ```

Run:

    ```
    pip install -r requirements.txt
    python3 manage.py runserver
    ```

Open browser at `http://localhost:8000/ws`
