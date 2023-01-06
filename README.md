# cyrex-practical-test

## Preparetion

1. Clone the repository:
```
    $ git@github.com:eheperson/cyrex-practical-test.git
```




fix for grpco build for apple slicons :
    pip uninstall grpcio
    export GRPC_PYTHON_LDFLAGS=" -framework CoreFoundation"
    pip install grpcio --no-binary :all:
