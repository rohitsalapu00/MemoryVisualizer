import tkinter as tk
from tkinter import messagebox
from main import reset_memory, access_page


#Create main window
root = tk.Tk()
root.title("Memory Management Visualizer")
root.geometry("700x500")

#frame for inputs
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

#Acess sequence 
tk.Label(input_frame, text="Access Sequence(comma separated):").grid(row=0, column=0, sticky="w")
access_entry = tk.Entry(input_frame, width=30)
access_entry.grid(row=0, column=1)

#Number of frames
tk.Label(input_frame, text="Number of frames: ").grid(row=1, column=0, sticky="w")
frames_entry = tk.Entry(input_frame, width=10)
frames_entry.grid(row=1, column=1)

#Replacement algorithm
tk.Label(input_frame, text="Algorithm:").grid(row=2, column=0, sticky="w")
algo_var = tk.StringVar(value="FIFO")
algo_menu = tk.OptionMenu(input_frame, algo_var, "FIFO", "LRU")
algo_menu.grid(row=2, column=1)


#frame to display memory
memory_frame = tk.Frame(root)
memory_frame.pack(pady=20)

#funtion to create memory blocks
memory_labels = []


def create_memory_blocks(num_frames):
    #Create empty memory blocks in GUI
    global memory_labels
    for label in memory_labels:
        label.destroy() # Clear old blocks
    memory_labels = []
    for i in range(num_frames):
        lbl = tk.Label(memory_frame, text="Empty", width=12, height=4, relief="solid" ,bg="lightgray", font=("Arial",12))
        lbl.grid(row=0, column=i, padx=5)
        memory_labels.append(lbl)

def start_simulation():
    #Run the memory management simulation
    try:
        seq = [int(x.strip()) for x in access_entry.get().split(",") if x.strip()]
        num_frames = int(frames_entry.get())
        algo = algo_var.get()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid inputs")
        return
    
    #Reset memory before simulation
    physical_memory, page_table, page_faults, hits, page_usage_order, fifo_index = reset_memory(num_frames)
    create_memory_blocks(num_frames)

    #Run simulation step by step
    prev_faults = 0
    prev_hits = 0

    for page in seq:
        physical_memory, page_table, page_faults, hits, page_usage_order, fifo_index = access_page(page, algo, physical_memory, page_table, page_usage_order, page_faults, hits, fifo_index)
        #Decide color: fault or hit?
        if page_faults > prev_faults:
            color = "red" #page fault
            prev_faults = page_faults
        elif hits > prev_hits:
            color = "lightgreen" #hit
            prev_hits = hits
        else:
            color = "lightgrey" #empty(no change)

        #Update GUI memory blocks
        for i in range(num_frames):
            if physical_memory[i] is None:
                memory_labels[i].config(text="Empty", bg="lightgray")
            else:
                memory_labels[i].config(text=str(physical_memory[i]), bg=color)

        root.update()
        root.after(1000) #pause 1s for animation

    #show results in popup
    messagebox.showinfo("Simulation Finished", f"Page Faults: {page_faults}, Hits: {hits}")

#start Button 
start_button = tk.Button(input_frame, text="Start Simulation", command=start_simulation, bg="lightblue")
start_button.grid(row=3, column=0, columnspan=2, pady=10)


#Run the window
root.mainloop()