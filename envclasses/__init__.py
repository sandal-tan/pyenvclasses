"""Environment classes to define configuration from environment variables"""

# Python Standard Library
import inspect
import os
from dataclasses import InitVar, dataclass, field
from typing import Any, Callable, Dict

BOOL_MAP: Dict[str, bool] = {'yes': True, 'true': True, 'false': False, 'no': False}
"""The mapping of strings to their boolean."""

IGNORE_ERRORS_FLAG: str = 'env_ignore_errors'
"""The environment variable to define for disabling None checks for fields."""


def post_init(self, env_ignore_errors: bool = False):
    """Define the post initialization for the environment.

    This allows us to throw errors in one place and report all errors in the environment. This also allows us to
    ignore whichever failures we want in testing mode.

    Args:
        env_ignore_errors: Whether or not to ignore errors

    Raises:
        RuntimeError: If environment variables are evaluated to not be true

    """
    attributes = dict(inspect.getmembers(self))
    annotations = attributes['__annotations__']
    if not env_ignore_errors:
        errors = [
            _field.upper()
            for _field in annotations
            if attributes[_field] is None and _field != IGNORE_ERRORS_FLAG
        ]
        if errors:
            raise RuntimeError(F'The following environment variables are undefined: {", ".join(errors)}')

def bool_caster(value: Any) -> bool:
    """Cast smartly to a bool.

    If passed a string, values "yes", "no", "true", "false" will be converted to a boolean with the correct
    state

    Args:
        value: The value to cast

    Returns:
        A boolean corresponding to ``value``

    """
    if isinstance(value, str) and value:
        return BOOL_MAP[value.lower()]
    return bool(value)


def make_cast_function(type_: Callable) -> Callable:
    """Make a cast function for a given type.

    This is to ensure that None is propagated correctly and not converted to another type.

    Args:
        type_: The type to cast the value to

    Returns:
        A function to cast to a type, preserving None

    """

    def _wrapper(value: Any) -> Any:
        """Wraps the cast function to preserve None

        Args:
            value: The value to cast

        Returns:
            The casted type or None

        """
        if value is None:
            return value
        return type_(value)

    return _wrapper

_PYENV_CLASS_REFRESH_LOAD_FLAG = '_PYENV_CLASS_REFRESH_LOAD'

def _fresh_access_property_maker(name: str, cast_function: Callable, default_set: Any = None) -> property:
    """Creates an env property which will read from the env on every access.

    Args:
        name: The name of the prop.
        cast_function: thbe casting fuction to covert string a string encoding of the value to a python native type.
        default_set: A value to use if the env has nothing. Defaults to None.

    Returns:
        A property to assign to an env class.
    """
    internal_attr_name = '_' + name.lower()

    @property
    def prop(self):
        self.__dict__[internal_attr_name] = cast_function(
            os.environ.get(
                name.upper(), 
                os.environ.get(name.lower(), default_set)
            )
        )
        return getattr(self, internal_attr_name)

    @prop.setter
    def prop(self, value):
        setattr(self, internal_attr_name, value)

    return prop


class EnvClassMeta(type):
    """Metaclass to provide the transformation of an environment class into a dataclass."""

    def __new__(cls, class_name: str, superclasses: Any, attributes: Dict[str, Any]) -> Any:
        """Wrap a class, creating a dataclass from environment variables.

        Args:
            class_name: The name of the class that this metaclass is creating
            superclasses: The superclasses of the base class we are wrapping
            attributes: The attributes of the class we are wrapping

        Returns:
            The wrapped class

        """

        annotations = attributes['__annotations__']
        for name, annotation in annotations.items():
            cast_function = make_cast_function(annotation if annotation is not bool else bool_caster)
            value = attributes.get(name)

            if os.environ.get(_PYENV_CLASS_REFRESH_LOAD_FLAG):
                prop = _fresh_access_property_maker(
                    name=name,
                    cast_function=cast_function,
                    default_set=value
                )
                attributes[name] = prop
            else:
                attributes[name] = field(
                    default=cast_function(os.environ.get(name.upper(), os.environ.get(name.lower(), value)))
                )

        attributes['__annotations__'][IGNORE_ERRORS_FLAG] = InitVar
        attributes[IGNORE_ERRORS_FLAG] = field(
            default=bool_caster(os.environ.get(IGNORE_ERRORS_FLAG.upper(), False))
        )
        attributes['__post_init__'] = post_init

        return dataclass(type.__new__(cls, class_name, superclasses, attributes))
