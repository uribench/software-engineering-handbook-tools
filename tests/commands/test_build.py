"""Tests of the 'build' sub-command of the 'handbook' command"""

from subprocess import Popen, PIPE

def test_returns_usage_information():
    output = Popen(['./handbook.py', 'build', '-h'], stdout=PIPE).communicate()[0]
    assert b'Usage:' in output

    output = Popen(['./handbook.py', 'build', '--help'], stdout=PIPE).communicate()[0]
    assert b'Usage:' in output
