[![Build Status](https://travis-ci.org/uribench/software-engineering-handbook-tools.svg?branch=master)](https://travis-ci.org/uribench/software-engineering-handbook-tools)
[![Maintainability](https://api.codeclimate.com/v1/badges/60f2e373b5ca64453968/maintainability)](https://codeclimate.com/github/uribench/software-engineering-handbook-tools/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/60f2e373b5ca64453968/test_coverage)](https://codeclimate.com/github/uribench/software-engineering-handbook-tools/test_coverage)
[![PyPI version](https://badge.fury.io/py/handbook-tools.svg)](https://badge.fury.io/py/handbook-tools)

# Handbook Tools

A collection of automation scripts to build and maintain the `Handbook` directory of the 
[Software Engineering Handbook][1] repository.

## Package Installation and Usage

The handbook tools are implemented in Python 3 as a command line and are available as a Pip package.

### Package Installation

Make sure you have the Python 3 version of pip installed:

```bash
$ sudo apt upgrade python3-pip
```

Install the handbook-tools package:

```bash
$ pip3 install handbook-tools --user
```

### Package Usage

The tools are used with a dispatcher called `handbook` that is executing dedicated commands in the
following pattern:

```bash
$ handbook [options] <command> [<args>...]
```

Run the following command to get help on the handbook tools usage:

```bash
$ handbook -h 
```

## Source Code

If you would like to contribute changes and enhancement to the handbook tools, fork and clone this
repository, make changes and propose a pull request.

### File Structure

Following is a partial structure of the source code files showing only the main parts:

```

software-engineering-handbook-tools/    root of the repository
|  ├──commands/                         folder of commands that are automatically discovered
|  |  ├──build.py                       builds the Handbook from configuration
|  |  ├──status.py                      generates various status reports about the Handbook
|  |  └──toc.py                         composes a TOC of the Handbook from configuration
|  ├──lib/                              common libraries
|  └──handbook.py                       the main script
├──tests/                               collection of tests for the handbook tools
└──setup.py                             package configuration file

```

### Running the Tests

To run the tests on the cloned repository:

```bash
$ python setup.py test
```

The above command uses the package definitions in the `setup.py` configurations file and is 
equivalent to the following command:

```bash
$ pytest --cov-report term-missing --cov=handbook_tools
```

This executes [pytest][2] with the [pytest-cov][3] plugin for [Coverage.py][4].

### Building the Package

Make sure you have the latest versions of setuptools and wheel installed:

```bash
$ python3 -m pip install --user --upgrade setuptools wheel
```

Now run this command from the same directory where setup.py is located:

```bash
$ python3 setup.py sdist bdist_wheel
```

This command should output a lot of text and once completed should generate two files in the 
`dist` and `build` directories.

The `dist/tar.gz` file is a source archive whereas the `dist/*.whl` file is a built distribution
that can be installed locally without uploading it to PyPi. This is useful during testing. See 
instructions under the chapter "Installing your newly uploaded package" below.

Newer pip versions preferentially install built distributions, but will fall back to source archives 
if needed. You should always upload a source archive and provide built archives for the platforms 
your project is compatible with. In this case, our example package is compatible with Python on any 
platform so only one built distribution is needed.

### Installing the Package Locally

To install the package locally from a wheel file without uploading to a remote packages repository
such as [PyPi][5]:

```bash
$ pip3 install dist/<wheel-package-file>.whl
```

Example:

```bash
$ pip3 install dist/handbook_tools-0.3.2-py2.py3-none-any.whl
```

---

[1]: https://github.com/uribench/software-engineering-handbook
[2]: https://docs.pytest.org/en/latest/
[3]: https://pypi.org/project/pytest-cov/
[4]: https://coverage.readthedocs.io/
[5]: https://pypi.org/