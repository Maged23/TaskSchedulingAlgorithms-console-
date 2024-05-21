'''
This function calculates the remaining resources each process needs to complete its execution.
FYI: need  = max_demand - allocation
'''

# def build_need_matrix(max_demand, allocation):
#     processes_num = len(max_demand)
#     resources_num = len(max_demand[0])
#     need_matrix =  []
#     for i in range(processes_num):
#         process_need = []
#         for j in range(resources_num):
#             process_need.append(max_demand[i][j] - allocation[i][j])
#         need_matrix.append(process_need)
#     return need_matrix
'''
This function detects deadlocks by checking which processes can finish with the available resources. 
It updates the work and finish arrays to reflect the current state of resource allocation and availability. 
Processes that cannot finish are identified as part of a deadlock.
'''
def detect_deadlock(available, allocation, request):
    num_processes = len(allocation)
    num_resources = len(available)
    
    work = available[:]
    finish = [False] * num_processes 
    
    # Find initial processes that can finish
    for i in range(num_processes):
        if all(request[i][j] == 0 for j in range(num_resources)):
            finish[i] = True #Mark this process as it will be able to finish execution
            # Add the allocated resources to the copy of the available
            for j in range(num_resources):
                work[j] += allocation[i][j]

    while True:
        found = False
        for i in range(num_processes):
            if not finish[i] and all(request[i][j] <= work[j] for j in range(num_resources)):
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                found = True
        if not found:
            break

    deadlocked_processes = [i for i in range(num_processes) if not finish[i]]
    return deadlocked_processes

# Using the algorithm
available = [3, 3, 2]  # 3 units of resource 0, 3 units of resource 1, 2 units of resource 2
# Maximum demand for each process
max_demand = [
    [7, 5, 3],  # Maximum demand for process 0
    [3, 2, 2],  # Maximum demand for process 1
    [9, 0, 2],  # Maximum demand for process 2
    [2, 2, 2],  # Maximum demand for process 3
    [4, 3, 3]   # Maximum demand for process 4
]
# Resources currently allocated to each process
allocation = [
    [0, 1, 0],  # Resources allocated to process 0
    [2, 0, 0],  # Resources allocated to process 1
    [3, 0, 2],  # Resources allocated to process 2
    [2, 1, 1],  # Resources allocated to process 3
    [0, 0, 2]   # Resources allocated to process 4
]
# Resources currently requested by each process
request = [
    [0, 12, 0],  # Resources requested by process 0
    [1, 0, 2],  # Resources requested by process 1
    [6, 0, 0],  # Resources requested by process 2
    [0, 0, 0],  # Resources requested by process 3
    [4, 3, 1]   # Resources requested by process 4
]

# Detect deadlock
deadlocked_processes = detect_deadlock(available, allocation, request)
if deadlocked_processes:
    print(f" Process {deadlocked_processes}  will go into a deadlock")
else:
    print("No deadlock detected.")
