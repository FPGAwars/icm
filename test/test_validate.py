from icm.__main__ import create, validate


def test_create(clirunner, validate_cliresult):
    with clirunner.isolated_filesystem():
        clirunner.invoke(create)
        result = clirunner.invoke(validate)
        validate_cliresult(result)
