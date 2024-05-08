from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote
from openpyxl import Workbook
import time

country, location, txt = "USA", "California", "it services"

page = 1

all_businesses_data = []

encoded_location = quote(location)

encoded_txt = quote(txt)

required_data_list = ["Business Started:", "Hours of Operation", "Contact Information", "Business Categories"]

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

                business_data_dict = {"Title": '',"Overview": '', "Product & Services": '',"Business Started": '',  "Hours of Operation" : '', "Contact Information" : '', "Business Categories" : '', 'Website': '', "Phone Number":''}

                business_data_dict["Title"] = link.text

                driver.switch_to.window(driver.window_handles[1]) #switch to second tab
                
                # Overview and Product & Services

                driver.get(link_attrb)

                time.sleep(10)

                try:
                    overview = driver.find_element(By.XPATH, "//div[contains(@class,'dtm-overview')]//div").text
                    business_data_dict["Overview"] = overview
                except:
                    print("Error @ Overview")

                try:
                    products_services = driver.find_element(By.XPATH, "//div[contains(@class,'dtm-products-services')]").text
                    business_data_dict["Product & Services"] = products_services
                except:
                    print("Error @ Products & Services")


                driver.get(link_attrb + "/details")

                time.sleep(10)

                # Business Started, Hours of Operation, All contact person, Business categories

                div =  driver.find_element(By.XPATH, "//div[@class='stack css-n8vred e1ri33r70']")

                data_heading = div.find_elements(By. TAG_NAME, "dt" )

                data_value = div.find_elements(By. TAG_NAME, "dd")

                for index in range(len(data_heading)):

                    try:
                        label = data_heading[index].text
                        if label in required_data_list:
                            if label.endswith(":"):
                                label = label[:-1]

                            value = data_value[index].text
                            
                            business_data_dict[label] = value
                    except:

                        print("Error in heading loop")

                # Contact Info
                ## Phone Number, Website

                try:
                    contact_div = driver.find_element(By.XPATH, "//div[contains(@class,'dtm-contact')]")

                    try:
                        website = contact_div.find_element(By.TAG_NAME, "a")
                        business_data_dict["Website"] = website.get_attribute('href')
                    except:
                        print("Error @ website")

                    try:
                        phone_number = contact_div.find_element(By.XPATH, "//a[contains(@class,'dtm-phone')]")
                        business_data_dict["Phone Number"] = phone_number.text
                    except:
                        print("Error @ Phone Number")

                except:

                    print("Error @ contact info")

                all_businesses_data.append(business_data_dict)

                time.sleep(10)
      
            except:
                print("Skipping:", link_attrb)

# Store data in excel

wb = Workbook()

ws = wb.active

if len(all_businesses_data) > 0:

    headers_list = all_businesses_data[0].keys()

    ws.append(list(headers_list))

    for business in all_businesses_data:

        ws.append(list(business.values()))


wb.save('Output.xlsx')