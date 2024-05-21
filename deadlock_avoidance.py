def build_need_matrix(max_demand, allocation):
    processes_num = len(max_demand)
    resources_num = len(max_demand[0])
    need_matrix =  []
    for i in range(processes_num):
        process_need = []
        for j in range(resources_num):
            process_need.append(max_demand[i][j] - allocation[i][j])
        need_matrix.append(process_need)
    return need_matrix


def is_safe_state(available, allocation, need):
    processes_num = len(allocation)
    resources_num = len(available)
    work = available[:]
    finish = [False] * processes_num
    safe_sequence = [] #store the order of process executions if the system is found to be in a safe state.

    while len(safe_sequence) < processes_num:
        allocated_in_this_round = False
        for i in range(processes_num):
            ''' 
            Does the need of the process i can be satisfied by the currently available 
            resources plus resources held by tasks prior to current task
            '''
            if not finish[i] and all(need[i][j] <= work[j] for j in range(resources_num)):
                safe_sequence.append(i)
                finish[i] = True
                for j in range(resources_num):
                    work[j] += allocation[i][j]
                allocated_in_this_round = True
        # If allocated_in_this_round flag is still false there is no safe sequence exist
        if not allocated_in_this_round:
            return False, []
    
    return True, safe_sequence
'''
This function processes resource requests from a given process, temporarily allocates the resources 
if possible, and checks if the new state is safe. If not, it rolls back the allocation
'''
def request_resources(available, max_demand, allocation, process_id, request):
    need = build_need_matrix(max_demand, allocation)
    num_resources = len(available)

    if all(request[j] <= need[process_id][j] for j in range(num_resources)) and \
       all(request[j] <= available[j] for j in range(num_resources)):
        
        # Temporarily allocate requested resources
        for j in range(num_resources):
            available[j] -= request[j]
            allocation[process_id][j] += request[j]
            need[process_id][j] -= request[j]
        
        safe, _ = is_safe_state(available, allocation, need)

        if safe:
            return True # The system is still in safe state after granting the resources to the process
        else:
            # Rollback allocation
            for j in range(num_resources):
                available[j] += request[j]
                allocation[process_id][j] -= request[j]
                need[process_id][j] += request[j]
            return False
    else: # In case the process has requested more than the available or more than its needs
        return False

# Example usage
available = [3, 3, 2]  # Resources currently available
max_demand = [
    [7, 5, 3],  # Maximum demand for process 0
    [3, 2, 2],  # Maximum demand for process 1
    [9, 0, 2],  # Maximum demand for process 2
    [2, 2, 2],  # Maximum demand for process 3
    [4, 3, 3]   # Maximum demand for process 4
]
allocation = [
    [0, 1, 0],  # Resources allocated to process 0
    [2, 0, 0],  # Resources allocated to process 1
    [3, 0, 2],  # Resources allocated to process 2
    [2, 1, 1],  # Resources allocated to process 3
    [0, 0, 2]   # Resources allocated to process 4
]

# Calculate need matrix
need = build_need_matrix(max_demand, allocation)

# Check if the system is in a safe state
is_safe, safe_sequence = is_safe_state(available, allocation, need)
print("Is the system in a safe state?", is_safe)
if is_safe:
    print("Safe sequence:", safe_sequence)

# Request resources for a process
process_num = 2
request = [1, 0, 0]  # Process 1 requests 1 of the first resource, 0 of the second, and 2 of the third
if request_resources(available, max_demand, allocation, process_num, request):
    print(f"Resources successfully allocated to process {process_num}.")
else:
    print(f"Resources request by process {process_num} denied.")
