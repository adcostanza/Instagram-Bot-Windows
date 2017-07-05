import os
import re
import shutil
class Recycler:
	def __init__(self, folder):
		self.directories = [x[0] for x in os.walk(folder)]
		#print(self.directories)
		
	def trash(self,match):
		regex = re.compile(match)
		matches = [x for x in self.directories if regex.search(x) and x.count("\\") == 6]
		#print(matches)
		for match in matches:
			
			try:
			
				shutil.rmtree(match)
				print("Deleting",match)
			except:
				print("Could not delete",match)