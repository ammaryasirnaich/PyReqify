from setuptools import setup, find_packages

setup(
    name='pyreqify',
    version='0.1.0',
    description='A module to extract and package Python dependencies',
    author='Ammar Yasir Naich',
    author_email='ammar.naich@gmail.com',
    readme = "README.md",
    # license = {file = "LICENSE" },
    packages=find_packages(),
    install_requires=[
        'nbformat',
        'typing',
        # Add other dependencies here
    ],
    python_requires='>=3.6',  # Specify minimum Python version
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

