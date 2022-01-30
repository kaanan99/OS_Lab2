import argparse
import queue

class Job:

    def __init__(self, job_name, run_time, arrival):
        self.name = job_name
        job_name += 1
        self.run_time = run_time
        self.arrival = arrival
        self.start = -1
        self.completed = -1

    def __str__(self):
        return "Job: " + str(self.name) +" Run Time: " +  str(self.run_time) +  " Arrival: " + str(self.arrival) + " Started: " + str(self.start) + " Completed: " + str(self.completed)

    def __lt__(self, other):
        return self.run_time < other.run_time

def sort_arrival(job):
    return job.arrival

def sort_name(job):
    return job.name

def parse_file(file_path):
    job_list = []
    job_name = 0
    f = open(file_path)
    for job in f.readlines():
        line = job.split()
        job_list.append(Job(job_name, int(line[0]), int(line[1])))
        job_name += 1
    f.close()
    return sorted(job_list, key=sort_arrival)

def round_robin(jobs, q):
    running_jobs = []
    time = jobs[0].arrival
    running_jobs.append(jobs[0])
    current_job = 0
    next_job = 1
    job_runtime = 0
    jobs[0].start = time
    while len(running_jobs) > 0:
        # Next Job
        if job_runtime == q:
            current_job += 1
            if current_job == len(running_jobs):
                current_job = 0
            job_runtime = 0
            if running_jobs[current_job].start == -1:
                running_jobs[current_job].start = time
        # Adding New Jobs
        while next_job < len(jobs) and jobs[next_job].arrival == time:
            running_jobs.append(jobs[next_job])
            next_job += 1
        running_jobs[current_job].run_time -= 1
        job_runtime += 1
        # Removing Job
        if running_jobs[current_job].run_time == 0:
            running_jobs[current_job].completed = time
            running_jobs.pop(current_job)
            if current_job >= len(running_jobs):
                current_job = 0
            job_runtime = 0
        time += 1


def srtn(jobs):
    q = queue.PriorityQueue()
    time = jobs[0].arrival
    q.put(jobs[0])
    next_job = 1
    while not q.empty():
        # Check for next jobs
        while next_job < len(jobs) and jobs[next_job].arrival == time:
            q.put(jobs[next_job])
            next_job += 1
        # Increment time
        current = q.get()
        # Update the start value
        if current.start == -1:
            current.start = time
        # Decrement Runtime
        current.run_time -= 1
        # Check if completed
        if current.run_time > 0:
            q.put(current)
        # If completed mark down the time
        else:
            current.completed = time
        time += 1

def fifo(jobs):
    time = 0
    for job in jobs:
        job.start = time
        job.completed = time + job.run_time
        time += job.run_time

def print_jobs(jobs):
    avg_turn_around = 0
    avg_wait = 0
    for job in jobs:
        turn_around = job.completed - job.start
        wait = job.start - job.arrival
        print("Job {0} -- Turnaround {1:3.2f} Wait {2:3.2f}".format(job.name, turn_around, wait))
        avg_turn_around += turn_around
        avg_wait += wait
    print("Average -- Turnaround {0:3.2f} Wait {1:3.2f}".format(avg_turn_around / len(jobs), avg_wait/ len(jobs)))

def main():
    parser = argparse.ArgumentParser(description="Simulation of a scheduler")
    parser.add_argument("job_file", help= "Path to the file with the jobs")
    parser.add_argument("-p", required=True, help= "Type of scheduler (SRTN, FIFO, or RR")
    parser.add_argument("-q", required=False, help= "Time quantum value, defaults to 1")
    args = parser.parse_args()
    jobs = parse_file(args.job_file)
    alg = args.p
    if alg == "SRTN":
        srtn(jobs)
    elif alg == "RR":
        if args.q == None:
            round_robin(jobs, 1)
        else:
            round_robin(jobs, args.q)
    elif alg == "FIFO":
        fifo(jobs)
    else:
        raise Exception("Invalid algorithm")
    print_jobs(sorted(jobs, key=sort_name))


if __name__ == '__main__':
    main()