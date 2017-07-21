

import time
import os
import urllib.request
import pandas as pd
import numpy as np
import datetime

#search_keyword = ['Akshay Kumar']
#keywords = ['high resolution']

def fetch_url(url):
	try:
		headers = {}
		headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
		req = urllib.request.Request(url, headers = headers)
		resp = urllib.request.urlopen(req)
		respData = str(resp.read())
		return respData 
	except Exception as e:
		print(str(e))


def _images_get_all_items(page):
	items = []
	while True:
		item, end_content = _images_get_next_item(page)
		if item == "no_links":
			break
		else:
			items.append(item)
			time.sleep(0.1) 
			page = page[end_content:]
	return items


def _images_get_next_item(s):
	start_line = s.find('rg_di')
	if start_line == -1:
		end_quote = 0
		link = "no_links"
		return link, end_quote
	else:
		start_line = s.find('"class="rg_meta"')
		start_content = s.find('"ou"',start_line+1)
		end_content = s.find(',"ow"',start_content+1)
		content_raw = str(s[start_content+6:end_content-1])
		return content_raw, end_content

def status_entry(profile):
	status_path = 'status_entry.csv'
	raw = open(status_path, 'a')
	line = str(profile) + ','
	raw.write(line)
	raw.write('\n')
	raw.close()

def status_close(profile):

	status_path = 'status_complete.csv'
	raw = open(status_path, 'a')
	line = str(profile)
	raw.write(line)
	raw.write('\n')
	raw.close()

def askStatus(profile):

	status = 0

	status_entry = 'status_entry.csv'
	status_complete = 'status_complete.csv'

	end = pd.read_csv(status_complete, sep = ',', header = None)
	end = np.asarray(end)

	start = pd.read_csv(status_entry, sep = ',', header = None)
	start = np.asarray(start)

	profile = [profile]
	if profile in end:
		status = 1
	elif profile in start:
		tem_path = settings.profile_path
		profile_path = os.path.join(tem_path, str(profile[0]))
		file_list = os.listdir(profile_path)
		if len(file_list) > 1:
			status = 1
		else:
			status = 0
	else:
		status = 0

	return status




if __name__ == '__main__':

	#searchList = ['Gnelia Dsouza']
	searchList = ['God Shiv']

	out = 'data'

	errorCount = 0

	for x in searchList:
		search = x.replace(' ','%20')
		profile = x.replace(' ', '_')
		print(profile)

		items = []


		url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
			
		try:
			raw_html = fetch_url(url)
		except:
			print('Error1')
			pass

		time.sleep(0.1)

		try:
			items = items + (_images_get_all_items(raw_html))
		except:
			print('Error2')
			pass

		print ('Total Number of Images found, \t', profile,',\t', len(items))

		profile_path = os.path.join(out, str(profile))
		if not os.path.exists(profile_path):
			os.mkdir(profile_path)

		print ("Starting Download...")

		k=0
		
		while(k<len(items)):
			import urllib.request as urllib2
			#from urllib2 import Request,urlopen
			#from urllib2 import URLError, HTTPError

			try:
				req = urllib2.Request(items[k], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
				response = urllib2.urlopen(req)

				out_img_file = profile_path + '/' + str(k+1) + '.jpg'

				output_file = open(out_img_file,'wb')
				data = response.read()
				output_file.write(data)
				response.close()

				print("completed ====> "+str(k+1), '\tat ===>', datetime.datetime.now())
				k += 1

			except IOError:
				errorCount+=1
				print("IOError on image "+str(k+1))
				k += 1

			except urllib2.HTTPError as e:
				errorCount+=1
				print("HTTPError"+str(k))
				k += 1

			except urllib2.URLError as e:
				errorCount+=1
				print("URLError "+str(k))
				k += 1

			except:
				errorCount += 1
				pass