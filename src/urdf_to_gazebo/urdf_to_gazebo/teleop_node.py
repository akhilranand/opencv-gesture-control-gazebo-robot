import math
import cv2
import numpy as np

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Int32


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


class FingerTeleopNode(Node):

    def __init__(self):
        super().__init__("finger_teleop")

        # Parameters
        self.declare_parameter("camera_index", 0)
        self.declare_parameter("roi", [350, 50, 600, 300])
        self.declare_parameter("show_windows", True)

        cam_idx = self.get_parameter("camera_index").value

        self.x1, self.y1, self.x2, self.y2 = \
            self.get_parameter("roi").value

        self.show = self.get_parameter("show_windows").value

        # Open camera
        self.cap = cv2.VideoCapture(cam_idx)

        if not self.cap.isOpened():
            self.get_logger().error(
                f"Cannot open camera {cam_idx}"
            )
            return

        # Publish finger count
        self.finger_pub = self.create_publisher(
            Int32,
            "finger_count",
            10
        )

        # Publish robot velocity
        self.cmd_pub = self.create_publisher(
            Twist,
            "/cmd_vel",
            10
        )

        # Robot speed
        self.speed = 0.5
        self.turn = 1.0

        self.previous_fingers = -1

        # 30 FPS
        self.timer = self.create_timer(
            1.0 / 30.0,
            self.process_frame
        )

        self.get_logger().info(
            "OpenCV Finger Teleop Started"
        )

        self.get_logger().info(
            "0 = STOP | 1 = FORWARD | 2 = LEFT"
        )

        self.get_logger().info(
            "3 = RIGHT | 4 = BACKWARD | 5 = STOP"
        )

    def process_frame(self):

        x1, y1, x2, y2 = (
            self.x1,
            self.y1,
            self.x2,
            self.y2
        )

        # Read camera
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warn(
                "Failed to read camera frame"
            )
            return

        # Mirror camera
        frame = cv2.flip(frame, 1)

        # Draw ROI
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # Crop ROI
        roi = frame[y1:y2, x1:x2]

        # Convert BGR to HSV
        hsv = cv2.cvtColor(
            roi,
            cv2.COLOR_BGR2HSV
        )

        # Skin color mask
        mask = cv2.inRange(
            hsv,
            np.array([0, 30, 60]),
            np.array([20, 150, 255])
        )

        # Remove noise
        mask = cv2.dilate(
            mask,
            np.ones((3, 3), np.uint8),
            iterations=2
        )

        mask = cv2.GaussianBlur(
            mask,
            (5, 5),
            0
        )

        fingers = 0

        # Find contours
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:

            # Get largest contour
            cnt = max(
                contours,
                key=cv2.contourArea
            )

            # Ignore small contours
            if cv2.contourArea(cnt) > 3000:

                # Convex hull
                hull_pts = cv2.convexHull(cnt)

                cv2.drawContours(
                    roi,
                    [cnt],
                    -1,
                    (255, 0, 0),
                    2
                )

                cv2.drawContours(
                    roi,
                    [hull_pts],
                    -1,
                    (0, 255, 255),
                    2
                )

                # Hull indices
                hull_idx = cv2.convexHull(
                    cnt,
                    returnPoints=False
                )

                # Convexity defects
                defects = cv2.convexityDefects(
                    cnt,
                    hull_idx
                )

                gaps = 0

                if defects is not None:

                    for s, e, f, depth in defects.reshape(
                        -1,
                        4
                    ):

                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        far = tuple(cnt[f][0])

                        a = dist(end, start)
                        b = dist(far, start)
                        c = dist(end, far)

                        if b * c == 0:
                            continue

                        # Calculate angle
                        angle = math.degrees(
                            math.acos(
                                max(
                                    -1,
                                    min(
                                        1,
                                        (
                                            b ** 2
                                            + c ** 2
                                            - a ** 2
                                        )
                                        /
                                        (2 * b * c)
                                    )
                                )
                            )
                        )

                        # Detect finger valley
                        if (
                            angle <= 90
                            and depth / 256 > 20
                        ):

                            gaps += 1

                            cv2.circle(
                                roi,
                                far,
                                5,
                                (0, 0, 255),
                                -1
                            )

                # Calculate fingers
                if gaps > 0:

                    fingers = min(
                        gaps + 1,
                        5
                    )

                else:

                    # Either fist or one finger
                    _, _, w, h = cv2.boundingRect(cnt)

                    if h / w > 1.4:
                        fingers = 1
                    else:
                        fingers = 0

        # ------------------------------------------------
        # Publish finger count
        # ------------------------------------------------

        finger_msg = Int32()
        finger_msg.data = int(fingers)

        self.finger_pub.publish(
            finger_msg
        )

        # ------------------------------------------------
        # Control Gazebo robot
        # ------------------------------------------------

        cmd = Twist()

        if fingers == 0:

            # STOP
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        elif fingers == 1:

            # FORWARD
            cmd.linear.x = self.speed
            cmd.angular.z = 0.0

        elif fingers == 2:

            # LEFT
            cmd.linear.x = 0.0
            cmd.angular.z = self.turn

        elif fingers == 3:

            # RIGHT
            cmd.linear.x = 0.0
            cmd.angular.z = -self.turn

        elif fingers == 4:

            # BACKWARD
            cmd.linear.x = -self.speed
            cmd.angular.z = 0.0

        elif fingers == 5:

            # STOP
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        # Publish velocity
        self.cmd_pub.publish(cmd)

        # Log only when finger count changes
        if fingers != self.previous_fingers:

            self.get_logger().info(
                f"Fingers: {fingers}"
            )

            self.previous_fingers = fingers

        # ------------------------------------------------
        # Display OpenCV
        # ------------------------------------------------

        if self.show:

            cv2.putText(
                frame,
                f"Fingers: {fingers}",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                3
            )

            # Display action
            if fingers == 0:
                action = "STOP"

            elif fingers == 1:
                action = "FORWARD"

            elif fingers == 2:
                action = "LEFT"

            elif fingers == 3:
                action = "RIGHT"

            elif fingers == 4:
                action = "BACKWARD"

            else:
                action = "STOP"

            cv2.putText(
                frame,
                action,
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (255, 0, 0),
                3
            )

            cv2.imshow(
                "Finger Robot Control",
                frame
            )

            cv2.imshow(
                "Mask",
                mask
            )

            # Press q to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):

                self.get_logger().info(
                    "Quit requested"
                )

                # Stop robot
                stop = Twist()

                self.cmd_pub.publish(
                    stop
                )

                rclpy.shutdown()

    def destroy_node(self):

        # Stop robot
        stop = Twist()

        self.cmd_pub.publish(
            stop
        )

        # Release camera
        self.cap.release()

        # Close OpenCV
        cv2.destroyAllWindows()

        super().destroy_node()


def main(args=None):

    rclpy.init(args=args)

    node = FingerTeleopNode()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()