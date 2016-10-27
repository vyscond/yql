from distutils.core import setup

setup(
    name='yql',
    version='0.1.0',
    description='yql wrapper',
    author='Ramon Moraes',
    author_email='vyscond@gmail.com',
    url='https://github.com/vyscond/yql',
    license='MIT',
    packages=['yql'],
    install_requires=[
        'requests>=2.11.1'
    ]
)
