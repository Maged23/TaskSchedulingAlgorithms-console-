import ast
import math

# Calculate the utilization bound for the given number of tasks
def calculate_bound(num):
    """Calculate the utilization bound for the given number of tasks."""
    return num * (math.pow(2, (1 / num)) - 1)

# Check if the task set is schedulable
def is_schedulable(tasks, bound):
    """Check if the task set is schedulable."""
    total_utilization = sum(execution / period for period, execution in tasks.values())
    return total_utilization, total_utilization <= bound

def main():
    input_dict = {}
    num = int(input("Enter the number of tasks: "))
    for i in range(num):
        key = "task {}".format(i + 1)
        input_dict[key] = ast.literal_eval(input(f"Enter the period and execution time for {key} (in the form (period, execution_time)): "))
        

    bound = calculate_bound(num)
    total_utilization, schedulable = is_schedulable(input_dict, bound)
    
    # Format the output to two decimal places
    total_utilization_str = f"{total_utilization:.2f}"
    bound_str = f"{bound:.2f}"
    
    if schedulable:
        print(f"{total_utilization_str} is less than or equal to {bound_str}")
        print("Task Set is Schedulable")
    else:
        print(f"{total_utilization_str} is greater than {bound_str}")
        print("Task Set is not Schedulable")

if __name__ == "__main__":
    main()






