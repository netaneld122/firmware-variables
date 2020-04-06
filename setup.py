from distutils.core import setup

setup(
    name='firmware_variables',
    version='0.0.1',
    description='Windows library for controlling UEFI firmware variables',
    author='netaneld122@github',
    packages=['firmware_variables'],
    package_dir={'': 'src'},
    install_requires=['pywin32'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Windows',
    ],
)
