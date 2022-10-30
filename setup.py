from setuptools import setup

KEYWORDS = 'python; cosmology; data analysis'

AUTHOR = 'Shi-Hui Zang'

AUTHOR_EMAIL = 'zangsh20@gmail.com'

URL = 'https://github.com/Zangshihui/StdRec'

LICENSE = 'MIT'

DATA_FILES = ''

with open('requirements.txt', 'r') as fh:
    dependencies = [l.strip() for l in fh]
    
setup(
    name='StdRec',
    version='0.1',
    description='A Python package for perform standard reconstruction.',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language ::Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=['StdRec'],
    install_requires=dependencies,
    setup_requires=['cython>0.25', 'setuptools>=18.0'],
    test_suite='tests',
)