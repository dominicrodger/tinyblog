import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import tinyblog


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='tinyblog',
    version=tinyblog.__version__,
    description='A Django app for a very simple blog.',
    long_description=open('README.rst').read(),
    author='Dominic Rodger',
    url='https://github.com/dominicrodger/tinyblog/',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.4',
        'requests==1.2.0',
        'django-tinymce==1.5.1b4',
        'django-uuidfield==0.4.0',
        'bleach==1.2.2',
    ],
    tests_require=[
        "pytest==2.6.4",
        "pytest-cov==1.7.0",
        "pytest-django==2.6.2",
        'factory_boy==1.3.0',
        'feedparser==5.1.3',
        'mock==1.0.1',
    ],
    cmdclass = {'test': PyTest},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
)
