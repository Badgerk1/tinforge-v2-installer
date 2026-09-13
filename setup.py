from setuptools import find_packages, setup

setup(
    name="tinforge-v2-installer",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
)
