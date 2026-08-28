
# Wake
**NOTE:** *This application is not currently in a working state.*
*If you would like to help me get there faster please consider contributing to one of the outstanding issues.*
*Otherwise I will continue my process of working on it and developing it to hopefully be in a functional state soon.*

Wake is a project which allows you to make a network of servers and other computers. The way it works is by running the main application on the "lead" or "parent" server which runs and hosts a dashboard accessible through a web browser that allows the user to send commands to shutdown, startup, or reboot any of the child servers. Meanwhile, the child servers will run a lightweight connector that allows for the main server to properly issue these commands and keep track of the actual active status of the servers.

## Restrictions
For proper functionality of this project there are a few key things to keep in mind.
- The child servers need to support wakeonlan and connected via ethernet
- The lead server must be on the same lan network as all the child servers

## Secrets
Secrets for this environment are stored in a .env file that is not shared in this repository for obvious reasons.
If you wish to use this project on your own you will need to set those up yourself by obtaining your own and setting them in a .env file somewhere within the project.

The current secrets are:
- TEST_MAC - This is a testing parameter, so you actually shouldn't need it, but I was using it to test the wake functionality on my actual computer.
- VAR_SECRET_KEY (required) - This is the secret key used in production for Django
- HOSTS (required) - This is the list of available hosts for the Django webapp. By default you can set it to "localhost,127.0.0.1".

## Requirements
The requirements for this project can be found in requirements.txt, but for a more general overview.

### Python 3.14.6
- Wake on Lan
- Django
- Django Channels
- Daphne
- python-dotenv

## Setup
Clone the repository and navigate into the folder that contains the `manage.py` file (located in the top level folder called `wake`)

```console
git clone https://github.com/SMR305/Wake.git
cd Wake/wake
```

Then make a virtual environment and use the `requirements.txt` to install necessary dependencies.

```console
pip install -r requirements.txt
```

Set up the secrets that were discussed in the [Secrets Section](#secrets) (you only need to set up the required ones)

```python
TEST_MAC = "MAC address you wanna test with (ex '00:00:00:00:00:00')"
VAR_SECRET_KEY = 'Your Django Secret'
HOSTS = "Comma seperated list of hosts (ex 'localhost,127.0.0.1')"
```

Then you need to initialize the database (you'll need to either be in the same folder as manage.py or include the path to it)

```console
python manage.py migrate
```
The finally you can run the development build by using (again either form the same folder as manage.py or including the path to it)

```console
python manage.py runserver
```

The dashboard is currently displayed at `http://{one-of-the-hosts-you-entered}:8000/`, and for now just shows a series of buttons that update states in the database through POST requests.

## Tests
The set of tests for the project are still a work in progress along with the rest of the application. That being said, contributions to the testing cases are also appreciated. However, do know that those contributions are held to the same standard as contributions to the rest of the project.

## Contributions
The core rules around contributions can be found in [CONTRIBUTIONS](CONTRIBUTING.md).

## License
Wake is available under the [MIT License](LICENSE.txt).
