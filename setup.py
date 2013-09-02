import os
from setuptools import setup, find_packages

from sentry_mailagain import __version__, __author__


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fobj:
            return fobj.read()
    except IOError:
        return ''


install_requires = read('requirements.txt').splitlines()


setup(
    name='sentry-mailagain',
    version=__version__,
    url='https://github.com/simonpercivall/sentry-mailagain',
    license='BSD',
    author=__author__,
    author_email='simon.percivall@trioptima.com',
    description='A Sentry plugin that renotifies you of unresolved events',
    long_description=read('README.rst'),

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'sentry.apps': [
            'sentry_mailagain = sentry_mailagain',
        ],
        'sentry.plugins': [
            'sentry_mailagain = sentry_mailagain.plugin:MailAgainPlugin',
        ]
    },
    
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins'
    ]
)
