from setuptools import setup, find_packages

setup(
    name="nanobot-sim",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pybullet>=3.2.5',
        'numpy>=1.21.0',
        'torch>=1.9.0',
        'gymnasium>=0.26.0',
        'matplotlib>=3.4.3',
        'scipy>=1.7.1',
    ]
)