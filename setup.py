"""Setup script for cmsplugin_zinnia"""
from setuptools import setup
from setuptools import find_packages

import cmsplugin_zinnia

setup(
    name='cmsplugin_zinnia',
    version=cmsplugin_zinnia.__version__,

    description='Django-CMS plugins for django-blog-zinnia',
    long_description=open('README.rst').read(),

    keywords='django, blog, weblog, zinnia, cms, plugins, apphook',

    author=cmsplugin_zinnia.__author__,
    author_email=cmsplugin_zinnia.__email__,
    url=cmsplugin_zinnia.__url__,

    packages=find_packages(exclude=['demo_cmsplugin_zinnia']),
    classifiers=[
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'],

    license=cmsplugin_zinnia.__license__,
    include_package_data=True,
    zip_safe=False
)
