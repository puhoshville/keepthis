from setuptools import setup


version = "0.0.3"

install_requires = [
    'pymemcache>=2.2.2',
    'numpy>=1.17.0',
    'pandas>=0.25.0',
]


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='keepthis',
    version=version,
    author='Dmitrii Pukhov',
    author_email='pukhovdn@yandex.ru',
    description='KeepThis - data scientist helper, tool for caching artifacts which allow easily to share it with '
                'your teammates.',
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

