'''' IIRS SUMMER 2018 PS1 PROJECT

authors: Prithvi Raj Nair , Abhiroop Bhattacharjee

purpose: cross platform tool with GUI for real time elevation monitoring of inland waterways using satellite altimetry

methodology: automating the process of checking for new data,downloading new data and processing netCDF files to get elevation
'''

'''module to process the netCDF file
'''

import netCDF4 as ncd
import os.path as op
import os 
import numpy as np
import datetime
import django
import shutil

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webGUI.settings")
django.setup()

from addLoc.models import *
from django.db import IntegrityError

#getting path of app folder
#use join() to form path in cross platform way (uses the cocrrecet slash)
app_dir=op.join(op.dirname(op.realpath(__file__)),'..','..')

def process(satName, file_name,cycle_num):
    print()
    print("inside process")
    print("satName={} cycle={} file_name={}".format(satName,cycle_num,file_name))
    print()

    #reading the required locations from database
    locations=Location.objects.all().filter(satellite__nameShort=satName)	
    for i in locations:
            print(i)

    #opening the netCDF file
    print('opening the netCDF file')
    with ncd.Dataset(op.join(app_dir,'data','temp','ncf.nc'),'r') as d:
            print('opened file successfully')

            #checking to see if india lies in this track
            lat=list(d.variables["lat"])
            lon=list(d.variables["lon"])
            flag=True
            for i in range(0,len(lat)):
                if lat[i]>5 and lat[i]<40 and lon[i]>65 and lon[i]<100:
                    print("track contains India")
                    print("making a copy of the file and storing in data/"+satName+"/"+cycle_num)
                    flag=False
                    if cycle_num not in os.listdir(app_dir+'/data/'+satName):
                        try:
                            os.mkdir(app_dir+'/data/'+satName+'/'+cycle_num)
                        except OSError:
                            print("unable to create directory")
                    shutil.copyfile(app_dir+'/data/temp/ncf.nc',app_dir+'/data/'+satName+'/'+cycle_num+'/'+file_name)
                    break
            if flag:
                print("track does not contain India")
                return

            #extracting required variables and converting to list
            required=["time","alt_20hz","lat_20hz","lon_20hz","ice_range_20hz_ku","rad_wet_tropo_corr","model_wet_tropo_corr","model_dry_tropo_corr",
            "pole_tide","iono_corr_gim_ku",'iono_corr_alt_ku','iono_corr_alt_ku_mle3',"solid_earth_tide","mean_sea_surface","geoid"]

            time=list(d.variables["time"])
            alt=list(d.variables["alt_20hz"])
            lat=list(d.variables["lat_20hz"])
            lon=list(d.variables["lon_20hz"])
            ice=list(d.variables['ice_range_20hz_ku'])
            rad1=list(d.variables['model_wet_tropo_corr'])
            rad2=list(d.variables["rad_wet_tropo_corr"])
            model=list(d.variables["model_dry_tropo_corr"])
            pole=list(d.variables["pole_tide"])
            iono1=list(d.variables["iono_corr_gim_ku"])
            iono2=list(d.variables["iono_corr_alt_ku"])
            iono3=list(d.variables["iono_corr_alt_ku_mle3"])
            solid=list(d.variables["solid_earth_tide"])
            mss=list(d.variables["mean_sea_surface"])
            geoid=list(d.variables['geoid'])

            flag=-1
            non_maskable=["model_dry_tropo_corr","pole_tide","solid_earth_tide","mean_sea_surface","geoid"]
            close_geo=[] #to store geoid elevation of points close to the required points
            close_mss=[] #to store mean sea surface elevation of points close to the required points
            for i in range(0,len(time)):
                    lat20=list(lat[i])
                    lon20=list(lon[i])
                    # print(lat20[10],lon20[10])
                    for j in range(0,20):
                            if np.ma.is_masked(lat20[j]) or np.ma.is_masked(lon20[j]): 
                                    continue
                            for k in range(0,len(locations)):
                                    if abs(float(lat20[j])-float(locations[k].latitude))<0.0045 and abs(float(lon20[j])-float(locations[k].longitude))<0.0045:
                                            if flag==-1:
                                                    flag=k
                                                    print("location found : ",locations[k])
                                                    close_geo.clear()
                                                    close_mss.clear()
                                            alt20=list(alt[i])
                                            ice20=list(ice[i])
                                            print("alt20={} ice20={} model={} pole={} solid={} mss={} geoid={}".format(alt20[j],ice20[j],model[i],pole[i],solid[i],mss[i],geoid[i]))
                                            if np.ma.is_masked(alt20[j]) or np.ma.is_masked(ice20[j]) or np.ma.is_masked(model[i]) or np.ma.is_masked(pole[i]) or np.ma.is_masked(solid[i]) or (np.ma.is_masked(mss[i]) and np.ma.is_masked(geoid[i])):
                                                    print("something unmaskable is masked")
                                                    print('cannot record measurment at this location')
                                                    continue
                                            ele_geo=alt20[j]-ice20[j]-model[i]-pole[i]-solid[i]-geoid[i]
                                            ele_mss=alt20[j]-ice20[j]-model[i]-pole[i]-solid[i]-mss[i]
                                            if not np.ma.is_masked(rad1[i]):
                                                    ele_mss=ele_mss-rad1[i]
                                                    ele_geo=ele_geo-rad1[i]
                                            elif not np.ma.is_masked(rad2[i]):
                                                    print("rad1 is masked")
                                                    ele_mss=ele_mss-rad2[i]
                                                    ele_geo=ele_geo-rad2[i]
                                            else:
                                                    print('all rad masked')
                                                    print('cannot record measurment at this location')
                                                    continue

                                            if not np.ma.is_masked(iono1[i]):
                                                    ele_mss=ele_mss-iono1[i]
                                                    ele_geo=ele_geo-iono1[i]
                                            elif not np.ma.is_masked(iono2[i]):
                                                    print("iono1 is masked")
                                                    ele_mss=ele_mss-iono2[i]
                                                    ele_geo=ele_geo-iono2[i]
                                            elif not np.ma.is_masked(iono3[i]):
                                                    print("iono2 is masked")
                                                    ele_mss=ele_mss-iono3[i]
                                                    ele_geo=ele_geo-iono3[i]
                                            else:
                                                    print("all iono masked")
                                            if not np.ma.is_masked(ele_mss):
                                                    close_mss.append(ele_mss)
                                            if not np.ma.is_masked(ele_geo):
                                                    close_geo.append(ele_geo)
                                    elif flag==k:
                                            flag=-1

                                            #finding date
                                            utctimestamp=datetime.datetime.timestamp(datetime.datetime(2000,1,1,0,0,0))
                                            date=datetime.date.fromtimestamp(time[i]+utctimestamp)
                                            #process close points and find average elevation
                                            if len(close_geo)>0:
                                                    mean_geo=sum(close_geo)/len(close_geo)
                                                    print("writing geo value to database")
                                                    e=ElevationGeoid(elevation=mean_geo,date=date,location=locations[k])
                                                    try:
                                                            e.save()
                                                    except IntegrityError:
                                                            print('data for this date already exists')

                                            if len(close_mss)>0:
                                                    mean_mss=sum(close_mss)/len(close_mss)
                                                    print("writing mss value to database")
                                                    e=ElevationMss(elevation=mean_mss,date=date,location=locations[k])
                                                    try:
                                                            e.save()
                                                    except IntegrityError:
                                                            print('data for this date already exists')
    return 

#process("JA3","JA3_OPN_2PdS086_001_20180609_071556_20180609_091042.nc","cycle086")
