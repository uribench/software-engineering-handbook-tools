"""Tests of the 'toc' sub-command of the 'handbook' command"""

import pytest
from commands.toc import Toc

def test_prints_toc(capsys):
    toc = Toc(global_args={'--verbose': True, 
                           '--root': '../software-engineering-handbook'})
    toc.execute()
    out, err = capsys.readouterr()
    assert '# Table of Contents' in out
