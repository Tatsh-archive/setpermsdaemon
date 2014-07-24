from distutils.core import setup

setup(
    name='setpermsdaemon',
    version='0.1.7',
    author='Andrew Udvare',
    author_email='audvare@gmail.com',
    packages=['setpermsd'],
    url='https://github.com/Tatsh/setpermsdaemon',
    license='LICENSE.txt',
    description='Sets permissions on Linux automatically by listening to '
                'inotify create and modify events',
    long_description=open('README.rst').read(),
    scripts=['bin/setpermsd'],
)

print('This utility is deprecated/abandoned in favour of "better planning" (deployment, etc). Please do not use.')
