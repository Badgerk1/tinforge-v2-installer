from setuptools import find_packages, setup

setup(
    name="tinforge-v2",
    version="2.1.0",
    description="TinForge v2 - Professional TIN generator",
    author="Badgerk1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "tinforge-v2=tinforge_v2.main:main",
        ],
    },
)
