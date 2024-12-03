from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

credentials = [
    ["SkyWalker12", "aKj5b6e1"], ["TechGuru94", "Wn2d7k9z"], ["PixelMaster23", "f4Hc9p3r"], 
    ["CoolBreeze07", "D7nq8a2p"], ["IronFist99", "tG3rX5j1"], ["SilverPhoenix88", "Kp6nF7s8"], 
    ["DreamChaser21", "Z9t2yL1a"], ["BlueKnight05", "b3Vd7sW5"], ["ShadowHunter42", "jD6nT4e9"], 
    ["OceanWaves17", "M1kW7a2d"], ["CyberStorm77", "pX2j8wF4"], ["BlazeRunner59", "fJ4n3g8l"], 
    ["QuantumAce04", "H1dR7b9m"], ["MysticWarrior36", "Q3c7iV9b"], ["SpeedDemon11", "aF9pG4y7"], 
    ["EchoSonic82", "bZ3rL7e8"], ["LunarEclipse25", "R4mT9w3d"], ["DarkKnight33", "Y5vP7k6b"], 
    ["FrozenFire48", "J8nF2hV3"], ["ThunderClap19", "g7Pq9sX1"], ["NightRider56", "iD3fW2v5"],
]

#Change only first element of the list
username = credentials[1][0]
password = credentials[1][1]
#############################################


# Initialize WebDriver
driver = webdriver.Chrome()

driver.get('http://127.0.0.1:8000/profile')


time.sleep(2)


sign_up_link = driver.find_element(By.LINK_TEXT, 'Sign Up')
sign_up_link.click()

time.sleep(2)

username_field = driver.find_element(By.NAME, 'username')  
password1_field = driver.find_element(By.NAME, 'password1')  
password2_field = driver.find_element(By.NAME, 'password2')  

username_field.send_keys(username)

password1_field.send_keys(password)
password2_field.send_keys(password)

create_user_btn = driver.find_element(By.XPATH, '/html/body/form/button')
create_user_btn.click()


time.sleep(2)

username_field = driver.find_element(By.NAME, 'username')
password_field = driver.find_element(By.NAME, 'password')  

username_field.send_keys(username)
password_field.send_keys(password)

login_btn = driver.find_element(By.XPATH, '/html/body/form/button')
login_btn.click()


input("Enter to close the web app...")
driver.quit()