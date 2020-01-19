from setuptools import setup


version = "0.0.4"

install_requires = [
    'pymemcache>=3.0.0',
    'numpy>=1.18.1',
    'pandas>=0.25.3',
]


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='keepthis',
    version=version,
    author='Dmitrii Pukhov',
    author_email='pukhovdn@yandex.ru',
    description='KeepThis - helper tool for Data Scientists collaborative work. '
                'Cache artifacts and share them with your teammates.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/puhoshville/keep-this",
    packages=['keepthis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    license='MIT',
)

