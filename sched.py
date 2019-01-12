#! /usr/bin/python3
#Amr Hammam -23180137
from collections import deque
import socket
import sys
import time
import os.path


class PCB():

	def __init__(self, line):
		self.line = line.split(',')
		self.start_time = int(self.line[0])
		self.name = self.line[1]
		self.pid = int(self.line[2])
		self.state = self.line[3]
		self.priority = int(self.line[4])
		self.interrupt = int(self.line[5])
		self.tot_time = int(self.line[6])
		self.remain_time = int(self.line[7])

	def __str__(self):
		return ','.join(self.line)

	def __repr__(self):
		return str(self.pid)


class Scheduler():

	def __init__(self,host,port,algorithm):
		self.host = host
		self.port = int(port)
		self.algorithm = algorithm

	def schedule(self):
		start = time.time()
		ready_queue = deque([])
		contextSwitch = 0
		arrival = 0
		service_time = 0
		wait_time = 0
		procCount = 0
		timeStart = 0
		timeEnd = 0

#------Queue set up
		with open('processes.txt', 'rt') as infile:
			lines = infile.read().split('\n')

		process_list = [line.split(',') for line in lines]
		current_time = 0
		current_proc = process_list.pop(0)

		while process_list:

			if int(current_proc[0]) == current_time:
				temp = time.time()
				timeStart += temp
				newProcess = ','.join(current_proc)
				ready_queue.append(PCB(newProcess))
				procCount += 1
				print('\t Added to queue: %s' % newProcess)
				current_proc = process_list.pop(0)

			current_time += 1

		timeStart = timeStart / procCount
#-------End Queue set up

		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((self.host, self.port))
			print('Connected to %s:%s' % (self.host, self.port))

			while ready_queue:
				if self.algorithm == "priority":
					ready_queue = deque(sorted(ready_queue, key=lambda x:x.priority))

				elif self.algorithm == "sjn" or self.algorithm == "srtn":
					ready_queue = deque(sorted(ready_queue, key=lambda x:x.tot_time))
				sender = ready_queue.popleft()
				sender = str(sender)
				print('\tCPU: Exec %s' % sender)
				service_time = time.time()
				wait_time += service_time - start
				sock.send(sender.encode('utf-8'))

				data = sock.recv(1024)
				contextSwitch += 1
				data = data.decode()
				data = data.split(',')
				index = len(data) - 1
				value = int(data[index])

				if value > 0:
					data = ",".join(data)
					ready_queue.append(PCB(data))

				else:
					proc_completed = time.time()
					timeEnd += proc_completed
					print("\t\tScheduler: Process " + data[1] + ", " + data[0] + ", " + "Completed")
		timeEnd = timeEnd / procCount
		avg_time = str(timeEnd - timeStart)
		end = time.time()
		total_time_spent = str(end - start)
		contextSwitch = str(contextSwitch - 1)
		wait_time = str(wait_time/procCount)

		fOut = open('stats.txt', 'a')
		fOut.write('\n' + algorithm + '\t\t' + avg_time + '\t' + wait_time + '\t' + total_time_spent + '\t\t' + contextSwitch)
		fOut.close()

		print("Avg turnaround: " + avg_time + "seconds")
		print("Avg wait: " + wait_time + "seconds")
		print("Total time: " + total_time_spent + "seconds")
		print("# of context switches: " + contextSwitch)
		print("Connection closed.")


if __name__ == '__main__':
	host = '127.0.0.1'
	port = 9000
	if len(sys.argv) < 2:
		algorithm = "fcfs"
		print("\nrunning default algorithm: FCFS")
		print("possible algorithms: FCFS \t SJN \t PRIORITY \t SRTN")
		print("\t\t./run [algorithm]")
		print("Algorithm: FCFS\n")
	else:
		if sys.argv[1] == "fcfs" or sys.argv[1] == "sjn" or sys.argv[1] == "priority" or sys.argv[1] == "srtn":
			algorithm = sys.argv[1]
			print("Algorithm: " + algorithm)
		else: 
			algorithm = "fcfs"
			print("Algorithm: FCFS")
			print("input check:" + sys.argv[1])

	scheduler = Scheduler(host, port, algorithm)
	scheduler.schedule()