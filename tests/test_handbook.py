"""Tests of the dispatcher for commands maintaining the Software Engineering Handbook"""

import pytest
from subprocess import Popen, PIPE

@pytest.fixture(params=['-h', '--help'])
def test_prints_usage_information(request):
    output = Popen(['./handbook.py', request.params], stdout=PIPE).communicate()[0]
    assert b'Usage:' in output
