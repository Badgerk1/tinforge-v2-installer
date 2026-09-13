from setuptools import find_packages, setup

setup(
    name="tinforge-v2-installer",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={
        "tinforge_v2": ["assets/*.qrc", "assets/icons/*.ico", "assets/icons/*.png"],
        "tinforge_v2.gui.styles": ["*.qss"],
    },
)
