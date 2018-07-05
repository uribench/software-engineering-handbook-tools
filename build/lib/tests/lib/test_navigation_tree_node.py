"""Tests of the NavigationTreeNode class"""

import pytest
from handbook_tools.lib.navigation_tree_node import NavigationTreeNode

def get_id(node_name):
    return NavigationTreeNode(node_name).options['id']

def test_trims_spaces():
    assert get_id('  Node  Name  ') == 'node-name'

def test_removes_consecutive_dashes():
    assert get_id('Node --Name') == 'node-name'

def test_removes_special_characters():
    assert get_id('Node %#$Name=+*&') == 'node-name'

def test_preserves_valid_characters():
    assert get_id('Node._(Name)') == 'node._(name)'

@pytest.mark.parametrize('node_string, expected_stop, expected_id, expected_include', [
    ('Node Name @stop', True, 'node-name', None),
    ('Node Name @stop @include @id', True, 'node-name', 'node-name'),
    ('Node Name @id @stop @include ', True, 'node-name', 'node-name'),
    ('Node Name @include @id', False, 'node-name', 'node-name'),
    ('Node Name', False, 'node-name', None),
    ('Node Name @stop @include @id=custom-id', True, 'custom-id', 'node-name'),
    ('Node Name @stop @include=custom-include @id', True, 'node-name', 'custom-include'),
])
def test_sets_multiple_tags(node_string, expected_stop, expected_include, expected_id):
    node = NavigationTreeNode(node_string)
    assert node.options['stop'] == expected_stop
    assert node.options['id'] == expected_id
    if expected_include is not None:
        assert node.options['include'] == expected_include
