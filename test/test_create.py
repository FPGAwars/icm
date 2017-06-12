from os import getcwd
from os.path import join, isdir, isfile, getsize

from icm.__main__ import create


def validate_create():
    cwd = getcwd()
    assert isdir(join(cwd, 'blocks'))
    assert isdir(join(cwd, 'examples'))
    assert isdir(join(cwd, 'locale'))
    assert isdir(join(cwd, 'locale/en'))
    assert isfile(join(cwd, 'locale/en/en.po'))
    assert getsize(join(cwd, 'locale/en/en.po')) > 0
    assert isfile(join(cwd, 'locale/translation.js'))
    assert getsize(join(cwd, 'locale/translation.js')) > 0
    assert isfile(join(cwd, 'LICENSE'))
    assert getsize(join(cwd, 'LICENSE')) > 0
    assert isfile(join(cwd, 'package.json'))
    assert getsize(join(cwd, 'package.json')) > 0
    assert isfile(join(cwd, 'README.md'))
    assert getsize(join(cwd, 'README.md')) > 0


def test_create(clirunner, validate_cliresult):
    with clirunner.isolated_filesystem():
        result = clirunner.invoke(create)
        validate_cliresult(result)
        validate_create()
