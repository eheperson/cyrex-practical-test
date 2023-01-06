# cyrex-practical-test

## Pre-Requirements
```
    $ make evans-cli
```

pip install locust
pip install protebuf
pip install grpcio grpcio-tools
pip install python-dotenv


fix for grpco build for apple slicons :
    pip uninstall grpcio
    export GRPC_PYTHON_LDFLAGS=" -framework CoreFoundation"
    pip install grpcio --no-binary :all:
