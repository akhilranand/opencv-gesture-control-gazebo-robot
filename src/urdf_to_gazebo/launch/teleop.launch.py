from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    teleop = Node(
        package='urdf_to_gazebo',
        executable='teleop_node',
        name='teleop_node',
        # output='screen'
    )

    return LaunchDescription([
        teleop
    ])
