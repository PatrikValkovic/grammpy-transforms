from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

v = '1.2.5'

setup(
    name='grammpy-transforms',
    version=v,
    packages=[
        'grammpy_transforms',
        'grammpy_transforms.ChomskyForm',
        'grammpy_transforms.UnitRulesRemove',
        'grammpy_transforms.EpsilonRulesRemove',
        'grammpy_transforms.UnreachableSymbolsRemove',
        'grammpy_transforms.NongeneratingSymbolsRemove',
        'grammpy_transforms.SplittedRules'
    ],
    url='https://github.com/PatrikValkovic/grammpy-transforms',
    download_url='https://github.com/PatrikValkovic/grammpy-transforms/archive/v' + v + '.tar.gz',
    license='GNU General Public License v3.0',
    author='Patrik Valkovic',
    author_email='patrik.valkovic@hotmail.cz',
    description='Set of transformations for grammpy library.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'grammpy',
    ],
)
