# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner


@pytest.fixture(scope='module')
def clirunner():
    return CliRunner()


@pytest.fixture(scope='session')
def validate_cliresult():
    def decorator(result):
        print(result)
        assert result.exit_code == 0
        assert not result.exception
        assert 'error' not in result.output.lower()
    return decorator
