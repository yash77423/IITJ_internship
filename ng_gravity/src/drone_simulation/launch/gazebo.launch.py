from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_sim = get_package_share_directory('drone_simulation')

    world = os.path.join(pkg_sim, 'worlds', 'narrow_gap.sdf')
    model_sdf = os.path.join(pkg_sim, 'models', 'drone_description', 'model.sdf')

    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', world, '-r'],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/camera@sensor_msgs/msg/Image[ignition.msgs.Image'],
        output='screen'
    )

    rqt_image = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        name='rqt_image_view',
        arguments=['/camera']
    )

    return LaunchDescription([
        gazebo,
        bridge,
        rqt_image
    ])
