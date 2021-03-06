from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'pytz==2020.1',
    'requests==2.24.0'
]

TEST_REQUIRES = [
    # testing and coverage
    'pytest', 'coverage', 'pytest-cov',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="wealthaccess",
    version="0.0.1",
    author="Doug Guthrie",
    author_email="douglas.p.guthrie@gmail.com",
    description="Python wrapper for the Wealth Access API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    url="https://github.com/dpguthrie/wealthaccess",
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'test': TEST_REQUIRES + INSTALL_REQUIRES,
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Intended Audience :: Financial and Insurance Industry",
        "Operating System :: OS Independent"
    ],
    keywords='finance, financial planning, wealth management, api, api-wrapper'
)