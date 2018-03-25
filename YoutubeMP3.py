import sys
import requests
from bs4 import BeautifulSoup

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
target_path = dir_path + filename + ".mp3"
final_mp3_url = cleaned

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










