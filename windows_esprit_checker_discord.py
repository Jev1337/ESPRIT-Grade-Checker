from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import asyncio
import discord
import datetime


secret = "" # Your discord bot token
room_id = "" # The room id where you want to send the message

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=discord.Intents.all())

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options = options)


print ("Enter your username:")
username = input()
print ("Enter your password:")
password = input()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await main()

async def main():
    first_suc = True
    default = -1
    await client.wait_until_ready()
    channel = client.get_channel(int(room_id))
    while True:
        try:
            if "default.aspx" not in driver.current_url and "Resultat2021.aspx" not in driver.current_url:
                driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")
                print("[=] Redirected to login page...")

            # Check if redirected to login page
            if "default.aspx" in driver.current_url:
                print("[+] Logging in...")
                # Enter login credentials
                driver.find_element(By.ID, "ContentPlaceHolder1_TextBox3").send_keys(username)
                driver.find_element(By.ID, "ContentPlaceHolder1_Button3").click()
                await asyncio.sleep(3)
                driver.find_element(By.ID, "ContentPlaceHolder1_TextBox7").send_keys(password)
                driver.find_element(By.ID, "ContentPlaceHolder1_ButtonEtudiant").click()
                if "default.aspx" in driver.current_url:
                    print("[!] Wrong credentials / Error logging in...")
                    pass

            # Go back to the result page
            driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")

            if first_suc == False:
                await asyncio.sleep(60)
                
            if "default.aspx" not in driver.current_url:
                
                print("\033c")
                # Find the table and count the rows
                table = driver.find_element(By.XPATH,"//table")
                rows = table.find_elements(By.XPATH,".//tr")
                
                if first_suc == True:
                    await channel.send('This is an initialization embed:')
                    embed = discord.Embed(title="Returned Modules for " + username, description="", color=0x00ff00)
                    for i in range(1,len(rows)):
                        cells = rows[i].find_elements(By.XPATH, ".//td")
                        embed.add_field(name="Module " + str(i), value=cells[0].text, inline=False)
                    await channel.send(embed=embed)
                first_suc = False
                print("[!] Returned Marks:", len(rows)-1)
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(rows)-1) + " marks | Last: " + datetime.datetime.now().strftime("%H:%M:%S") ))
                if default == -1:
                    default = len(rows)-1
                elif default != len(rows)-1:
                    print("[+] Marks updated!")
                    await channel.send('@everyone A new mark has been added!')
                    embed = discord.Embed(title="Returned Modules for " + username, description="", color=0x00ff00)
                    for i in range(1,len(rows)):
                        cells = rows[i].find_elements(By.XPATH, ".//td")
                        embed.add_field(name="Module " + str(i), value=cells[0].text, inline=False)
                    await channel.send(embed=embed)
                    default = len(rows)-1
                print("Last update:", datetime.datetime.now().strftime("%H:%M:%S"))
        except Exception as e:
            if str(e) == "KeyboardInterrupt":
                print("[-] Exiting...")
                break
            else:
                print("Error:", e)
                pass
    driver.quit()
    client.close()
    quit()


client.run(secret)