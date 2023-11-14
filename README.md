# Smooth Math #

Evaluate and differentiate smooth expressions!


### Installation ###

We're using [Pipenv](https://docs.pipenv.org/) to manage dependency package installation.
They provide [instructions for installing Pipenv](https://docs.pipenv.org/#install-pipenv-today).

Once Pipenv is installed, you can install the dependencies for smoothmath by running:
```
pipenv install
```

To get a shell in the virtual environment, run:
```
pipenv shell
```


### Testing ###

We use [pytest](https://docs.pytest.org) for testing. Before running the test suite, you'll need to
install smoothmath. To install smoothmath in the virtual environment:
```
pip install .
```

To install smoothmath in the virtual environment for use while developing smoothmath 
(i.e. in "editable mode"), execute:
```
pip install --editable .
```

To run the test suite, execute:
```
pytest
```
