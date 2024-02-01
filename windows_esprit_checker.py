from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import datetime
import time



options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)


print ("Enter your username:")
username = input()
print ("Enter your password:")
password = input()

def main():
    default = -1
    while True:
        try:
            print("[+] Checking login status...")
            if "default.aspx" not in driver.current_url and "Resultat2021.aspx" not in driver.current_url:
                driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")
                print("[=] Redirected to login page...")

            # Check if redirected to login page
            if "default.aspx" in driver.current_url:
                print("[+] Logging in...")
                # Enter login credentials
                driver.find_element(By.ID, "ContentPlaceHolder1_TextBox3").send_keys(username)
                driver.find_element(By.ID, "ContentPlaceHolder1_Button3").click()
                #sleep
                time.sleep(3)
                driver.find_element(By.ID, "ContentPlaceHolder1_TextBox7").send_keys(password)
                driver.find_element(By.ID, "ContentPlaceHolder1_ButtonEtudiant").click()
                if "default.aspx" in driver.current_url:
                    print("[!] Wrong credentials / Error logging in...")
                    pass

            # Go back to the result page
            driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")

            time.sleep(2)
            # Check if still logged in
            if "default.aspx" not in driver.current_url:
                print("\033c")
                # Find the table and count the rows
                table = driver.find_element(By.XPATH,"//table")
                rows = table.find_elements(By.XPATH,".//tr")
                print("[!] Returned Marks:", len(rows)-1)
                if default == -1:
                    default = len(rows)-1
                elif default != len(rows)-1:
                    print("[+] Marks updated!")
                    default = len(rows)-1
                print("Last update:", datetime.datetime.now().strftime("%H:%M:%S"))
        except Exception as e:
            print("Error:", e)
            break
    quit()

main()
