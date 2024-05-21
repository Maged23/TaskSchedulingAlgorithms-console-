import ast

def period_transformation_test(tasks):
    """Check if the task set is schedulable using the Period Transformation Test."""
    transformed_tasks = []
    for i, (task_name, (period, execution)) in enumerate(sorted(tasks.items(), key=lambda x: x[1][0])):
        transformed_period = period_transform(period, i+1)
        transformed_tasks.append((task_name, transformed_period, execution))
        if not is_rm_schedulable(transformed_tasks):
            return False, f"Period Transformation Test failed for task {task_name}"
    return True, "Period Transformation Test passed for all tasks"

def period_transform(period, n):
    """Transform the period of a task."""
    return period * (2**(1/n) - 1)

def is_rm_schedulable(tasks):
    """Check if the transformed tasks are schedulable using rate-monotonic scheduling."""
    tasks = sorted(tasks, key=lambda x: x[1])
    total_utilization = sum(execution / period for _, period, execution in tasks)
    return total_utilization <= 1

def main():
    input_dict = {}
    num = int(input("Enter the number of tasks: "))
    for i in range(num):
        key = "task {}".format(i + 1)
        input_dict[key] = ast.literal_eval(input(f"Enter the period and execution time for {key} (in the form (period, execution_time)): "))

    schedulable, explanation = period_transformation_test(input_dict)
    if schedulable:
        print("Task Set is Schedulable by Period Transformation Test")
    else:
        print("Task Set is not Schedulable by Period Transformation Test")
        print("Explanation:", explanation)

if __name__ == "__main__":
    main()
