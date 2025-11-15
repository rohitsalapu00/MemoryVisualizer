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

style.configure("TLabel",background=CARD_BG, foreground= "white",font=("Segoe UI",11))
style.configure("TButton", font=("Segoe UI semibold",11), backgound=ACCENT_COLOR,foreground="white",padding=10)
style.map("TButton", background=[("active","#6ca0f7")], relief=[("pressed", "sunken")])
# style.map("TButton", background=[("active", "#6ca0f7")], relief=[("pressed", "sunken")])



#============home page===============

home_frame = tk.Frame(root, bg=BG_COLOR)
home_frame.pack(fill="both",expand=True)

title_label = tk.Label(
    home_frame,
    text="Digital Memory Management visualizer",
    font=("Segoe UI Black",24,"bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)

title_label.pack(pady=60)

desc_label = tk.Label(
    home_frame,
    text=(
        "Simulate and visualize how memory pages are replaced"
        "using FIFO and LRU algorithms.\n\n"
        "understand page faults, hits, and memory behavior interactively."
    ),
    font=("Segeo UI", 13),
    bg=BG_COLOR,
    fg="#cccccc",
    justify="center"
)

desc_label.pack(pady=10)




#--Fifo & LRu Explanation-----------

info_frame = tk.Frame(home_frame,bg=CARD_BG, bd=1, relief="solid")
info_frame.pack(padx=80, pady=30, fill="x")

fifo_label = tk.Label(
    info_frame,
    text="Fifo (First In, First Out):",
    font=("Segoe UI semibold",13),
    bg=CARD_BG,
    fg=ACCENT_COLOR,
    anchor="w"
)

fifo_label.pack(anchor="w",padx=15, pady=(10,0))

fifo_text = tk.Label(
    info_frame,
    text=". The oldest loaded page is replaced first.\n"
    ". Works like a queue - first page is the first to be removed.\n"
    ". simple but may cause more page faults (Belady's anomaly).",

    font=("Segoe UI",11),
    bg=CARD_BG,
    fg="#cccccc",
    justify="left",
    wraplength=700
)

fifo_text.pack(anchor="w",padx=30,pady=(0,15))

lru_label = tk.Label(
    info_frame,
    text = "LRU (Least Recently used):",
    font=("Segoe UI semibold",13),
    bg = CARD_BG,
    fg=ACCENT_COLOR,
    anchor="w"
)

lru_label.pack(anchor="w",padx=15, pady=(5,0))

lru_text = tk.Label(
    info_frame,
    text=". Replaces the page that has been used for the longest time.\n"
        ". keeps track of recently accessed pages.\n"
        ". more efficient than FIFO is most real systems.",
    font=("Segoe UI",11),
    bg=CARD_BG,
    fg="#cccccc",
    justify="left",
    wraplength=700
)

lru_text.pack(anchor="w", padx=30, pady=(0,15))

#start button

def start_btn_enter(e):
    start_btn.config(bg="")

def start_btn_leave(e):
    start_btn.config(bg="")

start_btn = tk.Button(
    home_frame,
    text="Start simulation",
    bg=ACCENT_COLOR,
    fg="white",
    font=("Segoe UI semibold",12),
    width=20,
    relief="flat",
    command=lambda: show_simulation_page(),
)

start_btn.bind("<Enter>", start_btn_enter)
start_btn.bind("<Leave>", start_btn_leave)

start_btn.pack(pady=30)

#--------------------SIMULATION PAGE---------------------------

sim_frame = tk.Frame(root, bg=BG_COLOR)

header = tk.Label(
    sim_frame,
    text = "Simulation Setup",
    font=("Segoe UI semibold",18,"bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)

header.pack(padx=30, pady=(20,10))

input_frame = tk.Frame(sim_frame, bg=BG_COLOR, bd = 2,relief="ridge")
input_frame.pack(pady=20, padx=20, ipadx=20,ipady=20)

ttk.Label(input_frame, text="Access sequence (comma sepearated):").grid(row=0,column=0, sticky="W",padx=10, pady=10)
access_entry = ttk.Entry(input_frame,width=45)
access_entry.grid(row=0, column=1,padx=10, pady=10)

ttk.Label(input_frame, text="Number of frames: ").grid(row=1,column=0,sticky="W",padx=10,pady=10)
frames_entry = ttk.Entry(input_frame, width=20)
frames_entry.grid(row=1,column=1,padx=10,pady=10)

ttk.Label(input_frame,text="Algorithm:").grid(row=2, column=0,sticky="w",padx=10,pady=10)
algo_var = tk.StringVar(value="FIFO")
algo_menu = ttk.OptionMenu(input_frame,algo_var,"FIFO","FIFO","LRU")
algo_menu.grid(row=2, column=1, padx=10, pady=10)

#hover effects

def on_enter(e): e.widget.config(backgorund="#0A7CC0")
def on_leave(e): e.widget.config(background=ACCENT_COLOR)

#start simulation button

start_sim_btn = tk.Button(
    input_frame,
    text="Start simulation",
    bg=ACCENT_COLOR,
    fg="white",
    font=("Segoe UI semibold",12),
    width=20,
    relief="flat",
    command=lambda: start_simulation()
)

start_sim_btn.grid(row=3, column=0, columnspan=2, pady=15)
start_sim_btn.bind("<Enter>", on_enter)
start_sim_btn.bind("<Leave>",on_leave)


#back to home button 
back_btn = tk.Button(
    sim_frame,
    text = "Back",
    bg="#33384d",
    fg="white",
    font=("Segoe UI semibold",11),
    width=15,
    relief="flat",
    command=lambda: show_home_page()
)
back_btn.pack(pady=10)

#memory visualization area
memory_frame=tk.Frame(sim_frame,bg=BG_COLOR)
memory_frame.pack(pady=40)

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

def show_home_page():
    sim_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)

#Run the window+ 
root.mainloop()