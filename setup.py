from setuptools import (
    find_packages,
    setup,
)

setup(
    name='sanic-blog',
    version='0.0.1.dev.1',
    description='feed conductor module',
    packages=find_packages(exclude=[]),
    author='ricequant',
    author_email='public@ricequant.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    install_requires=[
        'aiofiles',
        'aioredis',
        'aiosmtplib',
        'forgerypy',
        'gino',
        'ipython',
        'itsdangerous',
        'jinja2',
        'sanic',
        'sanic-restful',
        'whooshalchemy',
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "blog-manager = blog.manager:cli"
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
    ],
)
