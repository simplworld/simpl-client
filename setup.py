import os
from setuptools import setup, find_packages

VERSION = '0.1.3'


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='simpl_client',
    version=VERSION,
    description='',
    long_description=readme,
    author='',
    author_email='',
    url='https://gitlab.com/lldev-team/simpl-client',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    install_requires=[
        "genericclient==0.0.15",
    ],
    test_suite='nose.collector',
    tests_require=[
        "responses==0.5.1",
        "nose==1.3.7",
    ]
)
