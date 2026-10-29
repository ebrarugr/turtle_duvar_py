from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'turtle_duvar_py'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ogrenci',
    maintainer_email='ogrenci@example.com',
    description='Duvardan kacan kaplumbaga: ROS 2 turtlesim duvar kontrolu',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'duvar_kontrol = turtle_duvar_py.duvar_kontrol:main',
        ],
    },
)
