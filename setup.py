from setuptools import setup

setup(
    name='doun',
    version='0.1',
    author="Dounya Goumeri",
    author_eamil="goumeri@hotitem.nl",
    Description="doun is a tool to manage AWS EC2 snapshots",
    packages=['brian'],
    url="https://github.com/dgoumeri/AWS_repository",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        brian=brian.brian:cli
        ''',
)
## pipenv run python setup.py bdist_wheel - command prompt
## pip3 install dist/doun
## brian instances list
