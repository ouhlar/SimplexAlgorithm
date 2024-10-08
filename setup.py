from setuptools import setup


setup(
    name="LinOpt",
    version="0.0.1",
    description="linear optimization",
    author="Oliver Uhlar",
    author_email="ouhlar@studen.umb.sk",
    url="https://github.com/duchzjety/LinOpt",
    py_modules=['rational_number', 'vector', 'matrix', 'simplex_method'],
    package_dir={'': 'src'},
    install_requires=[
        'prettytable==3.5.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Education"
    ]
)
