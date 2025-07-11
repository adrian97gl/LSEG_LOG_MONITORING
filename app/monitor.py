from datetime import datetime
from app.utils.CONSTANTS import OUTPUTFILE


class Monitor:
    def __init__(self):
        self.TIME_FORMAT = "%H:%M:%S"
        self.log_dictionary = {}

    def log_monitor(self, lines):
        for line in lines:
            if line.strip():
                line = line.strip().split(',')

                task_description = line[1].strip()
                task_name = task_description.split(' ')[-1]
                task_type = task_description.split(' ')[-2]
                task_pid = line[-1]
                task_time = line[0].strip()

                if task_name not in self.log_dictionary:
                    self.log_dictionary[task_name] = {}

                if line[-2].strip() == 'START':
                    self.log_dictionary[task_name]['START'] = task_time
                elif line[-2].strip() == 'END':
                    self.log_dictionary[task_name]['END'] = task_time
                else:
                    print('The line don`t have the same format', line)

                self.log_dictionary[task_name]['TYPE'] = task_type
                self.log_dictionary[task_name]['DESCRIPTION'] = task_description
                self.log_dictionary[task_name]['PID'] = task_pid

        self.calculate_duration()
        self.generate_report()

        return self.log_dictionary

    def calculate_duration(self):
        for task_name, task_object in self.log_dictionary.items():
            if 'START' in task_object and 'END' in task_object:
                start_time = datetime.strptime(task_object['START'], self.TIME_FORMAT)
                end_time = datetime.strptime(task_object['END'], self.TIME_FORMAT)
                duration = end_time - start_time

                minutes = int(duration.total_seconds() / 60)

                if minutes > 10:
                    self.log_dictionary[task_name]['BEHAVIOR'] = 'ERROR'
                elif minutes > 5:
                    self.log_dictionary[task_name]['BEHAVIOR'] = 'WARNING'
                else:
                    self.log_dictionary[task_name]['BEHAVIOR'] = 'OK'

                self.log_dictionary[task_name]['DURATION'] = duration.total_seconds()

            else:
                self.log_dictionary[task_name]['DURATION'] = 'N/A'

                self.log_dictionary[task_name]['BEHAVIOR'] = 'ERROR'

        return self.log_dictionary

    def generate_report(self, output_path="log/" + OUTPUTFILE):
        with open(output_path, 'a') as file:
            for task_name, task_object in self.log_dictionary.items():
                task_behavior = task_object.get('BEHAVIOR', 'UNKNOWN')
                task_duration = task_object.get('DURATION', 'N/A')

                if task_duration != 'N/A':
                    task_duration = "{:.2f}".format(task_duration / 60)

                task_pid = task_object.get('PID', 'N/A')
                task_type = task_object.get('TYPE', 'N/A')

                if task_behavior != 'OK':
                    text_line = (f'[{task_behavior}] Application {task_name}, type {task_type} with PID {task_pid}, '
                                 f'duration of application {task_duration} minutes')

                    file.write(text_line + '\n')

