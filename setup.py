from setuptools import setup

setup(
   name='SnowStorm',
   version='1.0',
   description='An audio streaming tool built to make running internet radio stations easy',
   url='https://github.com/chance-nelson/SnowStorm',
   author='Chance Nelson',
   author_email='chance-nelson@nau.edu',
   classifiers=[
       'License :: OSI Approved :: MIT License',
   ],
   keywords=['internet', 'radio'],
   packages=['stream', 'api'],
   install_requires=[
       'Click==7.0',
       'Flask==1.1.1',
       'Flask-Cors==3.0.8',
       'itsdangerous==1.1.0',
       'Jinja2==2.10.1',
       'MarkupSafe==1.1.1',
       'mutagen==1.42.0',
       'six==1.12.0',
       'Werkzeug==0.16.0'
    ], #external packages as dependencies
)