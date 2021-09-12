from moosetools import __version__, __app__

import pkg_resources


def test_version():
    assert __version__ == pkg_resources.get_distribution(__app__).version
