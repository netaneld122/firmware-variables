from setuptools import setup

setup(
    name='firmware_variables',
    version='0.0.1',
    description='Windows library for controlling UEFI firmware variables',
    author='Netanel Dziubov',
    packages=['firmware_variables'],
    package_dir={'': 'src'},
    install_requires=['pywin32'],
    url="https://github.com/netaneld122/firmware-variables",
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
)
