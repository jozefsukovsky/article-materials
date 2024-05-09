import timeit

NUMBER = 100000

libs = ['json', 'orjson', 'ujson', 'simplejson', 'rapidjson']


def test_lib_dumps(lib: str):
    setup = f"""
import {lib}
from test_data import test_data
"""

    statement = f"""
{lib}.dumps(test_data)
"""

    result = timeit.timeit(
        statement,
        setup=setup,
        number=NUMBER
    )
    print(f'{lib}: {result}')


def test_lib_loads(lib: str):
    setup = f"""
import json
import {lib}
from test_data import test_data
pload = json.dumps(test_data)
"""

    statement = f"""
{lib}.loads(pload)
"""

    result = timeit.timeit(
        statement,
        setup=setup,
        number=NUMBER
    )
    print(f'{lib}: {result}')


if __name__ == '__main__':
    print('dumps')
    for x in libs:
        test_lib_dumps(x)

    print('loads')

    for x in libs:
        test_lib_loads(x)

