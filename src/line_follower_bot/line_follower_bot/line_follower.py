#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class SeekAndFollowLine(Node):
    def __init__(self):
        super().__init__('line_follower_node')
        self.bridge = CvBridge()
        
        self.image_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.get_logger().info('Line Seeker & Follower Active!')

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'CvBridge Error: {e}')
            return

        h, w, _ = frame.shape

        # Crop bottom region for line detection
        crop = frame[int(h * 0.5):h, 0:w]
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

        # Strict Black Line Filter
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 60])

        mask = cv2.inRange(hsv, lower_black, upper_black)
        M = cv2.moments(mask)
        twist = Twist()

        if M['m00'] > 200: # Line found!
            cx = int(M['m10'] / M['m00'])
            error = cx - (w / 2)

            # Move forward & steer towards line center
            twist.linear.x = 0.15
            twist.angular.z = -float(error) / 90.0
            self.get_logger().info(f'🎯 Line Detected! Moving towards track | Steering: {twist.angular.z:.2f}')
        else:
            # SEEK MODE: Move forward slowly & turn to find line
            twist.linear.x = 0.10
            twist.angular.z = 0.35
            self.get_logger().warn('🔍 Searching for Black Line... Moving towards track')

        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = SeekAndFollowLine()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()