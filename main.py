
def reset_memory(num_frames):
    #Reset memory and counters before a simulation run
    physical_memory = [None] * num_frames
    page_table = {}
    page_faults = 0
    hits = 0
    page_usage_order = []
    fifo_index = 0
    return physical_memory, page_table, page_faults, hits, page_usage_order, fifo_index

#replacement algorithm: FIFO or LRU
def access_page(page_number, algo, physical_memory, page_table,page_usage_order, page_faults, hits, fifo_index):
    #Simulates accessing a page using FIFO or LRU algorithm
    num_frames = len(physical_memory)

    if page_number in page_table:
        #Page is in memory -> HIT
        hits += 1 
        if algo == "LRU":
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
            if algo == "FIFO":
                free_index = fifo_index
                replaced_page = physical_memory[free_index]
                fifo_index = (fifo_index + 1) % num_frames
            elif algo == "LRU":
                #Replace least recently used page
                lru_page = page_usage_order.pop(0)
                free_index = page_table[lru_page]
                replaced_page = lru_page
            del page_table[replaced_page]

        
        #Load new page
        physical_memory[free_index] = page_number
        page_table[page_number] = free_index

    #Update LRU usage order
    if algo == "LRU" and page_number not in page_usage_order:
            page_usage_order.append(page_number)

    return physical_memory, page_table, page_faults, hits, page_usage_order, fifo_index