import envclasses

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


    @staticmethod
    def test_lazy_init_of_env():
        if 'int_field' in envclasses.os.environ:
            del envclasses.os.environ['int_field'] 

        if 'bool_field' in envclasses.os.environ:
            del envclasses.os.environ['bool_field']

        envclasses.os.environ['ENV_IGNORE_ERRORS'] = 'yes'
        envclasses.os.environ[envclasses._PYENV_CLASS_REFRESH_LOAD_FLAG] = 'True'

        class TestLazyConf(metaclass=envclasses.EnvClassMeta):
            str_field: str = 'test'
            int_field: int
            bool_field: bool

        test = TestLazyConf()

        assert test.str_field == 'test'
        assert not test.bool_field
        assert not test.int_field

        envclasses.os.environ['int_field'] = '100'
        envclasses.os.environ['bool_field'] = 'True'

        assert test.str_field == 'test'
        assert test.int_field == 100
        assert test.bool_field



