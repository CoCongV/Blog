# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# README.rst
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os.path import dirname, join
try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

from setuptools import (
    find_packages,
    setup,
    Extension
)

with open(join(dirname(__file__), 'blog/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='flask_blog',
    version=version,
    description='',
    packages=find_packages(exclude=[]),
    author='ricequant',
    author_email='public@ricequant.com',
    license='Apache License v2',
    package_data={
        '': ['*.*'],
        'rqpro_api_server': [
            'fonts/*',
            'migrations/versions/*',
            'pem/*',
            'server/static/*',
            'server/static/img/*',
            'server/static/css/*',
            'server/static/js/*',
            'server/templates/admin/*',
            'server/templates/admin/account/*',
            'server/templates/admin/booking/*',
            'server/templates/admin/license/*',
            'server/templates/admin/modals/*',
            'server/templates/admin/trade/*',
            'server/templates/admin/user/*',
            'server/templates/security/*',
            'server/templates/*',
            'views/*'
        ]
    },
    install_requires=[
        str(ir.req)
        for ir in parse_requirements("requirements.txt", session=False)
    ],
    zip_safe=False,
    ext_modules=ext_modules,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
