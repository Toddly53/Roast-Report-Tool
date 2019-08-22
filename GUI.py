# Import modules.
import Main
import Errors

# Import GUI kit.
import tkinter as tk


# A function to create the GUI that will check the user inputs and run the reporting tool.
def run_app():
    
    # Create the master frame and give it a title.
    main = tk.Tk()
    main.title("Roast Report Tool")
    
    # Make a canvas with correct size.
    canvas = tk.Canvas(main, height = 250, width = 600)
    canvas.pack()
    
    # Make the main frame and set the dimesions.
    frame = tk.Frame(main)
    frame.place(relx = .05, rely = .05, relwidth = .9, relheight = .9)
    
    # Make the label and entry for start roast.
    start_roast_label = tk.Label(frame, text = 'First Roast Number:', font = 16)
    start_roast_label.place(relx = .1, rely = .1, relwidth = .25, relheight = .075)
    start_roast_entry = tk.Entry(frame)
    start_roast_entry.place(relx = .4, rely = .1, relwidth = .25, relheight = .075)
    
    # Make the label and entry for finish roast.
    finish_roast_label = tk.Label(frame, text = 'Last Roast Number:', font = 16)
    finish_roast_label.place(relx = .1, rely = .25, relwidth = .25, relheight = .075)
    finish_roast_entry = tk.Entry(frame)
    finish_roast_entry.place(relx = .4, rely = .25, relwidth = .25, relheight = .075)
    
    # Make the label and entry for username.
    username_label = tk.Label(frame, text = 'Username:', font = 16)
    username_label.place(relx = .1, rely = .4, relwidth = .25, relheight = .075)
    username_entry = tk.Entry(frame)
    username_entry.place(relx = .4, rely = .4, relwidth = .25, relheight = .075)
    
    # Make the label and entry for password.
    password_label = tk.Label(frame, text = 'Password:', font = 16)
    password_label.place(relx = .1, rely = .55, relwidth = .25, relheight = .075)
    password_entry = tk.Entry(frame)
    password_entry.place(relx = .4, rely = .55, relwidth = .25, relheight = .075)
    
    # Make the label and entry for file path
    file_path_label = tk.Label(frame, text = 'File Path:', font = 16)
    file_path_label.place(relx = .1, rely = .7, relwidth = .25, relheight = .075)
    file_path_entry = tk.Entry(frame)
    file_path_entry.place(relx = .4, rely = .7, relwidth = .25, relheight = .075)
    
    
    # Make the 'Run' button and set logic to either run the reporting tool or not based on user inputs.
    run_button = tk.Button(frame, text = 'Run', command = lambda:  
        Main.run_reporting_tool(
                start_roast_entry.get(), 
                finish_roast_entry.get(), 
                username_entry.get(), 
                password_entry.get(), 
                'Events.csv',
                file_path_entry.get(), 
                main) if
        Errors.check_inputs(
                start_roast_entry.get(), 
                finish_roast_entry.get(), 
                username_entry.get(), 
                password_entry.get(), 
                file_path_entry.get()) else
        print('Error'))
    run_button.place(relx = .75, rely = .85, relwidth = .10, relheight = .075)
    
    # Make the 'Quit' button that will destroy the GUI.
    quit_button = tk.Button(frame, text = 'Quit', command = lambda: main.destroy())
    quit_button.place(relx = .9, rely = .85, relwidth = .10, relheight = .075)
    
    # Run the GUI.
    main.mainloop()


# Run the application.
run_app()

