import tkinter as tk
import queue
import time

# Function to setup the tkinter UI
def setup_ui(turtle_obj):
    root = tk.Tk()
    root.title("Turtle Controller")
    
    # Create label to display command history
    movements_label = tk.Label(root, text="Command history:", font=("Helvetica", 16))
    movements_label.pack(pady=20)
    
    command_queue = queue.Queue()
    
    return root, movements_label, command_queue

# Function to update the UI with command history
def update_ui(movements_label, history):
    movements_label.config(text="Command history:\n" + "\n".join(history))

# Function to turn the turtle incrementally
def turn_turtle(turtle_obj, angle, duration=0.5):
    steps = 36  # Number of steps for smooth turning
    step_angle = angle / steps
    step_duration = duration / steps
    
    for _ in range(steps):
        turtle_obj.left(step_angle)
        turtle_obj.getscreen().update()  # Update screen to show rotation
        time.sleep(step_duration)  # Delay to make the rotation visible

# Function to process commands and control the turtle
def process_commands(command_queue, root, turtle_obj, movements_label, velocity):
    history = []

    def process_command(command):
        nonlocal turtle_obj, velocity
        if command == "done":
            return False
        elif command == "forward":
            turtle_obj.forward(10)
        elif command == "left":
            turn_turtle(turtle_obj, 90)  # Turn left 90 degrees incrementally
        elif command == "right":
            turn_turtle(turtle_obj, -90)  # Turn right 90 degrees incrementally
        # Add more commands as needed
        velocity[0] += 0.4  # Example: Increase velocity
        history.append(command)
        return True
    
    def process_command_wrapper():
        try:
            command = command_queue.get(timeout=1)  # Timeout to prevent blocking indefinitely
            if not process_command(command):
                return
            update_ui(movements_label, history)  # Update UI after each command
        except queue.Empty:
            pass  # Handle empty queue if necessary
        root.after(100, process_command_wrapper)  # Schedule next check
    
    # Start the loop to process commands
    process_command_wrapper()
