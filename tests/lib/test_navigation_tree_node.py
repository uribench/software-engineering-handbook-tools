"""Tests of the NavigationTreeNode class"""

import pytest
from lib.navigation_tree_node import NavigationTreeNode

@pytest.mark.parametrize('node_string, expected_name', [
    ('Node Name', 'node-name'),
    ('Node   Name', 'node-name'),
    ('  Node Name  ', 'node-name'),
    ('Node_Name', 'node_name'),
    ('Node -Name', 'node-name'),
    ('Node --Name', 'node-name'),
    ('Node.Name', 'node.name'),
    ('Node (Name)', 'node-(name)'),
    ('Node %#$Name=+*&', 'node-name'),
])
def test_default_id_tag(node_string, expected_name):
    node = NavigationTreeNode(node_string)
    assert node.options['id'] == expected_name

@pytest.mark.parametrize('node_string, expected_stop, expected_id, expected_include', [
    ('Node Name @stop', True, 'node-name', None),
    ('Node Name @stop @include @id', True, 'node-name', 'node-name'),
    ('Node Name @id @stop @include ', True, 'node-name', 'node-name'),
    ('Node Name @include @id', False, 'node-name', 'node-name'),
    ('Node Name', False, 'node-name', None),
    ('Node Name @stop @include @id=custom-id', True, 'custom-id', 'node-name'),
    ('Node Name @stop @include=custom-include @id', True, 'node-name', 'custom-include'),
])
def test_multiple_tags(node_string, expected_stop, expected_include, expected_id):
    node = NavigationTreeNode(node_string)
    assert node.options['stop'] == expected_stop
    assert node.options['id'] == expected_id
    if expected_include is not None:
        assert node.options['include'] == expected_include
