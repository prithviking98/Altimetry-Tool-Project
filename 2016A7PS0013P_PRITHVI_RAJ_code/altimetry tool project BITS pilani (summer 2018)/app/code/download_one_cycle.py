'''' IIRS SUMMER 2018 PS1 PROJECT

authors: Prithvi Raj Nair , Abhiroop Bhattacharjee

purpose: cross platform tool with map based GUI for real time elevation monitoring of inland waterways using satellite altimetry

methodology: automating the process of checking for new data,downloading new data and processing netCDF files to get elevation
'''

'''main module
checks if new files are available for all satellites being used
downloads new .nc files using download module
processes them using process module
'''

import urllib3 as ulib 
import os.path as op
import download
# import process

#disabling InsecureRequestWarning (cause it's annoying af)
ulib.disable_warnings(ulib.exceptions.InsecureRequestWarning)

#getting path of app folder
#use join() to form path in cross platform way (uses the cocrrecet slash)
app_dir=op.join(op.dirname(op.realpath(__file__)),'..')

#jason  ogdr view cycles page
j3_ogdr_cycles_page_URL='https://data.nodc.noaa.gov/jason3/ogdr/ogdr/'
j2_ogdr_cycles_page_URL='https://data.nodc.noaa.gov/jason2/ogdr/ogdr/'

def download(satName, file_URL, file_name,lcycle):
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
	with open(op.join(app_dir,'data',satName,lcycle,file_name),'wb') as file:
		file.write(NCFile.data)
	print('write complete')
	print()
	return

def checkData(satName , lcycle, ogdr_files_page_URL, html, lfile):
	print()
	print("INSIDE CHECK DATA FUNCTION")
	print("satName={} ".format(satName))
	print("lcycle={} lfile={}".format(lcycle,lfile))
	print("ogdr_files_page_URL={} ".format(ogdr_files_page_URL,lfile))
	print()
	print("reading files")
	for line in html:
		if satName in line:
			start=line.index(satName)
			end=line.index('.nc')+3
			name=line[start:end]
			if name>lfile:
				print("new file found :",name)
				print("*****donwloading new netCDF file ....*****")
				download(satName,ogdr_files_page_URL+'/'+name, name,lcycle)
				print("*****download completed.*****")
				print()
				# print("*****processing the new file*****")
				# process.process(satName, lfile)
				# print("*****processing complete.*****")
				# print()
				lfile=name
				# writing updates to JAx_last.txt
				print("writing last downloads info to", satName+'_last.txt')
				print('lcycle={} lfile={}'.format(lcycle,lfile))
				with open(op.join(app_dir,'data','last',satName+'_last.txt'),"w") as f:
					f.write(lcycle+'\n')
					f.write(lfile+'\n')	
				print('write complete')
				print("******")
	return lfile


def jasonNewFileCheck(satName , ogdr_cycles_page_URL):
	'''function to check for new jason 2/3 file
	it will keep downloading and processing files from the last downloaded file
	until the latest file''' 

	print("***************** CHECKING FOR NEW FILE OF",satName,"********************")
	print("URL of cycles web page :", ogdr_cycles_page_URL)
	print()

	#getting information about last downloaded file
	print("opening last loaded file :",satName+'_last.txt ....')
	with open(op.join(app_dir,'data','last',satName+'_last.txt'),'r') as last:
		lcycle=last.readline()[:-1] #last accessed cycle
		lfile=last.readline()[:-1] #last downloaded file name
	print("last downloaded file loaded")
	print("last cycle =",lcycle)
	print("last file =",lfile)
	print()

	#creating PoolManager
	print("creating PoolManager (connection timout= 15.0s)")
	http=ulib.PoolManager(timeout=ulib.Timeout(connect=15.0))

	#downlaoding the page with list of cylces
	print("donwloading webpage with list of cycles ....")
	ogdr_cycles_page=http.request('GET',ogdr_cycles_page_URL)
	# saving the html in a file
	with open(op.join(app_dir,'data','temp','ogdr_cycles_page.html'),'wb') as f:
		f.write(ogdr_cycles_page.data)
	print("download complete.")
	print()

	#opening the cycles file for reading
	print("opening HTML file for reading")
	with open(op.join(app_dir,'data','temp','ogdr_cycles_page.html'),'r') as html:
		cflag=False
		for line in html:
			flag=True
			if 'cycle' in line:
				cflag=True
				if lcycle not in line:
					continue
				flag=False
				#last accessed cycle link found
				#downloading the corresponding cycle web page and saving the web page
				print("cycle found :",lcycle)
				print("downloading webpage...")
				lcycle_page=http.request('GET',ogdr_cycles_page_URL+lcycle)
				with open(op.join(app_dir,'data','temp','lcycle.html'),'wb') as f:
					f.write(lcycle_page.data)
				print("download complete.")
				print("opening HTML file and passing to checkData")
				with open(op.join(app_dir,'data','temp','lcycle.html'),'r') as f:
					lfile=checkData(satName, lcycle,ogdr_cycles_page_URL+lcycle, f , lfile)
				print("checking for new files in ",lcycle,"done.")
				print("latest downloaded file :",lfile)
				print()

				#updating lcycle variable
				num=int(lcycle[5:])
				num=num+1
				t=num
				count=0
				while t>0: #counting digits in num
					t=t//10
					count=count+1
				if count==1:
					lcycle='cycle00'+str(num)
				elif count==2:
					lcycle='cycle0'+str(num)
				elif count==3:
					lcycle='cycle'+str(num)
			if cflag and flag and 'cycle' not in line:
				#decrementing lcycle variable it is greater than available cycles
				num=int(lcycle[5:]) #cycle number
				num=num-1
				t=num
				count=0
				while t>0: #counting digits in num
					t=t//10
					count=count+1
				if count==1:
					lcycle='cycle00'+str(num)
				if count==2:
					lcycle='cycle0'+str(num)
				elif count==3:
					lcycle='cycle'+str(num)
				print("no more new cycles available")
				print("last downloaded cycle :",lcycle)
				print()
				break
			if cflag:
				print("next cycle to check :",lcycle)
				c=input("want to download new cycle ? (y/n) > ")
				if c=='y' or c=='Y':
					continue
				else:
					break

	# writing updates to JAx_last.txt
	print("writing last downloads info to", satName+'_last.txt')
	print('lcycle={} lfile={}'.format(lcycle,lfile))
	with open(op.join(app_dir,'data','last',satName+'_last.txt'),"w") as f:
		f.write(lcycle+'\n')
		f.write(lfile+'\n')	
	print('write complete')
	print()
	print("*************** NEW FILE CHECK COMPLETED FOR",satName,"******************")
	print()
	return

#program is a continuos loop to check for new files from each satellite
while True:
	# jasonNewFileCheck("JA3",j3_ogdr_cycles_page_URL)
	jasonNewFileCheck("JA2",j2_ogdr_cycles_page_URL)
	break;