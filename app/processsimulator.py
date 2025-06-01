import os
import random
import string
import time
import csv
from datetime import datetime, timedelta


class ProcessSimulator:
    def __init__(self, output_dir="log"):
        self.active_jobs = []
        self.jobs = []

    def _generate_id(self):
        return random.randint(10000, 99999)

    def _generate_name(self, prefix):
        if prefix == "scheduled task":
            return f"{random.randint(0, 999):03d}"
        else:
            return ''.join(random.choices(string.ascii_lowercase, k=3))

    def _log(self, name, action, job_id):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{timestamp},{name},{action},{job_id}")
        self.jobs.append([timestamp, name, action])

    def start_process_simulator(self, time_to_simulate: int):
        end_time = datetime.now() + timedelta(seconds=time_to_simulate)

        while datetime.now() < end_time:
            time.sleep(random.uniform(0.5, 1.5))

            if self.active_jobs and random.random() < 0.5:
                job = self.active_jobs.pop(0)
                self._log(job["name"], "END", job["id"])
            else:
                job_type = random.choice(["scheduled task", "background job"])
                job_name = job_type + ' ' + self._generate_name(job_type)
                job_id = self._generate_id()

                self._log(job_name, "START", job_id)
                self.active_jobs.append({
                    "name": job_name,
                    "id": job_id
                })

        return self.jobs


if __name__ == "__main__":
    simulator = ProcessSimulator()
    simulator.start_process_simulator(15)
