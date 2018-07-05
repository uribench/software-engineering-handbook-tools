"""Tests of the 'build' sub-command of the 'handbook' command"""

import pytest
from subprocess import Popen, PIPE

@pytest.mark.parametrize('option', ['-h', '--help'])
def test_prints_usage_information(option):
    output = Popen(['handbook_tools/handbook.py', 'build', option], stdout=PIPE).communicate()[0]
    assert b'Usage:' in output
