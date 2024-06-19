import turtle
import speech_recognition as sr
import tkinter as tk
import threading
import queue

# Function to initialize the turtle window
def initialize_turtle():
    window = turtle.Screen()
    window.title("Turtle Controller")
    window.bgcolor("lightblue")
    
    turtle_obj = turtle.Turtle()
    turtle_obj.shape("turtle")
    turtle_obj.color("green")
    turtle_obj.speed(0)  # Speed set to max for smoother gliding
    
    return turtle_obj, window

# Function to move the turtle with a gliding effect
def move_turtle(command, turtle_obj, velocity):
    if command == "left":
        turtle_obj.left(90)
    elif command == "right":
        turtle_obj.right(90)
    elif command == "forward":
        velocity[0] += 10  # Increase forward velocity
    elif command == "back":
        velocity[0] -= 10  # Increase backward velocity
    else:
        print("Unknown command:", command)

def glide_turtle(turtle_obj, velocity):
    # Apply the velocity to move the turtle
    turtle_obj.forward(velocity[0])
    
    # Apply friction to slow down the velocity over time
    velocity[0] *= 0.9
    
    # Schedule the next glide
    turtle_obj.getscreen().ontimer(lambda: glide_turtle(turtle_obj, velocity), 50)

# Function to recognize speech and update GUI
def recognize_speech(recognizer, mic, command_queue):
    recognizer.energy_threshold = 5000
    with mic as source:
        print("Listening for command...")
        while True:
            try:
                audio = recognizer.listen(source)
                print("Audio captured...")
                command = recognizer.recognize_google(audio).lower()
                print(f"Heard command: {command}")
                command_queue.put(command)
                if command == "done":
                    break
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError as e:
                print(f"Error requesting recognition results: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

# Function to process commands from the queue
def process_commands(command_queue, movements_label, turtle_obj, velocity):
    history = []
    while True:
        try:
            command = command_queue.get(timeout=0.1)
            if command == "done":
                break
            history.append(command)
            root.after(0, lambda: update_ui(command, movements_label, history, turtle_obj, velocity))
        except queue.Empty:
            continue

# Function to update the UI and move the turtle
def update_ui(command, movements_label, history, turtle_obj, velocity):
    move_turtle(command, turtle_obj, velocity)
    movements_label.config(text="Command history:\n" + "\n".join(history))

# Function to close the application
def close_application():
    window.bye()  # Close the turtle graphics window
    root.destroy()  # Close the tkinter window

if __name__ == "__main__":
    turtle_obj, window = initialize_turtle()
    velocity = [0]  # Initialize velocity
    
    # Start the gliding effect
    glide_turtle(turtle_obj, velocity)
    
    # Create tkinter window
    root = tk.Tk()
    root.title("Turtle Controller")
    
    # Create label to display command history
    movements_label = tk.Label(root, text="Command history:", font=("Helvetica", 16))
    movements_label.pack(pady=20)
    
    # Setup speech recognition
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    command_queue = queue.Queue()
    
    # Start speech recognition in a separate thread
    thread_recognition = threading.Thread(target=recognize_speech, args=(recognizer, mic, command_queue))
    thread_recognition.start()
    
    # Start processing commands in the main thread
    thread_processing = threading.Thread(target=process_commands, args=(command_queue, movements_label, turtle_obj, velocity))
    thread_processing.start()
    
    root.mainloop()  # Start the tkinter event loop

    thread_recognition.join()  # Wait for the speech recognition thread to finish
    thread_processing.join()  # Wait for the command processing thread to finish
    
    # Close the turtle graphics window
    window.bye()
