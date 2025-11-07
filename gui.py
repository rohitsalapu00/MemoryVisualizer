import tkinter as tk
from tkinter import ttk, messagebox
from main import reset_memory, access_page


#Create main window
root = tk.Tk()
root.title("Memory Management Visualizer")
root.geometry("900x600")
root.configure(bg="#0f111a")

#Global theme 
ACCENT_COLOR = "#4a90e2"
BG_COLOR = "#0f111a"
CARD_BG = "#1b1f2f"
TEXT_COLOR = "#ffffff"

#Apply modern style using ttk
style = ttk.Style()
style.theme_use("clam")

#General style settings
style.configure(
    "TLabel",
    background=CARD_BG,
    foreground="white",
    font=("Segoe UI",11)
)
style.configure(
    "TButton",
    font=("Segoe UI Semibold",11),
    background=ACCENT_COLOR,
    foreground="white",
    padding=10
)
style.map("TButton",
          background=[("active","#6ca0f7")],
          relief=[("pressed","sunken")])

#Home page
home_frame = tk.Frame(root,bg=BG_COLOR)
home_frame.pack(fill="both",expand=True)

title_label = tk.Label(
    home_frame,
    text="Digital Memory Management Visualizer",
    font=("Segoe UI Black",24,"bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)
title_label.pack(pady=80)

desc_label = tk.Label(
    home_frame,
    text=(
        "Simulate and visualize how memory pages are replaced "
        "using FIFO and LRU algorithms.\n\n"
        "Understand page faults, hits and memory behavior interactively."
    ),
    font=("Segoe UI",13),
    bg=BG_COLOR,
    fg="#cccccc",
    justify="center"
)
desc_label.pack(pady=15)

start_btn = ttk.Button(
    home_frame,
    text="Start Simulation",
    command=lambda: show_simulation_page(),
)
start_btn.pack(pady=40)

#Simulation page frame
sim_frame = tk.Frame(root,bg=BG_COLOR)

header = tk.Label(
    sim_frame,
    text="Simualtion Setup",
    font=("Segoe UI Semibold", 18, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)
header.pack(padx=30)

#frame for inputs
input_frame = tk.Frame(sim_frame, bg=BG_COLOR, bd=2, relief="ridge")
input_frame.pack(pady=20, padx=20, ipadx=20, ipady=20)


#Acess sequence 
ttk.Label(input_frame, text="Access Sequence(comma separated):").grid(row=0, column=0, sticky="w",padx=10,pady=10)
access_entry = ttk.Entry(input_frame, width=45)
access_entry.grid(row=0, column=1,padx=10,pady=10)

#Number of frames
ttk.Label(input_frame, text="Number of frames: ").grid(row=1, column=0, sticky="w",padx=10,pady=10)
frames_entry = ttk.Entry(input_frame, width=20)
frames_entry.grid(row=1, column=1,padx=10,pady=10)

#Replacement algorithm
ttk.Label(input_frame, text="Algorithm:").grid(row=2, column=0, sticky="w",padx=10, pady=10)
algo_var = tk.StringVar(value="FIFO")
algo_menu = ttk.OptionMenu(input_frame, algo_var, "FIFO", "FIFO", "LRU")
algo_menu.grid(row=2, column=1,padx=10, pady=10)

#Buttons with hover effect
def on_enter(e):
    e.widget.config(background="#6ca0f7")
def on_leave(e):
    e.widget.config(background=ACCENT_COLOR)

start_sim_btn = tk.Button(
    input_frame,
    text="Start Simulation",
    bg=ACCENT_COLOR,
    fg="white",
    font=("Segoe UI Semibold",12),
    width=20,
    relief="flat",
    command=lambda: start_simulation()
)

start_sim_btn.grid(row=3, column=0, columnspan=2, pady=15)
start_sim_btn.bind("<Enter>",on_enter)
start_sim_btn.bind("<Leave>",on_leave)

#frame to display memory
memory_frame = tk.Frame(sim_frame, bg=BG_COLOR)
memory_frame.pack(pady=40)

#funtion to create memory blocks
memory_labels = []


def create_memory_blocks(num_frames):
    #Create empty memory blocks in GUI
    global memory_labels
    for label in memory_labels:
        label.destroy() # Clear old blocks
    memory_labels = []
    for i in range(num_frames):
        lbl = tk.Label(
                       memory_frame, 
                       text="Empty", 
                       width=15, 
                       height=5, 
                       relief="ridge", 
                       bg="#262a3b",
                       fg="white", 
                       font=("Segoe UI",12,"bold")
                       )
        lbl.grid(row=0, column=i, padx=8)
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
            color = "#e74c3c" #page fault
            prev_faults = page_faults
        elif hits > prev_hits:
            color = "#27ae60" #hit
            prev_hits = hits
        else:
            color = "#262a3b" #empty(no change)

        #Update GUI memory blocks
        for i in range(num_frames):
            if physical_memory[i] is None:
                memory_labels[i].config(text="Empty", bg="#262a3b")
            else:
                memory_labels[i].config(text=str(physical_memory[i]), bg=color)

        root.update()
        root.after(900) #pause 1s for animation

    #show results in popup
    messagebox.showinfo("Simulation Finished", f"Page Faults: {page_faults}\nHits: {hits}")

# #start Button 
# start_btn2 = ttk.Button(input_frame, text="Start Simulation", command=start_simulation)
# start_btn2.grid(row=3, column=0, columnspan=2, pady=15)

#Navigation Function
def show_simulation_page():
    home_frame.pack_forget()
    sim_frame.pack(fill="both", expand=True)



#Run the window
root.mainloop()