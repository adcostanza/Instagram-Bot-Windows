from pg import pg
from crawler import Crawler
from timekeeper import TimeKeeper
import time
from recycler import Recycler
class Manager:
	def __init__(self, user, pw):
		self.user = user
		self.pw = pw
		self.sql = pg(user,"sql-user","sql-pw")
		self.tk = TimeKeeper()
		self.crawler = Crawler(user, pw, self.sql);
		self.recycler = Recycler("C:\\Users\\Adam\\AppData\\Local\\Temp")
	
	def HourlyLikes(self):
		likes = int(self.sql.HourlyLikes())
		return likes
	def run(self):
		self.recycler.trash("scoped_dir")
		likes = self.HourlyLikes()
		if(likes >= 300):
			print("Already liked 300 pages in the last hr, will check again in 20 minutes")
			time.sleep(20*60)
			self.run()
		else:
			quota = 300-likes
			print("Initiating crawler")
			self.crawler.login()
			posts = self.getFreshLinks()
			posts = posts[0:quota]
			print(posts)
			print(quota)
			
			self.crawler.likeLinks(posts)
			self.crawler.exit()
			self.run()
	def runTags(self, tags):
		likes = self.HourlyLikes()
		if(likes >= 300):
			print("Already liked 300 pages in the last hr, will check again in 20 minutes")
			time.sleep(20*60)
			self.runTags(tags)
		else:
			quota = 300-likes
			print("Initiating crawler")
			self.crawler.login()
			posts = self.getLinksFromTags(tags)
			posts = posts[0:quota]
			print(posts)
			print(quota)
			
			self.crawler.likeLinks(posts)
			self.crawler.exit()
			self.runTags(tags)
	def newTags(self, tags):
		for tag in tags:
			self.sql.addTag(tag)
	#also shows if tag exists if tag time is False
	def getSnaps(self,tags, num):
		self.crawler.login()
		links = self.crawler.LinksFromTagsIter(tags,num)
		snaps = self.crawler.checkSnaps(links)
	def getTagTimes(self, tags):
		tags_times = []
		for tag in tags:
			time = self.sql.getTagTime(tag)
			tags_times.append([tag,time])
		return tags_times
	def getAllTagsTimes(self):
		tags = self.sql.getAllTagsTimes()
		return(tags)
	def getFreshTags(self):
		tagstimes = self.getAllTagsTimes()
		tagstimes_fresh = self.tk.FreshTags(tagstimes, 5) #5 tags at a time
		tags = []
		for tagtime in tagstimes_fresh:
			tag = tagtime[0]
			tags.append(tag)
		return tags
	def getFreshTagNum(self,num):
		tagstimes = self.getAllTagsTimes()
		tagstimes_fresh = self.tk.FreshTags(tagstimes, num) #1 tag at a time
		tags = []
		for tagtime in tagstimes_fresh:
			tag = tagtime[0]
			tags.append(tag)
		return tags
	def getLinksFromTags(self,tags):
		links = self.crawler.searchTagList(tags)
		return links
	def getFreshLinks(self):
		tags = self.getFreshTags()
		self.newTags(tags)
		links = self.getLinksFromTags(tags)
		return links
	def getFreshLinksNTags(self, n):
		tags = self.getFreshTagNum(n)
		self.newTags(tags)
		links = self.getLinksFromTags(tags)
		return links
	def getHashTagsFromLink(self,link):
		self.crawler.login()
		self.crawler.getHashTagsFromLink(link)
		self.crawler.exit()
	def getFreshHashTags(self):
		self.crawler.login()
		links = self.getFreshLinksNTags(50)
		tags = []
		for link in links:
			_tags = self.crawler.getHashTagsFromLink(link)
			tags.extend(_tags)	
		import collections
		counter = collections.Counter(tags)
		print(counter.most_common(10))
		self.crawler.exit()
		return tags