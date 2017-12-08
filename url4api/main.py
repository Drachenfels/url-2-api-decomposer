"""Core of the package, contains only one function responsible for url
parsing/processing.
"""

from urllib.parse import urlparse

from . import exceptions, models


def split(url):
    """Function takes a url path and extracts from it version and base part.
    """
    parsed_url = urlparse(url)

    if parsed_url.scheme not in ('http', 'https'):
        raise exceptions.UnrecognisedProtocol(
            "Only http or https is ok with us")

    parts = parsed_url.path.split('/')

    try:
        version = float(parts[1])
    except (NameError, TypeError, ValueError):
        raise exceptions.InvalidUrlPattern(
            "Version has to be a float number.")

    try:
        base_url = str("/".join(parts[2:]))
    except (TypeError, exceptions.InvalidUrlPattern):
        raise exceptions.BadRouting(
            "Path is corrupted, dont know what to do with it")

    if parsed_url.params:
        base_url += ';' + parsed_url.params

    elif parsed_url.query:
        base_url += '?' + parsed_url.query

    elif parsed_url.fragment:
        base_url += '#' + parsed_url.fragment

    return models.ApiUrl(
        url=base_url,
        version=version,
        protocol=parsed_url.scheme,
        domain=parsed_url.hostname,
        port=parsed_url.port
    )
