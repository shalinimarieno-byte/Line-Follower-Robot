import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_dir = get_package_share_directory('line_follower_bot')
    world_path = os.path.join(pkg_dir, 'worlds', 'line_track.sdf')
    urdf_path = os.path.join(pkg_dir, 'urdf', 'line_bot.urdf.xacro')

    doc = xacro.parse(open(urdf_path))
    xacro.process_doc(doc)
    robot_description = {'robot_description': doc.toxml()}

    # 1. Robot State Publisher
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # 2. Gazebo Simulator
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

   # 3. Spawn Line Bot DIRECTLY ON THE BLACK LINE
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-string', doc.toxml(), '-name', 'line_bot', '-x', '0.5', '-y', '0.0', '-z', '0.05', '-Y', '0.0'],
        output='screen'
    )

    # 4. Universal Dual Direction ROS-GZ Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image'
        ],
        output='screen'
    )

    # 5. RQT Image Camera Viewer
    rqt_cam = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        arguments=['/camera/image_raw'],
        output='screen'
    )

    return LaunchDescription([rsp, gazebo, spawn, bridge, rqt_cam])