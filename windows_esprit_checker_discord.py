from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import asyncio
import discord
import datetime


secret = "" # Your discord bot token
room_id = "" # The room id where you want to send the message
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)


print ("Enter your username:")
username = input()
print ("Enter your password:")
password = input()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await main()

async def main():
    default = -1
    channel = client.get_channel(room_id)
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
                await asyncio.sleep(3)
                driver.find_element(By.ID, "ContentPlaceHolder1_TextBox7").send_keys(password)
                driver.find_element(By.ID, "ContentPlaceHolder1_ButtonEtudiant").click()
                if "default.aspx" in driver.current_url:
                    print("[!] Wrong credentials / Error logging in...")
                    pass

            # Go back to the result page
            driver.get("https://esprit-tn.com/ESPOnline/Etudiants/Resultat2021.aspx")

            await asyncio.sleep(2)
            # Check if still logged in
            if "default.aspx" not in driver.current_url:
                print("\033c")
                # Find the table and count the rows
                table = driver.find_element(By.XPATH,"//table")
                rows = table.find_elements(By.XPATH,".//tr")
                print("[!] Returned Marks:", len(rows)-1)
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(rows)-1)+" marks"))
                if default == -1:
                    default = len(rows)-1
                elif default != len(rows)-1:
                    print("[+] Marks updated!")
                    await client.wait_until_ready()
                    await channel.send('@everyone A new mark has been added! ')
                    default = len(rows)-1
                print("Last update:", datetime.datetime.now().strftime("%H:%M:%S"))
        except Exception as e:
            print("Error:", e)
            break
    driver.quit()
    client.close()
    quit()


client.run(secret)

