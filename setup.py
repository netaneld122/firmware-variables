from setuptools import setup

setup(
    name='firmware_variables',
    version='0.0.4',
    description='Windows library for controlling UEFI firmware variables',
    author='Netanel Dziubov',
    packages=['firmware_variables'],
    package_dir={'': 'src'},
    install_requires=['pywin32', 'aenum'],
    url="https://github.com/netaneld122/firmware-variables",
    python_requires='>=2.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
)
