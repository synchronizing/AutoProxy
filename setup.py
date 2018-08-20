import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "AutoProxy",
    version = "1.0.0",
    packages = find_packages(),
    author = "Felipe Faria",
    author_email = "felipefaria@me.com",
    description="Asynchronously gather and check proxies from TheBigProxyList.com",
    license = "MIT",
    keywords = "proxy thebigproxylist asynchronous gatherer proxies",
    url = "https://github.com/synchronizing/autoproxy",
    long_description=read('README.md'),
    project_urls={
        "Home": "https://github.com/synchronizing/autoproxy",
    }
)
