from icm.__main__ import create, update


def test_create(clirunner, validate_cliresult):
    with clirunner.isolated_filesystem():
        clirunner.invoke(create)
        result = clirunner.invoke(update)
        validate_cliresult(result)
