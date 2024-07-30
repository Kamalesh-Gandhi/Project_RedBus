# Intially import all the required modules for this project
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

# This function HomePage_driver will open the redbus page and maximize the window and scroll down the page
def HomePage_driver(driver):
    try:

        driver.get("https://www.redbus.in/")
        driver.maximize_window()
        driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    except Exception as e:
        print("The HomePagedriver Error Reason: ",e)    

# This function StatePage_Link will fetch the state name and state link
def StatesPage_Link(states_driver):
    try:

        driver.get(states_driver)
        time.sleep(1)
        states = driver.find_elements(By.XPATH,"//div[@class='D113_ul_rtc']/ul/li/a")
        print(len(states))
        States_link = []
        States_Names = []

        #Getting the values of the href(Links of the States
        for i in states[13:14]:
            States_link.append(i.get_attribute('href'))   
            States_Names.append(i.text)
        print(States_Names,'\n')    
    
    except Exception as e:
        print("The StatesPageLink Error Reason: ", e)

    return States_link,States_Names

# This function BusRoutes_link will scrape the route name and route link in all the pages of the states
def BusRoutes_link(States_Page_Links,StatesNames):
    try:
        Busrouteslinks = []
        Routes_link  = []
        Route_NO= 1
        x = 0
        wait = WebDriverWait(driver, 10)

        print("Total States routes links: ",len(States_Page_Links))

        for i in States_Page_Links:
            driver.get(i)
            time.sleep(2)

            #Extracting the reference of the PageTabs 
            Page_tabs = driver.find_elements(By.XPATH,"//div[@class='DC_117_paginationTable']/div")

            try:
                route=driver.find_elements(By.XPATH,"//div[@class='route_link']/div/a")
                for j in route:
                    route_l=j.get_attribute('href')
                    Routes_link.append(route_l)
                    route_name_link=(Route_NO,StatesNames[x],j.get_attribute('title'),j.get_attribute('href'))
                    Busrouteslinks.append(route_name_link)
                    Route_NO += 1
            except Exception as e:
                pass

            #Extract the BusRoutes links from the each Pages of the state
            no=0
            page_number=0
            while no < len(Page_tabs):
                try:
                    
                    pagination_container=wait.until(EC.presence_of_element_located((By.XPATH,"//div[@id='root']/div/div[4]/div[12]")))
                    next_page_button=pagination_container.find_element(By.XPATH,f'//div[contains(@class,"DC_117_pageTabs") and text()="{page_number + 1}"]')
                    driver.execute_script("arguments[0].scrollIntoView();",next_page_button)
                    next_page_button.click()
                    wait.until(EC.text_to_be_present_in_element((By.XPATH, "//div[@class='DC_117_pageTabs DC_117_pageActive']"), str(page_number + 1)))
                    time.sleep(1)

                    route=driver.find_elements(By.XPATH,"//div[@class='route_link']/div/a")
                    for j in route:
                        route_l=j.get_attribute('href')
                        Routes_link.append(route_l)
                        route_name_link=(Route_NO,StatesNames[x],j.get_attribute('title'),j.get_attribute('href'))
                        Busrouteslinks.append(route_name_link)
                        Route_NO += 1
               
                except Exception as e:
                    print("The Bus_routes_links Error ")
                    continue

                no += 1
                page_number +=1

            x += 1

    except Exception as e:
        print("The Stateslinks Error Reason: ",e)     

    return Busrouteslinks,Routes_link

#this BUSDETAILS will scrape the bus data of each routes in a state
def BUSDETAILS(busrouteslink):
    try:

        BusDetails = []
        Bus_NO = 1
        for link in busrouteslink:

            print( "The link: ", link,"\n")
            driver.get(link)
            driver.maximize_window()
            time.sleep(3)

            wait = WebDriverWait(driver, 10)
            try:

                goverment_buses=wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='button']")))
                buttons=driver.find_elements(By.XPATH,"//div[@class='button']")
                print(len(buttons))
                ind = 1
                if len(buttons)!=0:
                    for _ in buttons:
                        buttons[ind].click()  
                        time.sleep(3)
                        ind -= 1

            except Exception as e:
                pass            

            old_page_source = ''  
            
            while True:
                
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(1)
                new_page_source = driver.page_source
                if new_page_source == old_page_source:
                    break
                old_page_source = new_page_source

            # Bus_details = driver.find_elements(By.XPATH,"//ul[@class='bus-items']/div/li/div/div")[2]
            route_links = driver.find_elements(By.XPATH,"//div[@class='clearfix row-one']")
            # print("The No. of routes_links: ",len(route_links),"\n")
            
            for i in route_links:
                BusNames = i.find_element(By.CSS_SELECTOR,"div.travels.lh-24.f-bold.d-color").text
                BusType = i.find_element(By.CSS_SELECTOR,"div.bus-type.f-12.m-top-16.l-color.evBus").text 
                DepartureTime = i.find_element(By.CSS_SELECTOR,'div.dp-time.f-19.d-color.f-bold').text
                TravellingTime = i.find_element(By.CSS_SELECTOR,'div.dur.l-color.lh-24').text
                ReachingTime =i.find_element(By.CSS_SELECTOR,'div.bp-time.f-19.d-color.disp-Inline').text
                StarRating = i.find_element(By.XPATH,"//div[@class='rating-sec lh-24']/div/span").text
                Ticket_Price = i.find_element(By.CSS_SELECTOR,'span.f-19.f-bold').text
                SeatAvailability = i.find_element(By.CSS_SELECTOR,'div.seat-left').text.split()[0]

                BusDetails.append((Bus_NO,BusNames,BusType,DepartureTime,TravellingTime,ReachingTime,StarRating,Ticket_Price,SeatAvailability ))

            Bus_NO += 1    

    except Exception as e:
        print("The Error reason: ",e)

    return BusDetails

# This closingdriver will close the driver
def closingdriver():
    try:
        driver.quit()

    except Exception as e:
        print("The closingdriver Error reason: ",e)    

"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

# Initialize the Chrome driver
driver = webdriver.Chrome() 
HomePage_driver(driver)

"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

# Extracting the PagesLink of the each States and also State Names
secondpage_link = driver.find_elements(By.XPATH,"//a[@class='OfferSection__ViewAllText-sc-16xojcc-1 eVcjqm']")[1].get_attribute('href')
States_Page_Links,StatesNames = StatesPage_Link(secondpage_link)
df = pd.DataFrame(data=States_Page_Links,columns=['States link'])
time.sleep(2)

"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

# Extracting the BusRoutesLinks from all the States
busrouteslink,routelink = BusRoutes_link(States_Page_Links,StatesNames)
df2 = pd.DataFrame(data=busrouteslink,columns=['Route_NO','States Transportation Name','Bus Routes','Bus Routes Link']) 
df2.to_csv('route_data6.csv',index=False,mode='w')
print(busrouteslink,routelink)
print(df2.to_string(),"\n")

"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

# Extracting the Bus details from all the bus routes 
busdetails = BUSDETAILS(routelink)
df3 = pd.DataFrame(data=busdetails,columns=['Bus_NO','Bus Name','Bus Type','Departure Time','Travelling Time','Reaching Time','Bus Rating','Ticket Price','Seat Availability'])   
df3.to_csv('bus_data6.csv', index=False,mode='w')
print(df3.to_string(),"\n")

"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

# Closing the Driver 
closingdriver()