"""Tests of the NavigationTreeNode class"""

from lib.navigation_tree_node import NavigationTreeNode

def test_node_name():
    node_strings = [['Node Name', 'node-name'],
                    ['Node  Name', 'node-name'],
                    ['Node_Name', 'node_name'],
                    ['Node -Name', 'node-name'],
                    ['Node --Name', 'node-name'],
                    ['Node.Name', 'node.name'],
                    ['Node(Name)', 'node(name)'],
                    ['Node (Name)', 'node-(name)'],
                    ['   Node Name  ', 'node-name']]
    
    for node_string in node_strings:
       check_node_name(*node_string) 

def check_node_name(node_string, expected_name):
    node = NavigationTreeNode(node_string)
    assert node.options['id'] == expected_name

def test_node_name_and_stop_tag():
    node = NavigationTreeNode('node name @stop')
    assert node.name == 'node name'
    assert node.tags[0] == '@stop'
    assert node.options['stop']

def test_node_name_and_default_id_tag():
    node = NavigationTreeNode('  Node   Name  ')
    assert node.name == 'Node   Name'
    assert node.default_id == 'node-name'

def test_node_name_and_multiple_tags_with_default_values():
    node_strings = ['Node Name @stop @include @id',
                    'Node Name @stop   @include @id',
                    'Node Name  @stop @include  @id',
                    'Node Name @include @id @stop',
                    '   Node Name  @include @id @stop']
    
    for node_string in node_strings:
       check_node_name_and_multiple_tags_with_default_values(node_string) 

def check_node_name_and_multiple_tags_with_default_values(node_string):
    node = NavigationTreeNode(node_string)
    assert node.name == 'Node Name'
    assert node.default_id == 'node-name'
    assert node.options['stop']
    assert node.options['include'] == 'node-name'
    assert node.options['id'] == 'node-name'

def test_node_custome_id():
    node = NavigationTreeNode('Node Name @id=custom-node-name')
    assert node.options['id'] == 'custom-node-name'
