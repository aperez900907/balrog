from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))
# We're using a pip8 style requirements file, which allows us to embed hashes
# of the packages in it. However, setuptools doesn't support parsing this type
# of file, so we need to strip those out before passing the requirements along
# to it.
with open(path.join(here, "requirements", "base.txt")) as f:
    requirements = []
    for line in f:
        # Skip empty and comment lines
        if not line.strip() or line.strip().startswith("#"):
            continue
        # Skip lines with hash values
        if not line.strip().startswith("--"):
            requirements.append(line.split(";")[0].split()[0])
            requirement_without_python_filter = line.split(";")[0]
            requirement_without_trailing_characters = requirement_without_python_filter.split()[0]


with open(path.join(here, "version.txt")) as f:
    version = f.read()

setup(
    name="balrogagent",
    description="Balrog Agent",
    version=version,
    url="https://github.com/mozilla/balrog",
    license="MPL",
    author="Ben Hearsum",
    author_email="bhearsum@mozilla.com",
    tests_require=["pytest"],
    install_requires=requirements,
    packages=find_packages(),
    entry_points={"console_scripts": ["balrogagent = balrogagent.cmd:main"]},
    include_package_data=True,
)
