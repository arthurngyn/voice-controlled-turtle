import turtle
import speech_recognition as sr
import tkinter as tk
import threading
import queue

# Function to initialize the turtle window
def initialize_turtle():
    window = turtle.Screen()
    window.title("Turtle Controller")
    window.bgcolor("lightblue")  # Set background color
    
    turtle_obj = turtle.Turtle()
    turtle_obj.shape("turtle")
    turtle_obj.color("green")
    turtle_obj.speed(3)  # Set initial speed (adjust as needed)
    
    return turtle_obj, window

# Function to move the turtle based on the recognized command
def move_turtle(command, turtle_obj):
    if command == "left":
        turtle_obj.left(90)  # Turn left by 90 degrees
    elif command == "right":
        turtle_obj.right(90)  # Turn right by 90 degrees
    elif command == "forward":
        turtle_obj.forward(20)
    elif command == "back":
        turtle_obj.backward(20)
    else:
        print("Unknown command:", command)

# Function to recognize speech and put recognized commands into the queue
def recognize_speech(recognizer, mic, queue):
    recognizer.energy_threshold = 5000  # Set energy threshold to 5000
    with mic as source:
        print("Listening for command...")
        while True:
            try:
                audio = recognizer.listen(source)  # Continuously listen for audio
                print("Audio captured...")
                command = recognizer.recognize_google(audio).lower()  # Use recognize_google for online recognition
                print(f"Heard command: {command}")
                queue.put(command)  # Put recognized command into the queue
                if command == "done":
                    break  # Stop listening if "done" is recognized
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError as e:
                print(f"Error requesting recognition results: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

# Function to process commands from the queue and control the turtle
def process_commands(queue, turtle_obj, text_widget):
    while True:
        try:
            command = queue.get()  # Get command from the queue
            if command == "done":
                break
            # Schedule turtle movement and update command history in the main thread
            root.after(0, move_turtle, command, turtle_obj)
            root.after(0, update_command_history, text_widget, command)
        except queue.Empty:
            continue

# Function to update the command history in the text widget
def update_command_history(text_widget, command):
    text_widget.insert(tk.END, f"{command}\n")
    text_widget.see(tk.END)  # Scroll to the end

# Function to close the application
def close_application(window):
    window.bye()  # Close the turtle graphics window
    root.destroy()  # Close the tkinter window

if __name__ == "__main__":
    turtle_obj, window = initialize_turtle()
    
    # Create tkinter window
    root = tk.Tk()
    root.title("Turtle Controller")
    
    # Create text widget to display command history
    command_history = tk.Text(root, height=10, width=40, font=("Helvetica", 16))
    command_history.pack(pady=20)
    
    # Setup speech recognition
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    # Queue for communication between threads
    command_queue = queue.Queue()
    
    # Start speech recognition thread
    thread_recognition = threading.Thread(target=recognize_speech, args=(recognizer, mic, command_queue))
    thread_recognition.start()
    
    # Start command processing thread
    thread_processing = threading.Thread(target=process_commands, args=(command_queue, turtle_obj, command_history))
    thread_processing.start()
    
    # Function to close the application when "done" command is received
    root.protocol("WM_DELETE_WINDOW", lambda: close_application(window))
    
    root.mainloop()  # Start the tkinter event loop
    
    # Wait for threads to finish
    thread_recognition.join()
    thread_processing.join()
