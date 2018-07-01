"""
Represents a configuration navigation tree node.

A configuration navigation node is composed of a node name, optionally followed
by space-separated arguments as tags, each with the following syntax: @<key>[=<value>]

The supported keys are: 'id', 'include', and 'stop'.

The NavigationTreeNode also provides a public static method split_node_name_and_tags()
for direct use without instantiation.
"""

import sys
import re

class NavigationTreeNode:
    """Represents a configuration navigation tree node"""

    def __init__(self, node):
        """"""
        self.name, self.tags = self.split_node_name_and_tags(node)
        self.options = self._get_node_options(self.tags, self.name)
        self.default_id = self._node_name_to_node_default_id(self.name)

    @staticmethod
    def split_node_name_and_tags(node):
        """Split configuration navigation tree node into name and optional tags"""
        split_pattern = re.compile(r'^(?P<name>[^@]+)(?P<tags>.*)$')
        split_match = split_pattern.match(node)
        node_name = split_match.group('name').strip()
        node_tags = split_match.group('tags').strip().split(' ')

        return node_name, node_tags

    def _get_node_options(self, tags, name):
        """"""
        node_options = self._get_node_explicit_options(tags)
        node_options = self._set_node_default_options(node_options, name)

        return node_options

    @staticmethod
    def _get_node_explicit_options(tags):
        """"""
        # parse explicit arguments
        valid_keys = ['id', 'include', 'stop']
        node_options = {}
        options_pattern = re.compile(r'@(?P<k>[a-z]+)=?(?P<v>.*)')
        for tag in tags:
            options_match = options_pattern.match(tag)
            if options_match is None:
                continue
            if options_match.group('k') in valid_keys:
                node_options.update({options_match.group('k') : options_match.group('v')})
            else:
                print('Error: Unknown argument: {}'.format(options_match.group('k')))
                sys.exit()

        return node_options

    def _set_node_default_options(self, node_options, name):
        """"""
        # set defaults
        node_options['stop'] = True if 'stop' in node_options else False
        if 'id' not in node_options or node_options['id'] == '':
            node_options['id'] = self._node_name_to_node_default_id(name)
        if 'include' in node_options and node_options['include'] == '':
            node_options['include'] = self._node_name_to_node_default_id(name)

        return node_options

    @staticmethod
    def _node_name_to_node_default_id(name):
        """"""
        # remove invalid characters
        valid_chars_pattern = re.compile(r'[^\w\-. ()]+')
        name = valid_chars_pattern.sub('', name)

        # additional formatting
        name = re.sub(' ', '-', name)
        name = re.sub('-+', '-', name)

        return name.lower()
