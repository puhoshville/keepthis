from setuptools import setup


version = "0.0.1"

install_requires = [
    'pymemcache==2.2.2',
    'numpy==1.17.0',
    'pandas==0.25.0',
]

setup(
    name='keepthis',
    version=version,
    packages=[''],
    install_requires=install_requires,
    url='github.com/puhoshville',
    license='MIT',
    author='Dmitrii Pukhov',
    author_email='pukhovdn@yandex.ru',
    description='KeepThis - data scientist helper, tool for caching artifacts which allow easily to share it with '
                'your teammates.'
)
