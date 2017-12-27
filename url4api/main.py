"""Core of the package, contains only one function responsible for url
parsing/processing.
"""

import re

from urllib.parse import urlparse

from . import exceptions, models


def parse_pattern(pattern):
    cast_types = {
        'number': lambda val: int(float(val)),
        'double': float,
        'string': str,
        'bool': bool,
    }

    if not pattern:
        raise exceptions.InvalidInputPattern("Pattern cannot be empty")

    elements = re.findall(r'<([\w\.]+)(:(\w+))?>', pattern)

    groups = []

    for (element, separator, item_type) in elements:
        if not item_type:
            item_type = 'string'

        if item_type not in cast_types:
            raise exceptions.InvalidInputPattern(
                "There is unrecognised item type ({}) for element {}".format(
                    item_type, element))

        if (element, item_type) in groups:
            raise exceptions.InvalidInputPattern(
                "Element ({}) present twice on a pattern".format(element))

        del separator

        groups.append((element, cast_types[item_type]))

    return groups


def split(url, pattern=None):
    """Function takes a string and parses it into restful api relevant chunks.

    Second argument is optional. It allows to predefine that given url has to
    have certain structure. For example we can enforce that version or
    namespace is present. If not provided it will default to:

        <version:double>/<rest_of_url>

    Pattern consists of backslash separated groups. Each group member needs to
    be defined as:

        <name>

    or

        <name:type>

    Where type can be number, double, string or bool (default: string).
    """
    if pattern is None:
        pattern = '<...>'

    parsed_url = urlparse(url)

    if parsed_url.scheme not in ('http', 'https'):
        raise exceptions.UnrecognisedProtocol(
            "Only http or https is ok with us")

    groups = parse_pattern(pattern)

    url = parsed_url.path

    if url.startswith('/'):
        url = url[1:]

    kwargs = {}

    while url:
        if not groups:
            break

        name, cast_to = groups.pop(0)

        idx = url.find('/')

        if name == '...':
            if groups:
                raise exceptions.InvalidInputPattern(
                    "Argpars <...> cannot be followed by any other group")

            value = url
            url = ''
            name = 'url'

        else:
            value = url[:idx]
            url = url[idx + 1:]

            try:
                value = cast_to(value)
            except (NameError, TypeError, ValueError):
                raise exceptions.InvalidUrlPattern(
                    "Unable to cast value ({}) using ({})".format(
                        value, cast_to))

        kwargs[name] = value

    if parsed_url.params:
        kwargs['url'] += ';' + parsed_url.params

    elif parsed_url.query:
        kwargs['url'] += '?' + parsed_url.query

    elif parsed_url.fragment:
        kwargs['url'] += '#' + parsed_url.fragment

    return models.ApiUrl(
        protocol=parsed_url.scheme,
        domain=parsed_url.hostname,
        port=parsed_url.port,
        url=kwargs.pop('url') if 'url' in kwargs else '',
        **kwargs
    )
