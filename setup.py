import os
from setuptools import setup, find_packages

VERSION = '0.8.1'


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='simpl_client',
    version=VERSION,
    description='Python clients for accessing simpl-games-api',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='',
    author_email='',
    url='https://github.com/simplworld/simpl-client',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    install_requires=[
        "genericclient-aiohttp>=1.4.2,<1.5",
        "genericclient>=1.4.2,<1.5",
    ],
    setup_requires=[
        "pytest-runner",
    ],
    test_suite='tests',
    tests_require=[
        "mocket",
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
    ]
)
