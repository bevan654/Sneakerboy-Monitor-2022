import requests
import threading
import json
from termcolor import *
import colorama
from datetime import *

colorama.init()



class Monitor:
	def __init__(self,menu):
		self.menu = menu

	def LOG(self,text,color):
		print(colored(f'[{datetime.now()}][{self.menu}] {text}',color))

	def start_monitor(self):
		pass




options = []
for i in options:
	threading.Thread(target=Menu,args=(i,)).start()
	