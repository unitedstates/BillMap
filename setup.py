import setuptools

with open("README.adoc", "r") as fh:
    long_description = fh.read() 

import re
VERSIONFILE="_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setuptools.setup(
    name="flatgov-aih", 
    version=verstr,
    author="Ari Hershowitz",
    author_email="arihershowitz@gmail.com",
    description="Modules for the Flatgov Project",
    long_description=long_description,
    long_description_content_type="text/asciidoc",
    url="https://github.com/aih/FlatGov",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "elasticsearch==7.9.1", "lxml==4.6.3", "asgiref==3.2.10", "Django==3.1.6", "iteration-utilities==0.11.0",
        "pytz==2020.1", "sqlparse==0.3.1", "python-dotenv==0.15.0", "uwsgi==2.0.19.1", "scrapy==2.4.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ["flatgov-scripts"]
    ],
    python_requires='>=3.7',
)