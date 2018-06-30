"""Tests of the 'build' sub-command of the 'handbook' command"""

import pytest
from subprocess import Popen, PIPE

@pytest.fixture(params=['-h', '--help'])
def test_prints_usage_information(request):
    output = Popen(['./handbook.py', 'build', request.params], stdout=PIPE).communicate()[0]
    assert b'Usage:' in output
