from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import asyncio
import discord
import datetime
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1600, 1200))
display.start()


secret = "" # Your discord bot token
room_id = "" # The room id where you want to send the message

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=discord.Intents.all())

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=3')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
browser_driver = webdriver.ChromeService('/usr/lib/chromium-browser/chromedriver')
driver = webdriver.Chrome(options = options, service = browser_driver)

has_run_main = False

print ("Enter your username:")
username = input()
print ("Enter your password:")
password = input()

@client.event
async def on_ready():
    print('[+] Logged in as {0.user}'.format(client))
    await main()

@client.event
async def on_resumed():
    print('[+] Resumed connection to Discord')
    await main()

async def main():
    global has_run_main
    if has_run_main:
        return
    has_run_main = True
    first_suc = True
    default = -1
    await client.wait_until_ready()
    channel = client.get_channel(int(room_id))
    while True:
        try:
            if "default.aspx" not in driver.current_url and "Resultat2021.aspx" not in driver.current_url:
                driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")
                print("[=] Redirected to login page...")

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

            driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")

            if first_suc == False:
                await asyncio.sleep(60)
            
            if "default.aspx" not in driver.current_url:
                print("\033c")
                table = driver.find_element(By.XPATH,"//table")
                rows = table.find_elements(By.XPATH,".//tr")
                message = ""
                if first_suc == True:
                    embed = discord.Embed(title="Returned Modules for " + username, description="Initialization Embed (No Changes)", color=0x237feb, url="https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx", timestamp=datetime.datetime.now())
                    embed.set_author(name="ESPRIT-Grade-Checker", icon_url="https://avatars.githubusercontent.com/u/19759761?v=4")
                    embed.set_footer(text="By Jev1337")
                    embed.set_thumbnail(url="https://i.imgur.com/lKDeVmh.png")
                    for i in range(1,len(rows)):
                        cells = rows[i].find_elements(By.XPATH, ".//td")
                        embed.add_field(name="Module " + str(i), value=cells[0].text, inline=True)
                    if len(rows) == 1:
                        embed.add_field(name="Error", value="No modules returned")
                    await channel.send(embed=embed)
                first_suc = False
                print("[!] Returned Marks:", len(rows)-1)
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(rows)-1) + " marks | Last: " + datetime.datetime.now().strftime("%H:%M:%S")))
                if default == -1:
                    default = len(rows)-1
                elif default != len(rows)-1:
                    print("[+] Marks updated!")
                    embed = discord.Embed(title="Returned Modules for " + username, description="@everyone Grades have been updated!", color=0x237feb, url="https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx", timestamp=datetime.datetime.now())
                    embed.set_author(name="ESPRIT-Grade-Checker", icon_url="https://avatars.githubusercontent.com/u/19759761?v=4")
                    embed.set_footer(text="By Jev1337")
                    embed.set_thumbnail(url="https://i.imgur.com/lKDeVmh.png")
                    for i in range(1,len(rows)):
                        cells = rows[i].find_elements(By.XPATH, ".//td")
                        embed.add_field(name="Module " + str(i), value=cells[0].text, inline=True)
                    if len(rows) == 1:
                        embed.add_field(name="Error", value="No modules returned")
                    await channel.send(embed=embed)
                    default = len(rows)-1
                print("Last update:", datetime.datetime.now().strftime("%H:%M:%S"))
        except KeyboardInterrupt:
            has_run_main = False
            print("[-] Exiting...")
            driver.quit()
            client.close()
            exit(0)
        except TimeoutException:
            print("[!] Timeout...")
            await asyncio.sleep(5)
            driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")
            pass
        except Exception as e:
            print("[!] Unknown Error occured\n")
            with open("error.log", "a") as f:
                f.write("[" + datetime.datetime.now().strftime("%H:%M:%S") + "] " + str(e) + "\n")
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Error Occured at " + datetime.datetime.now().strftime("%H:%M:%S")))
            has_run_main = False
            break

client.run(secret, log_handler=None)
