#!/usr/bin/env python
import rospy
import numpy as np
from zed_interfaces.msg import ObjectsStamped
from zed_test.msg import BitrapData  # Adjust the import based on your message type

# NODE used for getting the body detection and tracking (position and velocity) 
# from depth camera as input for path prediction model (Bitrap)

# Define the number of time steps to stack
NUM_TIME_STEPS = 10
MAX_MISSING_TIME_STEPS = 5

# Create a dictionary to store the history of positions and velocities for each person
obj_history = {}

# Create a dictionary to store the missing time steps for each person
missing_time_steps = {}

# ROS Publisher
bitrap_data_pub = None

def print_obj_history(instance_id, obj_matrix):
    print(f"Person {instance_id} matrix:\n{obj_matrix}")

def publish_obj_history(instance_id, obj_matrix):
    global bitrap_data_pub
    bitrap_data_msg = BitrapData()
    bitrap_data_msg.person_id = instance_id
    bitrap_data_msg.position_vel = obj_matrix.flatten().tolist()
    bitrap_data_pub.publish(bitrap_data_msg)

def callback(data):
    global bitrap_data_pub

    objects = data.objects

    # Update the missing_time_steps dictionary for each person
    for instance_id in list(missing_time_steps.keys()):
        if instance_id not in [obj.instance_id for obj in objects]:
            missing_time_steps[instance_id] += 1
            if missing_time_steps[instance_id] >= MAX_MISSING_TIME_STEPS:
                del missing_time_steps[instance_id]
                del obj_history[instance_id]
                print(f"Person {instance_id} removed from obj_history")

    # Process detected objects
    for obj in objects:
        if obj.label == "Person":
            pos_vel = np.array([obj.position[0], obj.position[1], obj.velocity[0], obj.velocity[1]])

            # Check if the person ID is already in the dictionary
            if obj.instance_id in obj_history:
                # If yes, reset the missing time steps counter
                missing_time_steps[obj.instance_id] = 0

                # Append the new position and velocity to the existing history
                obj_history[obj.instance_id].append(pos_vel)
                
                # Trim the history to keep only the last NUM_TIME_STEPS entries
                obj_history[obj.instance_id] = obj_history[obj.instance_id][-NUM_TIME_STEPS:]

                # Check if enough time steps have been accumulated
                if len(obj_history[obj.instance_id]) == NUM_TIME_STEPS:
                    # Convert the list of arrays into a matrix
                    obj_matrix = np.stack(obj_history[obj.instance_id])

                    # Publish the message
                    publish_obj_history(obj.instance_id, obj_matrix)
                    
                    # print(obj.instance_id)
            else:
                # If no, create a new entry in the dictionary
                obj_history[obj.instance_id] = [pos_vel]
                missing_time_steps[obj.instance_id] = 0

def listener():
    global bitrap_data_pub

    rospy.init_node('listener', anonymous=True)

    # Initialize the publisher
    bitrap_data_pub = rospy.Publisher('/bitrap_input', BitrapData, queue_size=10)

    data = rospy.Subscriber("/zed2/zed_node/obj_det/objects", ObjectsStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
