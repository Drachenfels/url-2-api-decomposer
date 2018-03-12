from setuptools import setup


def readme():
    with open('README.rst') as fpl:
        return fpl.read()


setup(
    name='url2vapi',
    version='1.0',
    description=(
        'Tools extracts constant elements from url (for example version)'
    ),
    long_description=readme(),
    test_suite='nose.collector',
    tests_require=['nose'],
    url='https://github.com/Drachenfels/url2vapi',
    author="Drachenfels",
    author_email="drachu@gmail.com",
    license="MIT",
    packages=['url2vapi'],
    zip_safe=False
)
