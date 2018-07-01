"""Tests of the dispatcher for commands maintaining the Software Engineering Handbook"""

import pytest
from subprocess import Popen, PIPE

@pytest.mark.parametrize('option', ['-h', '--help'])
def _test_prints_usage_information(option):
    output = Popen(['./handbook.py', option], stdout=PIPE).communicate()[0]
    assert b'Usage:' in output