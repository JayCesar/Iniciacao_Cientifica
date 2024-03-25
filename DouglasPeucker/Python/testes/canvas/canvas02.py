import tkinter as tk

def main():
    # Define the points
    points = [(0, 0), (100, 100), (200, 200), (300, 300), (400, 400)]
    
    # Create the Tkinter window
    root = tk.Tk()
    root.title("Line Drawing Example")

    # Create a canvas widget
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    # Draw the line
    canvas.create_line(*points, fill="blue", width=2)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
