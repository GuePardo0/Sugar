from setuptools import setup

setup(
    name="sugar",
    version="0.1.0",
    py_modules=["sugar"],
    install_requires=[],
    author="Gustavo",
    author_email="gustavotimbo6@gmail.com",
    description="A sweet collection of Python utilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sugar",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)