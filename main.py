print("Memory Management Visualizer Project")

#Physical memory frames(example: 4 frames)
NUM_FRAMES = 4
physical_memory = [None] * NUM_FRAMES #None means empty frame

#page table for a single process (pid = 1)
page_table ={} #page_number -> frame_index

# Counters
page_faults = 0
hits = 0

#replacement algorithm: FIFO or LRU
replacement_algo = "FIFO" #Change to "LRU" to test LRU
def access_page(page_number):
    global page_faults, hits
    global page_usage_order

    if page_number in page_table:
        #Page is in memory -> HIT
        hits += 1
        print(f"Page {page_number} -> HIT in frame {page_table[page_number]}") 
        if replacement_algo == "LRU":
            #Move page to end to mark it as most recently used
            page_usage_order.remove(page_number)
            page_usage_order.append(page_number)
    else:
        #Page fault -> load into memory
        page_faults += 1
        try:
            #Find first free frame
            free_index = physical_memory.index(None)
        except ValueError:
            #No free frame -> replace first one (FIFO simple)
            if replacement_algo == "FIFO":
                free_index = 0
                replaced_page = physical_memory[free_index]
            elif replacement_algo == "LRU":
                #Replace least recently used page
                lru_page = page_usage_order.pop(0)
                free_index = page_table[lru_page]
                replaced_page = lru_page
            print(f"Memory full !! Replacing page {replaced_page} from frame {free_index}")
            del page_table[replaced_page]
        
        #Load new page
        physical_memory[free_index] = page_number
        page_table[page_number] = free_index
        print(f"Page {page_number} loaded into frame {free_index}")

    #Update LRU usage order
    if replacement_algo == "LRU":
        if page_number not in page_usage_order:
            page_usage_order.append(page_number)

    print("Current Memory: ",physical_memory)
    print("Page Table: ",page_table)
    print(f"Page Faults: {page_faults}, Hits: {hits}\n")

access_sequence = [1, 2, 3, 1, 4, 5]
for page in access_sequence:
    access_page(page)

#Test FIFO
replacement_algo = "FIFO"
physical_memory = [None] * NUM_FRAMES
page_table = {}
page_faults = 0
hits = 0
page_usage_order = []
print("----Testing FIFO----")
for page in access_sequence:
    access_page(page)


#Test LRU
replacement_algo = "LRU"
physical_memory = [None] * NUM_FRAMES
page_table = {}
page_faults = 0
hits = 0
page_usage_order = []
print("----Testing LRU----")
for page in access_sequence:
    access_page(page)
