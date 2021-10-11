![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)
[![PyPI version](https://badge.fury.io/py/pyenvclasses.svg)](https://badge.fury.io/py/pyenvclasses)
![Tests](https://github.com/sandal-tan/pyenvclasses/workflows/.github/workflows/test.yaml/badge.svg)

# Envclasses

Envclasses are a thin wrapper around dataclasses which allows for the values to be defined via environment variables
rather than explicitly in code. Values are typed and are able to be defaulted. 

## Motivation

I got tired of writing code that was configured through environment variables, referencing the environment variable 
when I needed to instantiate something. This made it difficult to keep up with how I could configure that software that
I was writing as I would have to comb through the code and make sure that the documentation was up to date. 

Envclasses are an attempt to reduce the sprawl of configuration through environment variables and centralize
configuration into a single, document-able class. They are both inspired by, and built on top of dataclasses, which is
why their structure is so similar.

## Usage

Defining an environment class is simple:

```python

from envclasses import EnvClassMeta

class ApplicationConfig(metaclass=EnvClassMeta):

    db_url: str
    db_username: str
    db_password: str
    port: int = 5050
    mode: str = 'development'


config = ApplicationConfig()
```

The provided metaclass will turn the `ApplicationConfig` into a dataclass with fields defined from `os.environ`.
The metaclass will prioritize upper-case versions of fields before lower-case, that is to say `DB_URL` would be
prioritized over `db_url`. Mixed-case variants are not considered.

If values are not defined, the metaclass will wait until all fields have been tested to report which are missing. In the
event that we should ignore missing fields, the environment variable `env_ignore_missing` should be defined as `true` or
`yes`.


## Refresh Mode
In cases of testing, having the environment read once at initialization of the module its defined in isn't ideal.
It can lead to a lot of plumbing work to overwrite mock values and import sequences. 

For cases liek this, using Refresh Mode might be appropriate. In this mode, the env class will re-read any 
environment variable of a given attriubute on access of said attribute. For example:

```python

from envclasses import EnvClassMeta

class FreshLoadingConfig(metaclass=EnvClassMeta):
    test_var: int


envclasses.os.environ['ENV_IGNORE_ERRORS'] = 'yes'
envclasses.os.environ['PYENV_CLASS_REFRESH_LOAD'] = 'yes'
config = ApplicationConfig()

print(config.test_var)
# prints "None"

envclasses.os.environ['test_var'] = '100'


print(config.test_var)
# prints "100"
```

Note that you should use this behaviour in production given the dynamic nature of it. It is only meant for testing
ease.