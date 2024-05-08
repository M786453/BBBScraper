from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
import time

country, location, txt = "USA", "California", "it services"

page = 1

encoded_location = quote(location)

encoded_txt = quote(txt)

required_list = ["Business Started", "Hours of Operation", "Contact Information", "Business categories", 
                 "Contact Info", "Phone Number", "Website", "Overview", "Products & Services"]

url = f"https://www.bbb.org/search?find_country={country}&find_loc={location}&find_text={txt}&page="

driver = webdriver.Chrome()

driver.get(url+"1")

time.sleep(10)

business_links = driver.find_elements(By.XPATH, "//a[@class='text-blue-medium css-1jw2l11 eou9tt70']")

try:
    
    paging = driver.find_element(By.XPATH, "//nav[@aria-label='pagination']")

    anchor = paging.find_elements(By.TAG_NAME, "a")[-3]

    total_Pages = int(anchor.text.strip(" ")[-1])

except Exception as e:
    print("Error:", e)
    total_Pages = 1

driver.execute_script(f'''window.open("","_blank");''')

print("PAGES:", total_Pages)

for pageNumber in range(1, total_Pages+1):

    print("PAGE#", pageNumber)

    driver.switch_to.window(driver.window_handles[0]) #switch to first tab
    
    while True:
        driver.get(url + str(pageNumber))
        if "500 Error" not in driver.page_source:
            break
        time.sleep(10)

    business_links = driver.find_elements(By.XPATH, "//a[@class='text-blue-medium css-1jw2l11 eou9tt70']")
    
    time.sleep(20) #testing

    for link in business_links:

        driver.switch_to.window(driver.window_handles[0]) #switch to first tab
        
        link_attrb = link.get_attribute("href")
        
        if link_attrb.startswith("https://www.bbb.org/"):
        
            try:

                driver.switch_to.window(driver.window_handles[1]) #switch to second tab
                
                driver.get(link_attrb + "/details")
                
                time.sleep(10)

                div =  driver.find_element(By.XPATH, "//div[@class='stack css-n8vred e1ri33r70']")
                
                data_heading = div.find_elements(By. TAG_NAME, "dt" )
                
                data_value = div.find_elements(By. TAG_NAME, "dd")

                for e in range(len(data_heading)):

                    print(data_heading[e].text, data_value[e].text)

                print("Profile:",link_attrb)
                
                time.sleep(10)
      
            except:
                print("Skipping:", link_attrb)