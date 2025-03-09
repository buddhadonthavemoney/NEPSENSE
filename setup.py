from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nepsense',
    version='0.0.4',
    author='Buddha Gautam',
    author_email='buddhagautam231@gmail.com',
    url='https://github.com/buddha231/NEPSENSE',
    description='Complete NepalStock solution in command line',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['nepsense'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    keywords='nepsense nepalstock stonk buddha python package buddha69',
    install_requires=[
        'nepse @ git+https://github.com/basic-bgnr/NepseUnofficialApi.git',
        'tabulate>=0.9.0',
        'colorama>=0.4.6',
        'pandas>=2.0.0'
    ],
    entry_points={
        'console_scripts': [
            'priceof=nepsense.cli:main',
        ],
    },
)
