# cyrex-practical-test
Python Developer Assesment for the Cyrex
> You can find the locust load testing reports in the `./reports` directory.
> 
> Each time the program is run, the report files will be automatically saved in this folder, 
> regardless of which method the program is run with(with docker or locally).
## Directory Structure:
```
├── cyrex-practical-test
    ├── lab ****
    ├── Python Dev - Practical Test
    ├── reports
    ├── src
    ├── .gitignore
    ├── docker-compose.yml
    ├── Makefile
    └── README.md
```

* **`/Python Dev - Practical Test :`** directory to store task description and required files
* **`/lab :`** directory to run test scrips, for perdonal use only.
* **`/reports :`** directory to store locust load testing report
* **/`src :`** directory to store source code
  
# Preparetion
## 1. Clone the repository:
```
    $ git@github.com:eheperson/cyrex-practical-test.git
    $ cd cyrex-practical-test
```

## 2. Run :

> **Note :** Before all, you need to create `.env` file in the `.cyrex-practival-test/src` directory, and fill it.

### Docker:
```
	$ sudo chmod +x ./src/entrypoint.sh
	$ docker-compose up -d --build; docker logs --follow worker
```

>if you have makefile, just run those commands in root directory of the project:
>```
>    $ make start-docker
>```
>

### Local:
>This option only tested on MacOS, 
```
	$ brew install protobuf
	$ brew tap ktr0731/evans
    $ brew install evans
	$ python -m venv venv
	$ source venv/bin/activate
	$ pip install --upgrade pip
	$ pip install -r ./src/requirements.txt
	$ locust -f ./src/app/main.py --config ./src/confs/locust.conf
```

>if you have makefile, just run those commands in root directory of the project:
>```
>    $ make prepare
>    $ make locust_run
>```


# Notes
### fix for grpco build for apple slicons :
```
    pip uninstall grpcio
    export GRPC_PYTHON_LDFLAGS=" -framework CoreFoundation"
    pip install grpcio --no-binary :all:
```
