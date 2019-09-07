from contrail import envclasses

import os

import pytest


class TestEnvClassMeta:

    @staticmethod
    def test_env_class_meta():

        envclasses.os.environ['int_field'] = '8080'
        envclasses.os.environ['bool_field'] = 'yes'

        class TestConfig(metaclass=envclasses.EnvClassMeta):

            str_field: str = ''
            int_field: int = 8888
            bool_field: bool = False

        test = TestConfig()

        assert test.str_field == ''
        assert test.int_field == 8080
        assert test.bool_field


        envclasses.os.environ['ENV_IGNORE_ERRORS'] = 'no'
        with pytest.raises(RuntimeError):
            class TestConfig(metaclass=envclasses.EnvClassMeta):

                str_field: str
                int_field: int = 8888
                bool_field: bool = False

            test = TestConfig()

        envclasses.os.environ['ENV_IGNORE_ERRORS'] = 'yes'
        class TestConfig(metaclass=envclasses.EnvClassMeta):

            str_field: str
            int_field: int = 8888
            bool_field: bool = False

        test = TestConfig()
        assert test.str_field is None
        assert test.int_field == 8080
        assert test.bool_field


