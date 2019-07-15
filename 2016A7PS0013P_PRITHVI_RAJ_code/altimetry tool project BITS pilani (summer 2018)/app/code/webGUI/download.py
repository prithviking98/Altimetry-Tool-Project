'''' IIRS SUMMER 2018 PS1 PROJECT

authors: Prithvi Raj Nair , Abhiroop Bhattacharjee

purpose: cross platform tool with GUI for real time elevation monitoring of inland waterways using satellite altimetry

methodology: automating the process of checking for new data,downloading new data and processing netCDF files to get elevation
'''

'''download module
downloads nc file given the link and stores it as ncf.nc in app_dir/temp/ncf.nc.
overwrites the file every time to avoid clutter.
'''

import urllib3 as ulib
import os.path as op
import django
import os


#disabling InsecureRequestWarning (cause it's annoying af)
ulib.disable_warnings(ulib.exceptions.InsecureRequestWarning)

#getting path of app folder
#use join() to form path in cross platform way (uses the cocrrecet slash)
app_dir=op.join(op.dirname(op.realpath(__file__)),'..','..')

def download(satName, file_URL, file_name):
	print()
	print("INSIDE DOWNLOAD")
	print("satName={}".format(satName))
	print("file_name={}".format(file_name))
	print("file_URL={}".format(file_URL))

	#creating PoolManager
	print("creating PoolManager (connection timout= 15.0s)")
	http=ulib.PoolManager(timeout=ulib.Timeout(connect=15.0))

	#downloading the file
	print('downloading',file_name)
	NCFile=http.request("GET",file_URL)
	print("download complete")

	#wrting file as nc file
	print('writing to .nc file')
	with open(op.join(app_dir,'data','temp','ncf.nc'),'wb') as file:
		file.write(NCFile.data)
	print('write complete')
	print()
	return