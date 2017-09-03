from setuptools import setup

v = '1.1.0'

setup(
    name='grammpy-transforms',
    version=v,
    packages=['grammpy_transforms',
              'grammpy_transforms.ChomskyForm', 'grammpy_transforms.UnitRulesRemove',
              'grammpy_transforms.EpsilonRulesRemove', 'grammpy_transforms.UnreachableSymbolsRemove',
              'grammpy_transforms.NongeneratingSymbolsRemove'],
    url='https://github.com/PatrikValkovic/grammpy-transforms',
    download_url='https://github.com/PatrikValkovic/grammpy-transforms/archive/v' + v + '.tar.gz',
    license='GNU General Public License v3.0',
    author='Patrik Valkovic',
    author_email='patrik.valkovic@hotmail.cz',
    description='Set of transformations for grammpy library.',
    install_requires=[
        'grammpy',
    ],
)
