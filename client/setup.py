from setuptools import setup, find_packages

setup(
    name="smokeager",
    version='0.0.1',
    author='Saurabh A.V.',
    author_email='saurabhav.torres@gmail.com',
    description="CLI for smokeager (smoke analytics).",
    packages=find_packages(),
    py_modules=['cli', 'scripts'],
    url="https://github.com/aliasav/smokeager",
    entry_points={
        'console_scripts': ['smokeager=cli:entry'],
               },    
)
