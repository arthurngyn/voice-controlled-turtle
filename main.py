import turtle
import tkinter as tk
import threading
import queue
from turtle_controller import initialize_turtle, glide_turtle, move_turtle
from ui_controller import setup_ui, update_ui, process_commands
from recognize_speech import recognize_speech  # Correct import statement

if __name__ == "__main__":
    turtle_obj, window = initialize_turtle()
    velocity = [0]  # Initialize velocity
    
    # Start the gliding effect
    glide_turtle(turtle_obj, velocity)
    
    # Create tkinter window and setup UI
    root, movements_label, command_queue = setup_ui(turtle_obj)
    
    # Start speech recognition in a separate thread
    thread_recognition = threading.Thread(target=recognize_speech, args=(command_queue,))
    thread_recognition.start()
    
    # Start processing commands in a separate thread
    thread_processing = threading.Thread(target=process_commands, args=(command_queue, root, turtle_obj, movements_label, velocity))
    thread_processing.start()
    
    root.mainloop()  # Start the tkinter event loop
    
    # Wait for recognition thread to finish
    thread_recognition.join()
    
    # Wait for processing thread to finish
    thread_processing.join()
    
    # Close the turtle graphics window
    window.bye()
