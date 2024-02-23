# Development #

## Creating an editable install ##

We're using [Pipenv](https://docs.pipenv.org/) to manage dependency package installation.
They provide [instructions for installing Pipenv](https://docs.pipenv.org/#install-pipenv-today).

Once Pipenv is installed, you can install the dependencies for smoothmath into a virtual
environment by running:
```
pipenv install
```

To get a shell in the virtual environment, run:
```
pipenv shell
```

We can use pip to install our package in our virtual environment using "editable mode", 
which allows our isntalled packge to automatically reflect code changes:
```
pip install --editable .
```


## Testing ##

We use [pytest](https://docs.pytest.org) for testing. Before running the test suite, 
you'll need to install smoothmath (using editable mode or otherwise). To run the test 
suite, execute:
```
pytest
```


## Documenting ##

We are using [sphinx-doc](https://www.sphinx-doc.org) to build this project's 
documentation. From the `docs/` directory, run:
```
make clean && make doctest && make html
```

This will remove old build artifacts, then ensure in-documentation code executes 
correctly, and finally builds the html documentation. The output can be found in
`docs/build/html/`.
