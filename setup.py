from setuptools import setup, find_packages

setup(
    name='Racing Game',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/paichiwo/racing_pygame',
    license='MIT',
    author='Lukasz Zerucha',
    author_email='lzerucha@gmail.com',
    description='Retro-style racing game',
    install_requires=['pygame']
)