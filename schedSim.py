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
        self.wait = 0

    def __str__(self):
        return "Job: " + str(self.name) +" Run Time: " +  str(self.run_time) +  " Arrival: " + str(self.arrival) + " Started: " + str(self.start) + " Completed: " + str(self.completed)

    def __lt__(self, other):
        return self.run_time < other.run_time

def print_debug(jobs):
    for x in jobs:
        print(x)

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
    while len(running_jobs) > 0:
        # Increment Waitt
        for job in jobs:
            if time >= job.arrival and job.run_time > 0 and job.name != running_jobs[current_job].name:
                job.wait += 1
        # Update start time
        if running_jobs[current_job].start == -1:
            running_jobs[current_job].start = time
        # Adding New Jobs
        while next_job < len(jobs) and jobs[next_job].arrival == time:
            running_jobs.append(jobs[next_job])
            next_job += 1
        # Updating runtime, q, and time
        running_jobs[current_job].run_time -= 1
        job_runtime += 1
        time += 1
        # Next Job
        if job_runtime == q:
            # Go to next job
            current_job += 1
            job_runtime = 0
            # Check if at end of list
            if current_job == len(running_jobs):
                current_job = 0
        # Removing Job
        if running_jobs[current_job].run_time == 0:
            running_jobs[current_job].completed = time
            running_jobs.pop(current_job)
            if current_job >= len(running_jobs):
                current_job = 0
            job_runtime = 0




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
        # Get job with shortest time remaining
        current = q.get()
        # Update the start value
        if current.start == -1:
            current.start = time
        # Decrement Runtime
        current.run_time -= 1
        # Increment Wait
        for job in jobs:
            if time >= job.arrival and job.run_time > 0 and job.name != current.name:
                job.wait += 1
        # Check if completed
        if current.run_time > 0:
            q.put(current)
        # If completed mark down the time
        else:
            current.completed = time + 1
        # Increment time
        time += 1

def fifo(jobs):
    time = 0
    for job in jobs:
        job.start = time
        job.completed = time + job.run_time
        time += job.run_time
        job.wait= job.start - job.arrival

def print_jobs(jobs):
    avg_turn_around = 0
    avg_wait = 0
    for job in jobs:
        turn_around = job.completed - job.arrival
        print("Job {0} -- Turnaround {1:3.2f} Wait {2:3.2f}".format(job.name, turn_around, job.wait))
        avg_turn_around += turn_around
        avg_wait += job.wait
    print("Average -- Turnaround {0:3.2f} Wait {1:3.2f}".format(avg_turn_around / len(jobs), avg_wait/ len(jobs)))

def main():
    parser = argparse.ArgumentParser(description="Simulation of a scheduler")
    parser.add_argument("job_file", help= "Path to the file with the jobs")
    parser.add_argument("-p", required=False, help= "Type of scheduler (SRTN, FIFO, or RR")
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
            round_robin(jobs, int(args.q))
    elif alg == "FIFO" or  alg == None:
        fifo(jobs)
    else:
        raise Exception("Invalid algorithm")
    #print_debug(jobs)
    print_jobs(sorted(jobs, key=sort_name))


if __name__ == '__main__':
    main()