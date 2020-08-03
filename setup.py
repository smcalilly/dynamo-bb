from setuptools import setup

setup(
    name='dynamo-bb',
    version='0.0.1',
    description='Baby wrapper classes for interfacing with DynamoDB',
    url='git@github.com:smcalilly/dynamo-bb.git',
    author='Sam McAlilly',
    author_email='smcalilly@gmail.com',
    license='unlicense',
    packages=['dynamo-bb'],
    install_requires=[
        'boto3'
    ],
    zip_safe=False
)