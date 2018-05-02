import sys
from bs4 import BeautifulSoup
from mutagen.mp3 import MP3, EasyMP3
from mutagen.id3 import ID3, APIC, error
from PIL import Image
import requests
from io import BytesIO
import urllib
import os

yt_url = input("Enter Youtube Video URL : ")

yt_id = yt_url.split("watch?v=")[1]
yt_id = yt_id.split("&")[0]

# Get Filename
res = requests.get(yt_url)

filename = str(res.text)
filename = filename.split("</title")[0]
filename = filename.split("<title>")[1]
filename = filename.split(" - YouTube")[0]
print("Name : ", filename)

# Get Actual MP3
base_url = "http://youtubeinmp3.me/api/generate.php?id="

final_url = base_url + yt_id

res = requests.get(final_url)
soup = BeautifulSoup(res.text, "lxml")

mp3_a = soup.find('a')

cleaned = str(mp3_a)
cleaned = cleaned.split("window.open")[1]
cleaned = cleaned.split("')")[0]
cleaned = cleaned.split("('")[1]

# Actual File Download Starts Here
dir_path = "/Users/admin/Desktop/"

if(not os.path.exists(dir_path)):
	dir_path = "/"
	
target_path = dir_path + filename + ".mp3"
final_mp3_url = cleaned

print("Final MP3 URL : ", final_mp3_url)

try:
	with open(target_path, "wb") as f:
			print ("Downloading %s" % filename)
			response = requests.get(final_mp3_url, stream=True)
			total_length = response.headers.get('content-length')

			if total_length is None:
				f.write(response.content)
			else:
				dl = 0
				total_length = int(total_length)
				for data in response.iter_content(chunk_size=4096):
					dl += len(data)
					f.write(data)
					done = int(50 * dl / total_length)
					sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
					sys.stdout.flush()
	print("Download Complete!")
except:
	print("Some error occured, try again...")

#Downloading Album Art

print("Adding Album Art, please wait...")

thumbnail_url = "https://img.youtube.com/vi/" + yt_id + "/0.jpg"

mp3 = EasyMP3(target_path, ID3=ID3)
mp3.tags.add(
	APIC(
		encoding = 3,
		mime     = 'image/png',
		type     = 3,
		desc     = 'cover',
		data     = urllib.request.urlopen(thumbnail_url).read()
	)
)
mp3.save() 

print("All Done!")









