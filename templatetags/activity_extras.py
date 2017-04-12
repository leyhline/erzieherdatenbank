"""
Created on Apr 11, 2017

:copyright: (c) 2017 by Thomas Leyh.
"""

import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()
RE_HASHTAG = re.compile(r"""(?P<hash>#)(?P<name>\w+)""")


def replace_with_hyperlink(match_object):
    """
    Returns the fitting html hyperlink for the given match object.
    :param match_object: Hashtag match object.
    :returns: A string: <a href="url/to/match">#match</>
    """
    hash, tag = match_object.groups()
    return "<a href=\"{}\">{}{}</a>".format(tag.lower(), hash, tag)


@register.filter(needs_autoescape=True)
@stringfilter
def hashtagger(value, autoescape=True):
    """
    Convert Hashtags to hyperlinks and return whole string.
    :param value: A string for inserting hyperlinks
    :param autoescape: Does value need escaping?
    :return: Safe string with hyperlinks.
    """
    if autoescape:
        value = conditional_escape(value)
    value = RE_HASHTAG.sub(replace_with_hyperlink, value)
    return mark_safe(value)
