from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from datetime import date


frame=pd.DataFrame()
todays_date=date.today()
for i in range(1,3):
    html_text=requests.get('https://www.pakwheels.com/used-cars/karachi/24857?page='+str(i)).text
    soup=BeautifulSoup(html_text,'lxml')

    boxes=soup.find_all('div',class_='well search-list clearfix ad-container page-'+str(i))
    for box in boxes:
        #finding location of vehicle and storing in loc
        name=box.find('ul',class_='list-unstyled search-vehicle-info fs13')
        loc=name.find('li').text.replace(" ","")
            
        #print("test"+str(i))
            #finding extra details of vehicle
        details=box.find('ul',class_='list-unstyled search-vehicle-info-2 fs13').text.replace(' ','')
        test=list()
        for line in details.splitlines():
            test.append(line)


            #finding name of vehicle 
        name=box.find('a',class_="car-name ad-detail-path").text.replace(' ','')


            #finding price of vehicle
        price=box.find('div',class_="price-details generic-dark-grey").text.replace(' ','')
        #print("head")


            #print(str(name)+str(loc)+str(details)+str(price))
        frame=frame.append({'name':name,'location':loc,'year_of_manufacture':test[1],'mileage':test[2],'fuel_type':test[3],'volume_of_fuel':test[4],'Gear_type':test[5],'price':price},ignore_index=True)


    print(frame.tail(3))
frame['volume_of_fuel']=frame['volume_of_fuel'].str.replace("cc",'')
frame['location']=frame['location'].str.replace(r"\n",'')
frame['price']=frame['price'].str.replace(r"\n",'')
frame['price']=frame['price'].str.replace('PKR','')
frame['price']=frame['price'].str.replace('Call','0')
    #print(frame[['price']])


frame['price']=frame['price'].astype(str)

for i in frame.index:
    if frame.price.loc[i].endswith('crore'):
        frame.price.loc[i]=re.sub(r'crore','',frame.price.loc[i])
        frame.price.loc[i]=float(frame.price.loc[i])*10000000

frame['price']=frame['price'].astype(str)

for i in frame.index:
    if frame.price.loc[i].endswith('lacs'):
        frame.price.loc[i]=re.sub(r'lacs','',frame.price.loc[i])
        frame.price.loc[i]=float(frame.price.loc[i])*100000
    #print(frame.price)


frame['mileage']=frame['mileage'].str.replace('km','')
frame['mileage']=frame['mileage'].str.replace(',','')
frame[['year_of_manufacture','volume_of_fuel','mileage']]=frame[['year_of_manufacture','volume_of_fuel','mileage']].apply(pd.to_numeric)
frame['year_of_manufacture']=todays_date.year-frame['year_of_manufacture']
frame.to_csv(r'C:\Users\rethek\Desktop\data\check.csv',index=False,header=True)
