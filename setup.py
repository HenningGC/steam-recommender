from setuptools import setup, find_packages
from pathlib import Path

# version
here = Path(__file__).absolute().parent
version_data = {}
with open(here.joinpath("engine-lib", "__init__.py"), "r") as f:
    exec(f.read(), version_data)
version = version_data.get("__version__", "0.0")

install_requires = [
    "numpy>=1.19",  # 1.19 required by tensorflow 2.6
    "pandas>1.0.3,<2",
    "ipykernel>=4.6.1,<7",
    "jupyter>=1,<2",
    "aiohttp>=3.7.4,<4",
    "asyncio>=3.4.3,<4",
    "requests>=2.25.1,<3",
    "csv>=1.0,<2",
    "re=>2.2.1,<3",
]

setup(
    name="engine-lib",
    version=version,
    install_requires=install_requires,
    package_dir={"enginelib": "enginelib"},
    python_requires=">=3.6, <3.10",
    packages=find_packages(where=".", exclude=["docs", "examples", "tests"]),
)
