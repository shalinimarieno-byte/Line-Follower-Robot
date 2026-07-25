#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class RobustLineFollower(Node):
    def __init__(self):
        super().__init__('robust_line_follower')
        self.bridge = CvBridge()
        
        # Topic Subscriptions and Publishers
        self.image_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.get_logger().info('Line Follower Node Initialized & Running!')

    def image_callback(self, msg):
        try:
            # 1. Convert ROS Image to OpenCV Image
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'CvBridge Exception: {e}')
            return

        h, w, _ = frame.shape

        # 2. Crop Bottom Region (Floor Area ONLY)
        # Look at lower 35% of the camera view
        crop_bottom = frame[int(h * 0.65):h, 0:w]

        # 3. Convert BGR to HSV Color Space for accurate detection
        hsv = cv2.cvtColor(crop_bottom, cv2.COLOR_BGR2HSV)

        # 4. Black Color Range (Detect Black Line)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 120]) # Increased upper bound for better sensitivity

        mask = cv2.inRange(hsv, lower_black, upper_black)

        # 5. Calculate Center of Mass (Moments)
        M = cv2.moments(mask)
        twist = Twist()

        if M['m00'] > 500: # Threshold for valid detection
            # Find center X coordinate of the line
            cx = int(M['m10'] / M['m00'])
            
            # Distance between center of image and center of line
            error = cx - (w / 2)

            # Proportional Controller (P-Controller) for Steering
            twist.linear.x = 0.18 # Forward velocity
            twist.angular.z = -float(error) / 120.0 # Steering velocity

            self.get_logger().info(f'✅ Line Found! Centroid X: {cx} | Steering Angular Z: {twist.angular.z:.2f}')
        else:
            # Search mode: Slow rotation if line is not detected
            twist.linear.x = 0.05
            twist.angular.z = 0.3
            self.get_logger().warn('⚠️ Line Lost! Rotating to search...')

        # Publish Motor Commands
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = RobustLineFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()