# Envclasses

[![CircleCI](https://circleci.com/gh/sandal-tan/py-envclasses.svg?style=svg)](https://circleci.com/gh/sandal-tan/py-envclasses)

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
