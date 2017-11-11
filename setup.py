"""Setup for pinteraction XBlock."""

import os

from setuptools import setup


# def find_package_data(pkg, roots):
#     """Generic function to find package_data.

#     All of the files under each of the `roots` will be declared as package
#     data for package `pkg`.

#     """
#     data = []
#     for root in roots:
#         for dirname, _, files in os.walk(os.path.join(pkg, root)):
#             for fname in files:
#                 data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

#     return {pkg: data}

def find_package_data(pkg, data_paths):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for data_path in data_paths:
        package_dir = pkg.replace(".", "/")
        for dirname, _, files in os.walk(package_dir + "/" + data_path):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), package_dir))
    return {pkg: data}


package_data=find_package_data("pinteraction", ["static", "public", "templates"])
print package_data

setup(
    name='pinteraction-xblock',
    version='0.1',
    description='pinteraction XBlock',   # TODO: write a better description.
    license='UNKNOWN',          # TODO: choose a license: 'AGPL v3' and 'Apache 2.0' are popular.
    packages=[
        'pinteraction',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'pinteraction = pinteraction.pinteraction:PatientInteractionXBlock',
            'response = pinteraction.pinteraction:PResponseXBlock',
        ]
    },
    package_data=package_data,
)
