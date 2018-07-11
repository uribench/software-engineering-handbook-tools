"""Tests of the NavigationTree class"""

import pytest
from handbook_tools.lib.navigation_tree import NavigationTree

@pytest.fixture
def navigation_tree():
    return NavigationTree('tests/fixtures/site')

def test_raises_exception_on_non_existing_configuration_path(navigation_tree):
    non_existing_navigation_path = 'non_existing_path/'
    existing_tree_config_filename = navigation_tree.tree_config_filename

    with pytest.raises(SystemExit):
        navigation_tree.load_tree_config_file(non_existing_navigation_path,
                                              existing_tree_config_filename)

def test_raises_exception_on_non_existing_configuration_file(navigation_tree):
    existing_navigation_path = navigation_tree.navigation_path
    non_existing_tree_config_filename = 'non_existing_file.yml'

    with pytest.raises(SystemExit):
        navigation_tree.load_tree_config_file(existing_navigation_path,
                                              non_existing_tree_config_filename)
