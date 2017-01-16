from setuptools import setup, find_packages

DESCRIPTION = 'Converts `google.appengine.ext.ndb.Model` into HTTP endpoints'
LONG_DESCRIPTION = """This project converts a `google.appengine.ext.ndb.Model`
into a HTTP endpoints. It provides validation, routing, documentation, and
CRUD server endpoints. Its purpose is to act as a "DSL" for Google App Engine,
allowing you to quickly write CRUD servers with just a `ndb.Model`."""

setup(
    name='gaend',
    version='1.0.0.dev4',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/samedhi/gaend',
    author='Stephen Cagle',
    author_email='samedhi@gmail.com',
    license='MIT',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7'],
    packages=find_packages(exclude=['tests']),
    install_requires=['Flask>=0.11',
                      'python-dateutil>=2.6'],
    include_package_data=True,
    zip_safe=False,
)
