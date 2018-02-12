from setuptools import setup

setup(
    name='flashlight',
    description='The Visualization Tool For ONNX',
    long_description=open('README.rst').read(),
    version='0.1.0',
    author='Sherin Thomas (hhsecond), Nisheet Verma (nisheetsun)',
    author_email='sherinct@live.com, nisheetsun@gmail.com',
    url='https://github.com/dlguys/flashlight',
    license="MIT",
    packages=['flashlight', 'flashlight/backend', 'flashlight/client'],
    package_data={'flashlight': ['flashlight/frontend/build/*']},
    include_package_data=True,
    keywords='pytorch visualization onnx',
    install_requires=['sanic==0.7.0'],
    entry_points={
        'console_scripts': ['flashlight = flashlight.backend.server:run']},)
