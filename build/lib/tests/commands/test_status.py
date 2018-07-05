"""Tests of the 'status' sub-command of the 'handbook' command"""

import pytest
from handbook_tools.commands.status import Status

def test_prints_status_report(capsys):
    status = Status(global_args={'--verbose': True, 
                                 '--root': 'tests/fixtures/site'})
    status.execute()
    out, err = capsys.readouterr()
    assert '# Status Report' in out
    assert '## Metadata Files' in out
    assert '## Guides Files' in out
    assert '## Topics Files' in out
