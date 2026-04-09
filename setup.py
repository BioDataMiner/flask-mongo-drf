from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flask-mongo-rest",
    version="1.0.0",
    author="wangyunkai",
    author_email="yunkaiwang0901@gmail.com",
    description="Industrial Flask framework for building RESTful APIs with MongoDB, featuring automatic Swagger documentation and dependency injection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BioDataMiner/flask-mongo-rest",
    project_urls={
        "Bug Tracker": "https://github.com/BioDataMiner/flask-mongo-rest/issues",
        "Documentation": "https://flask-mongo-rest.readthedocs.io",
        "Source Code": "https://github.com/BioDataMiner/flask-mongo-rest",
    },
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    include_package_data=True,
    install_requires=[
        "flask>=2.0.0",
        "pymongo>=4.0.0",
        "flasgger>=0.9.5",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.9",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.7",
    keywords="flask mongodb rest api swagger openapi",
)
