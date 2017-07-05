import os
import time
from selenium import webdriver
from selenium.common.exceptions import (StaleElementReferenceException, NoSuchElementException)
import re
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', raw_html)
  return cleantext
def extractType(string, type):
	[word for word in string.split() if word.startswith(type)]
class Crawler:
	
	def __init__(self, user, passw, sql):
		self.sql = sql
		self.user = user
		self.passw = passw
		self.chromedriver = "C:\Python36\chromedriver.exe"
		
	def login(self):
		os.environ["webdriver.chrome.driver"] = self.chromedriver
		#self.sql.createTable()
		driver = webdriver.Chrome(self.chromedriver)
		try:
			
			driver.get("http://instagram.com")
			element = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')
			element.click()
			element = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[1]/input')
			element.send_keys(self.user)
			element = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/input')
			element.send_keys(self.passw)
			element = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button')
			element.click()
			self.driver = driver
			time.sleep(1)
		except:
			driver.quit()
			self.login()
	def exit(self):
		self.driver.quit()
	def checkSnaps(self,links):
		for link in links:
			self.driver.get('https://www.instagram.com/p/'+link)
			profile = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/a')
			profile.click()
			time.sleep(2)
			spans = self.driver.find_elements_by_css_selector('span span')
			spans_text =[]
			for span in spans:
				try:
					spans_text.append(span.text)
				except:
					print("Stale element")
			about = ''.join(spans_text)
			
			snap_icon = b'\xf0\x9f\x91\xbb'.decode('utf8')
			if snap_icon in about or re.search(about,'(snap|Snap)'):
				user = self.driver.current_url
				user = user.split('/')
				user = user[-2]
				print(user)
	def LinksFromTagsIter(self,tags,num):
		driver = self.driver
		all_links = []
		for tag in tags:
			driver.get("https://www.instagram.com/explore/tags/"+tag)
			time.sleep(1)
			try:
				driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/a').click()
				
			except:
				print("Already clicked button")
			for val in range(num):
				sc = str((val+1)*500)
				print("Scrolling to",sc,"...")
				self.driver.execute_script("window.scrollTo(0, "+sc+");")
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/a').click()
				except:
					print("Scrolling to button...")
			
			vertical_row = driver.find_elements_by_css_selector('#react-root > section > main > article > div > div > div')

			a=0;
			current_links = []
			for row in vertical_row:
				#link.append(element.get_attribute('href'))
				try: 
					links = row.find_elements_by_css_selector('a')
					for link in links:
						_link = link.get_attribute('href')
						#remove tag ref for later processing
						_link = _link.split('?',1)[0]
						#remove beginning of url
						_link = _link.split('/')[4]
										
						if _link in all_links:
							continue
						print(_link)
						current_links.append(_link)
					print(a)
					a += 1
					all_links.extend(current_links)
				except:
					print("Could not get links")
				
		c = all_links
		c = list(set(c))
		return c
	def searchTagList(self, tags):
		driver = self.driver
		all_links = []
		for tag in tags:
			driver.get("https://www.instagram.com/explore/tags/"+tag)
			time.sleep(1)
			try:
				driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/a').click()
				
			except:
				print("Already clicked button")
			
			vertical_row = driver.find_elements_by_css_selector('#react-root > section > main > article > div > div > div')

			a=0;
			current_links = []
			for row in vertical_row:
				#link.append(element.get_attribute('href'))
				try: 
					links = row.find_elements_by_css_selector('a')
					for link in links:
						_link = link.get_attribute('href')
						#remove tag ref for later processing
						_link = _link.split('?',1)[0]
						#remove beginning of url
						_link = _link.split('/')[4]
										
						if _link in all_links:
							continue
						print(_link)
						current_links.append(_link)
					print(a)
					a += 1
					all_links.extend(current_links)
				except:
					print("Could not get links")
				
		c = self.compareLinks(all_links)
		c = list(set(c))
		return c
	def compareLinks(self, all_links):
		_links = self.sql.getAllLinks()
		real_links = []
		for link in _links:
			real_links.append(link[0])
		a=all_links
		print("A::::",a)
		b=real_links
		print("b::::",b)
		#remove duplicates
		c=[]
		for item in a:
			if item not in b:
				print(item)
				c.append(item)
		
		print("FINAL LINKS: ", c)
		return c
	def likeFollowLinks(self, current_links):
		driver = self.driver
		for ind, link in enumerate(current_links):
			if(ind>320): break
			print(ind)
			try:
				driver.get('https://www.instagram.com/p/'+link)
			except TypeError:
				print(link, "Link was list..?")
			#like all posts
			time.sleep(1)
			try:
				like = driver.find_element_by_css_selector('.coreSpriteLikeHeartOpen')
			except (StaleElementReferenceException, NoSuchElementException):
				print("Already liked")
			try:
				like.click()
			except (NameError,StaleElementReferenceException, NoSuchElementException):
				print("Already liked")
			
			try:
				follow = driver.find_element_by_css_selector('#react-root > section > main > div > div > article > header > span > button')
				if(follow.get_attribute('innerHTML') == 'Follow'):
					follow.click()
			except (StaleElementReferenceException, NoSuchElementException):
				print("Already followed")
			
			
			self.sql.addPost(link,1)
		time.sleep(100)
		driver.quit()
	def readLikes(self):
		driver = self.driver
		try:
			likes = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span/span')
			likes = likes.get_attribute('innerHTML')
			return likes
		except (StaleElementReferenceException, NoSuchElementException):
			print("No likes")
			return -1
	def likeLinks(self, current_links):
		driver = self.driver
		for ind, link in enumerate(current_links):
			if(ind > 320): break
			print(ind)
			try:
				driver.get('https://www.instagram.com/p/'+link)
			except TypeError:
				print("Link was list..?")
			#like all posts
			time.sleep(1)
			try:
				like = driver.find_element_by_css_selector('.coreSpriteLikeHeartOpen')
			except (StaleElementReferenceException, NoSuchElementException):
				print("Already liked")
			try:
				like.click()
			except (NameError,StaleElementReferenceException, NoSuchElementException):
				print("Already liked")
			
			self.sql.addPost(link,1)
		print(len(current_links))
		driver.quit()	
	
	def getLinks(self, link):
		driver = self.driver
		try:
			driver.get('https://www.instagram.com/p/'+link)
		except TypeError:
			print("Link was list..?")
		#get hash tag text
		time.sleep(1)
		hashtags = []
		try:
			links = driver.find_elements_by_css_selector('a')
			return links
		except:
			print("No links")
		self.driver.quit()	
	def splitTags(self,links):
		hrefs = [x.get_attribute('innerHTML') for x in links]
		tags = [x[1:] for x in hrefs if "#" in x ]
		
		return tags
			
	def getHashTagsFromLink(self,link):
		links = self.getLinks(link)
		tags = self.splitTags(links)
		print(tags)
		return tags

