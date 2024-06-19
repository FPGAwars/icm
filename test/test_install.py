from icm.__main__ import install


def test_install(clirunner, validate_cliresult):
    with clirunner.isolated_filesystem():
        clirunner.invoke(install)



# -- Test
    # install_main(collection, "iceK@0.1.4", True)
    # install_main(collection, "iceK", True)
    # install_main(collection, "iceK@0.1.3")
    # install_main(collection, "iceK")
    # install_main(collection, "iceWires")
    # install_main(collection, "iceIO")
    # install_main(collection, "iceGates")
    # install_main(collection, "iceMux")
    # install_main(collection, "iceCoders")
    # install_main(collection, "iceFF")
    # install_main(collection, "iceRegs")
    # install_main(collection, "iceSRegs")