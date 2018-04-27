from setuptools import (
    find_packages,
    setup,
)

setup(
    name='feed_conductor',
    version='0.2.0.dev1',
    description='feed conductor module',
    packages=find_packages(exclude=[]),
    author='ricequant',
    author_email='public@ricequant.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    install_requires=[
        'ipython',
        'sanic',
        'sanic-restful'
    ],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
    ],
)