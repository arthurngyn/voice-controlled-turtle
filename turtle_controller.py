import turtle

# Function to initialize the turtle window
def initialize_turtle():
    window = turtle.Screen()
    window.title("Turtle Controller")
    window.bgcolor("lightblue")
    
    turtle_obj = turtle.Turtle()
    turtle_obj.shape("turtle")
    turtle_obj.color("green")
    turtle_obj.speed(10)  # Speed set to max for smoother gliding
    
    return turtle_obj, window

# Function to move the turtle with a gliding effect
def move_turtle(command, turtle_obj, velocity):
    if command == "left":
        turtle_obj.left(90)
    elif command == "right":
        turtle_obj.right(90)
    elif command == "forward":
        velocity[0] += 0.3  # Increase forward velocity
    elif command == "back":
        velocity[0] -= 0.3  # Increase backward velocity
    else:
        print("Unknown command:", command)

def glide_turtle(turtle_obj, velocity):
    # Apply the velocity to move the turtle
    turtle_obj.forward(velocity[0])
    
    # Apply friction to slow down the velocity over time
    velocity[0] *= 0.9
    
    # Schedule the next glide
    turtle_obj.getscreen().ontimer(lambda: glide_turtle(turtle_obj, velocity), 50)
