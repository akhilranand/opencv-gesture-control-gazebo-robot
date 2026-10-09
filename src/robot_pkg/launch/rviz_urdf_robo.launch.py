# from launch import LaunchDescription
# from launch_ros.actions import Node
# from ament_index_python.packages import get_package_share_directory
# import os

# def generate_launch_description():


#     package_path = get_package_share_directory('robot_pkg')

#     urdf_path = os.path.join(package_path,'urdf','my_robo.urdf')

#     with open(urdf_path, 'r') as file:
#         robot_description = file.read()


        

#     robt_state_publisher = Node(
#         package="robot_state_publisher",
#         executable="robot_state_publisher", 
#         parameters=[
#             {"robot_description":robot_description}
#         ]
#     )    

#     joint_state_publisher = Node(
#         package="joint_state_publisher_gui",
#         executable="joint_state_publisher_gui"
#     )

#     rviz = Node(
#         package="rviz2",
#         executable="rviz2",
#     )

#     return LaunchDescription([
#         robt_state_publisher,
#         joint_state_publisher,
#         rviz
#     ])


from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
import os


def generate_launch_description():

    package_path = get_package_share_directory('robot_pkg')

    urdf_path = os.path.join(
        package_path,
        'urdf',
        'my_robo.urdf'
    )

    with open(urdf_path, 'r') as file:
        robot_description = file.read()


    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        )
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {"robot_description": robot_description}
        ]
    )


    joint_state_publisher = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )


    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )


    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity',
            'diff_robo',
            '-topic',
            'robot_description'
        ],
        output='screen'
    )


    rviz = Node(
        package="rviz2",
        executable="rviz2"
    )


    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher,
        gazebo,
        spawn_robot,
        rviz
    ])