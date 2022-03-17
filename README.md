# Library Management

Library Management is a Django REST project to serve APIs

##Local setup
Python version == 3.10

- Use the [link](https://www.python.org/downloads/) to install the latest version of python.
- If pip (package installer for python) is not installed, user the [link](https://pip.pypa.io/en/stable/getting-started/) to install the latest version of python.
- We will be using virtualenv to isolate python environments. Use the following command to install virtualenv. More info can be found on [link](https://pypi.org/project/virtualenv/).
```bash
pip install virtualenv
```
- To create a virtualenv use the following command:
```bash
virtualenv -p python3.10 venv
```
- To activate the virtualenv, use the following command:
```bash
source <path to virtualenv dir>/bin/activate
```
- After activating the virtualenv, install the project dependencies using the following command:
```bash
pip install -r requirements.txt
```
- Set up a postgres database server in the local machine. Use the [link](https://www.postgresql.org/download/) to download the latest version of Postgres.
- For the project create a database using the following credentials
```bash
'NAME': 'library_db',
'USER': 'library_db_user',
'PASSWORD': '_vftqd352kL@'
```
- If the database is created under a different credential edit the DATABASES variable in the settings.py file accordingly.
- To apply the database migrations use the following command, also make sure the virtualenv is active:
```bash
python manage.py migrate
```

Note: All the commands listed are for UNIX based OSs, for windows you might need to find the alternative commands.
