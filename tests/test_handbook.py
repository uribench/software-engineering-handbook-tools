"""Tests of the dispatcher for commands maintaining the Software Engineering Handbook"""

from subprocess import Popen, PIPE

def test_returns_usage_information():
    output = Popen(['./handbook.py', '-h'], stdout=PIPE).communicate()[0]
    assert b'Usage:' in output

    output = Popen(['./handbook.py', '--help'], stdout=PIPE).communicate()[0]
    assert b'Usage:' in output
