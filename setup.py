from setuptools import setup, find_packages

import tinyblog

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
        'django-setuptest==0.1.3',
        'factory_boy==1.3.0',
        'mock==1.0.1',
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
)
