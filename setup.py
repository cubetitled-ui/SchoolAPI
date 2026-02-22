import setuptools
import io

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
  
setuptools.setup(
    name="SchoolAPI",
    version="1.0b0",
    author="DavidZhivaev",
    author_email="zhivaevda.dev@gmail.com",
    description="Библиотека для удобной разработки проектов, связанных с МЭШ.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
