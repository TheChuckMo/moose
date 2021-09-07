from moosetools.test.test_connect import scenarios


def pytest_addoption(parser):
    parser.addoption("--scenario", action="store", type=str, default='free_dictionary_api',
                     help=f'scenario to test: {scenarios.keys()}')


# def pytest_generate_tests(metafunc):
#     if "scenario_name" in metafunc.fixturenames:
#         metafunc.parametrize("scenario_name", metafunc.config.getoption("scenario"))


