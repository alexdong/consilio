from setuptools import setup, find_packages

setup(
    name="consilio",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'better-exceptions',
        'prompt-toolkit',
        'anthropic',
        'pyyaml',
        'jinja2',
    ],
)
