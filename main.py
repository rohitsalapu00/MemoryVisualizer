print("Memory Management Visualizer Project")

#Physical memory frames(example: 4 frames)
NUM_FRAMES = 4
physical_memory = [None] * NUM_FRAMES #None means empty frame

#page table for a single process (pid = 1)
page_table ={} #page_number -> frame_index

# Counters
page_faults = 0
hits = 0

def access_page(page_number):
    global page_faults, hits

    if page_number in page_table:
        #Page is in memory -> HIT
        hits += 1
        print(f"Page {page_number} -> HIT in frame {page_table[page_number]}") 
    else:
        #Page fault -> load into memory
        page_faults += 1
        try:
            #Find first free frame
            free_index = physical_memory.index(None)
        except ValueError:
            #No free frame -> replace first one (FIFO simple)
            free_index = 0
            replaced_page = physical_memory[free_index]
            print(f"Memory full !! Replacing page {replaced_page} from frame {free_index}")
            #Remove replaced page from page table
            for key, value in page_table.items():
                if value == free_index:
                    del page_table[key]
                    break
        
        #Load new page
        physical_memory[free_index] = page_number
        page_table[page_number] = free_index
        print(f"Page {page_number} loaded into frame {free_index}")

    print("Current Memory: ",physical_memory)
    print("Page Table: ",page_table)
    print(f"Page Faults: {page_faults}, Hits: {hits}\n")

access_sequence = [1, 2, 3, 1, 4, 5]
for page in access_sequence:
    access_page(page)
