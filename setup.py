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
        "PyQt5==5.15.9",
        "PyQt5-sip==12.13.0",
        "requests>=2.32.0,<3.0",
    ],
    entry_points={
        "console_scripts": [
            "tinforge-v2=tinforge_v2.main:main",
        ],
    },
)
