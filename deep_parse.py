#!/usr/bin/env python

"""Simple library for parsing deeply nested structure (dict, json)
into regular object. You can specify fields to extract, and argument
names in created object.
Example

    content = {
        'name': 'Bob',
        'details': {
            'email': 'bob@email.com',
        }
    }
    fields = (
        ('name', ),
        ('details__email', 'details_email')
    )
    item = deep_parse_dict(content, fields)
    assert item.name == 'Bob'
    assert item.details_email == 'bob@email.com'

"""


class DeepParseObject(object):
    """Simple dummy object to hold content."""

    def __str__(self):
        return 'DeepParseObject: %s' % self.__dict__

    def __repr__(self):
        return 'DeepParseObject: %r' % self.__dict__


def deep_parse_dict(content, fields, exc_class=Exception, separator='__'):
    """Extracting fields specified in ``fields`` from ``content``."""
    deep_parse = DeepParseObject()
    for field in fields:
        try:
            lookup_name, store_name = field[0], field[0]
            if len(field) > 1:
                lookup_name, store_name = field
            parts = lookup_name.split(separator)
            value = content
            for part in parts:
                value = value[part]
            setattr(deep_parse, store_name, value)
        except Exception as original_exc:
            exc = exc_class('Error parsing field %s' % repr(field))
            exc.error_field = field
            exc.original_exc = original_exc
            raise exc
    return deep_parse
