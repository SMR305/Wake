# Wake

Wake is an early-stage Django dashboard for keeping track of servers and other
machines on a local network. It is intended to run on an always-available
"lead" server and eventually provide a single place to start, reboot, and shut
down managed machines.

The repository currently implements the dashboard and part of the status-update
plumbing. It does **not** yet provide reliable remote power management and
should not be treated as production-ready.

## Current functionality

Implemented:

- stores a unique name, MAC address, optional IP address, and on/off flag for
  each managed server in SQLite
- displays each stored server on the dashboard, with its saved on/off state
- adds test server records and toggles their saved state from the dashboard
- exposes an endpoint for deleting server records (there is no dashboard
  control for it yet)
- broadcasts model changes to connected dashboards over a Django Channels
  WebSocket so open pages can update without a reload
- starts a TCP listener on port `5000` under ASGI; a received connection toggles
  the record with database ID `3`

Partially implemented:

- Wake-on-LAN code is present, but it is disabled by the `WAKE_UP = False`
  development flag and uses `TEST_MAC` instead of the selected server's stored
  MAC address
- the power button changes the database flag; it does not currently establish
  whether a machine is online or send it a shutdown request
- the add-server UI creates placeholder values and input validation is bypassed
  while `TEST = True`
- the reboot route currently renders a placeholder page
- the TCP listener accepts any connection, has no message protocol or
  authentication, and is hard-coded to one database record

Planned work includes authenticated access, real shutdown and reboot agents on
managed machines, and status or uptime tracking that can detect changes made
outside Wake.

## How it works

The Django application runs on the lead server. Server records are persisted in
the local SQLite database and rendered into the dashboard. Changes to those
records trigger Django model signals, which publish events through an in-memory
Channels layer to browsers connected at `ws/servers/`.

The ASGI application also starts a background TCP listener on `0.0.0.0:5000`.
That listener is experimental and currently only toggles one hard-coded record.
Because the channel layer is in memory, live updates are limited to a single
application process.

Wake-on-LAN requires the lead server to be able to reach the target machine's
network and the target hardware and firmware to have Wake-on-LAN enabled. The
current code does not yet complete that flow.

## Requirements

- Python; the project does not currently declare a supported version
- Django, Channels, Daphne, and `wakeonlan`
- a free local TCP port `5000` when starting the ASGI application
- for future Wake-on-LAN use, compatible target hardware configured for
  Wake-on-LAN and network routing that permits the magic packet

There is currently no `requirements.txt`, `pyproject.toml`, or other dependency
lock file. Consequently, a clean clone cannot be installed reproducibly and
the exact compatible dependency versions are not documented.

## Configuration

Both `wake/wake/settings.py` and `wake/wake/views.py` import values from an
untracked `wake/wake/variables.py` file. Create that file locally with these
names before running a Django command:

```python
VAR_SECRET_KEY = "replace-with-a-private-django-secret-key"
HOSTS = ["localhost", "127.0.0.1"]
TEST_MAC = "00:00:00:00:00:00"
```

`VAR_SECRET_KEY` must be private. `HOSTS` becomes Django's `ALLOWED_HOSTS` list,
and `TEST_MAC` is the development MAC address referenced by the incomplete
Wake-on-LAN path. Replace the example values locally as appropriate. Do not
commit `variables.py`; it is excluded by `.gitignore`.

This file-based configuration is a current project limitation rather than a
recommended secrets-management approach.

## Setup

Clone the repository and change into the Django project directory containing
`manage.py`:

```console
git clone https://github.com/SMR305/Wake.git
cd Wake/wake
```

Create and activate a virtual environment, then install Django, Channels,
Daphne, and `wakeonlan` using versions appropriate for your Python environment.
The repository cannot yet provide a verified dependency installation command
because it contains no dependency metadata.

After creating `wake/wake/variables.py` as described above, initialize the
database and start the development server from `Wake/wake`:

```console
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. The dashboard shows persisted records and lets
you add placeholder records or toggle their saved state. Those controls do not
currently perform real power operations.

## Project structure

```text
Wake/
|-- .github/workflows/django.yml  # Current Django CI workflow
|-- wake/
|   |-- manage.py                 # Django command entry point
|   |-- templates/                # Dashboard and placeholder templates
|   |-- static/                   # Static asset directories
|   `-- wake/
|       |-- settings.py           # Django and Channels configuration
|       |-- models.py             # Persisted Server model
|       |-- views.py              # Dashboard and JSON endpoints
|       |-- consumers.py          # WebSocket consumer
|       |-- signals.py            # Model-change broadcasts
|       |-- listener.py           # Experimental TCP listener
|       `-- migrations/           # Database schema history
|-- LICENSE.txt
`-- README.md
```

## Known limitations

- no login, authorization, or protection for the server-control endpoints
- no working shutdown or reboot agent on managed machines
- no reliable online-state detection or uptime tracking
- Wake-on-LAN is disabled and not connected to each server's stored MAC address
- development flags bypass add-server validation
- the TCP listener is unauthenticated and tied to a hard-coded database ID
- the in-memory channel layer does not support multiple application processes
- dependency versions and a reproducible installation process are missing
- no automated tests are currently included

The existing GitHub Actions workflow is not currently runnable from a clean
checkout: it installs from a root-level `requirements.txt` that does not exist,
and its `cd wake` occurs in a different step from `python manage.py test`, so
the test command runs from the wrong directory. Tests would also need the local
`variables.py` configuration described above.

## Contributing

Issues and focused pull requests are welcome. Before changing behavior, please
open or reference an issue, keep implemented and planned functionality clearly
separated, and include tests when the repository gains a reproducible test
environment.

## License

Wake is available under the [MIT License](LICENSE.txt).
