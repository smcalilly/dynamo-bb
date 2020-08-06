from setuptools import setup

setup(
    name='dynamo-bb',
    version='0.0.12',
    description='Baby wrapper classes for interfacing with DynamoDB',
    url='git@github.com/smcalilly/dynamoBB.git',
    author='Sam McAlilly',
    author_email='smcalilly@gmail.com',
    license='unlicensed',
    packages=['dynamoBB'],
    install_requires=[
        'boto3'
    ],
    zip_safe=False
)