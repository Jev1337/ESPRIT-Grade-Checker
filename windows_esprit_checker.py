from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
    first_suc = True
    default = -1
    while True:
        try:
            if "default.aspx" not in driver.current_url and "Resultat2021.aspx" not in driver.current_url:
                driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")
                print("[=] Redirected to login page...")

            # Check if redirected to login page
            if "default.aspx" in driver.current_url:
                print("[+] Logging in...")
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_TextBox3')))
                driver.find_element(By.ID, "ContentPlaceHolder1_TextBox3").send_keys(username)
                driver.find_element(By.ID, "ContentPlaceHolder1_Button3").click()
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_TextBox7')))
                driver.find_element(By.ID, "ContentPlaceHolder1_TextBox7").send_keys(password)
                driver.find_element(By.ID, "ContentPlaceHolder1_ButtonEtudiant").click()
                if "default.aspx" in driver.current_url:
                    print("[!] Wrong credentials / Error logging in...")
                    pass

            # Go back to the result page
            driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")

            if first_suc == False:
                time.sleep(60)

            if "default.aspx" not in driver.current_url:
                first_suc = False
                print("\033c")
                table = driver.find_element(By.XPATH,"//table")
                rows = table.find_elements(By.XPATH,".//tr")
                print("[!] Returned Marks:", len(rows)-1)
                if default == -1:
                    default = len(rows)-1
                elif default != len(rows)-1:
                    print("[+] Marks updated!")
                    default = len(rows)-1
                print("Last update:", datetime.datetime.now().strftime("%H:%M:%S"))
                for row in rows:
                    print(row.text)
        except KeyboardInterrupt:
            print("[-] Exiting...")
            driver.quit()
            exit(0)
        except TimeoutException:
            print("[!] Timeout...")
            driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")
            pass
        except Exception as e:
            print("[!] Unknown Error occured")
            driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")
            pass
main()
