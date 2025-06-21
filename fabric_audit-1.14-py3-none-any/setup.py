from setuptools import setup, find_packages

setup(
    name="fabric_audit",
    version="1.14",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyarrow",
        "pyspark",
        "lxml",
        "azure-identity",
    ],
    author="Justin Leopold",
    author_email="justinaleopold@gmail.com",
    description="Fabric Audit is a Python package for auditing and validating data in the Fabric platform.",
    license="MIT",
)