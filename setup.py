from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mm_cargo/__init__.py
from mm_cargo import __version__ as version

setup(
	name="mm_cargo",
	version=version,
	description="Transport Management",
	author="dexciss",
	author_email="info@dexciss.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
