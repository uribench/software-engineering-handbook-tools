"""Tests of the NavigationTree class"""

import pytest
from handbook_tools.lib.navigation_tree import NavigationTree

@pytest.fixture
def navigation_tree():
    return NavigationTree('tests/fixtures/site')

def test_raises_exception_on_non_existing_configuration_file(navigation_tree):
    navigation_tree.root_config_filename = 'non_existing_file.yml'

    with pytest.raises(SystemExit):
        navigation_tree.scan(None)

def test_raises_exception_on_non_existing_configuration_path(navigation_tree):
    navigation_tree.navigation_path = 'non_existing_path/'

    with pytest.raises(SystemExit):
        navigation_tree.scan(None)
