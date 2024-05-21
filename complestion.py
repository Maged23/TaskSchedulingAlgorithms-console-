import ast
import math

def completion_time_test(tasks):
    """Check if the task set is schedulable using the Completion-Time Test."""
    task_list = sorted(tasks.items(), key=lambda x: x[1][0])  # Sort by period (rate-monotonic order)
    explanation = {}
    
    # Always consider the first task as schedulable
    explanation[task_list[0][0]] = [f"Task {task_list[0][0]} is highest priority Task So, it is obviously schedulable."]
    
    for i, (task_name, (period, execution)) in enumerate(task_list):
        if i == 0:
            continue  # Skip the first task since it's considered schedulable
        
        schedulable, explanation[task_name] = is_task_schedulable([(p, e) for t, (p, e) in task_list[:i + 1]], period, execution)
        if not schedulable:
            return False, explanation
    return True, explanation

def is_task_schedulable(task_list, period, execution):
    """Check if a single task is schedulable given a list of higher-priority tasks."""
    explanation = []
    t = execution
    while True:
        # Calculate the next workload after adding the execution time of the current task
        next_workload = execution + sum(math.ceil(t / hp_period) * hp_execution for hp_period, hp_execution in task_list[:-1])
        if next_workload == t:
            if t <= period:
                explanation.append(f"Task {task_list[-1][0]} meets its deadline with workload {t} <= deadline {period}.")
                return True, explanation
            else:
                explanation.append(f"Task {task_list[-1][0]} misses deadline with workload {t} > deadline {period}.")
                return False, explanation
        elif next_workload > period:
            explanation.append(f"Task {task_list[-1][0]} exceeds its deadline during iteration with workload {next_workload} > deadline {period}.")
            return False, explanation
        t = next_workload

def main():
    input_dict = {}
    num = int(input("Enter the number of tasks: "))
    for i in range(num):
        key = "task {}".format(i + 1)
        input_dict[key] = ast.literal_eval(input(f"Enter the period and execution time for {key} (in the form (period, execution_time)): "))

    schedulable, explanation = completion_time_test(input_dict)
    if schedulable:
        print("Task Set is Schedulable by Completion-Time Test")
    else:
        print("Task Set is not Schedulable by Completion-Time Test")
        print("Explanation for each task:")
        for task, expl_list in explanation.items():
            print(f"{task}:")
            for expl in expl_list:
                print(f" - {expl}")

if __name__ == "__main__":
    main()
