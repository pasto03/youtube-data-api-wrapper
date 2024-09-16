from setuptools import setup, find_packages

setup(
    name="youtube_data_api",  # Name of the module
    version="0.1",  # Version of your package
    description="a Python library that simplifies interactions with the YouTube Data API",
    author="Ben Law",
    author_email="chumaolaw@gmail.com",
    url="https://github.com/pasto03/youtube-data-api-wrapper.git",  # GitHub repo URL
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[],  # External packages that are required for this package (optional)
)
