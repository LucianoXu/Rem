import multiprocessing

def worker_function(shared_list):
    # Modify the shared list
    shared_list.append("Processed by {}".format(multiprocessing.current_process().name))

if __name__ == "__main__":
    # Create a manager object
    manager = multiprocessing.Manager()

    # Create a shared list using the manager
    shared_list = manager.list()

    # Define the number of processes you want to create
    num_processes = 4

    # Create a list to hold references to the processes
    processes = []

    # Start the processes
    for i in range(num_processes):
        p = multiprocessing.Process(target=worker_function, args=(shared_list,))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Print the shared list after all processes have completed
    print("Shared list after processing:", shared_list)
