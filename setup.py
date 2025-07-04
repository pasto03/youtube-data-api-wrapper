import pkg_resources
from setuptools import setup, find_packages
import os

setup(
    name="youtube_data_api",  # Name of the module
    version="1.1.0",  # Version of your package
    description="a Python library that simplifies interactions with the YouTube Data API",
    author="Ben Law",
    author_email="chumaolaw@gmail.com",
    url="https://github.com/pasto03/youtube-data-api-wrapper.git",  # GitHub repo URL
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
)
