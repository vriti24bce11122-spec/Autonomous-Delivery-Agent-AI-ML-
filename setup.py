from setuptools import setup, find_packages

setup(
    name="autonomous-delivery-agent",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.24.3",
        "matplotlib>=3.7.1",
        "networkx>=3.1",
        "click>=8.1.4"
    ],
    entry_points={
        "console_scripts": [
            "delivery-agent=main:cli",
        ],
    },
)
