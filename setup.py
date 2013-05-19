from setuptools import setup, find_packages

import tinyblog

setup(
    name='tinyblog',
    version=tinyblog.__version__,
    description='A Django app for a very simple blog.',
    long_description=open('README.md').read(),
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='https://bitbucket.org/dominicrodger/tinyblog',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django',
        'requests==1.2.0',
        'django-tinymce==1.5.1b4',
        'django-uuidfield==0.4.0',
    ],
    tests_require=[
        'django-setuptest==0.1.2',
        'factory_boy==1.3.0'
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',
)
