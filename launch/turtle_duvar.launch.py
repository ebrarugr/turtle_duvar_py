"""Turtlesim penceresini ve duvar kontrol düğümünü birlikte başlatır."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen',
        ),
        Node(
            package='turtle_duvar_py',
            executable='duvar_kontrol',
            name='duvar_kontrol',
            output='screen',
            parameters=[{
                'hiz': 2.0,
                'alt_sinir': 1.0,
                'ust_sinir': 10.0,
            }],
        ),
    ])
