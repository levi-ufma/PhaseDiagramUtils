from setuptools import setup, find_packages

def read(filename):
    return  [req.strip() for req in open(filename).readlines()]

setup(
    name="PhaseDiagramUtils",
    version="str",
    description="construções de gráficos",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read("requirements.txt"),
    extras_requires={
        "dev": read("requirements-dev.txt")
    }
)
