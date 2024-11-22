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

# Initialize WebDriver
driver = webdriver.Chrome()

driver.get('http://127.0.0.1:8000/profile')

# Wait for the page to load
time.sleep(2)

# Locate the "Sign Up" link and click on it
sign_up_link = driver.find_element(By.LINK_TEXT, 'Sign Up')
sign_up_link.click()

# Wait for the sign-up page to load
time.sleep(2)

# Loop through the credentials list and sign up each user
for username, password in credentials:
    # Locate the fields for username, password1, and password2
    username_field = driver.find_element(By.NAME, 'username')  
    password1_field = driver.find_element(By.NAME, 'password1')  
    password2_field = driver.find_element(By.NAME, 'password2')  

    # Fill in the fields with the username and password
    username_field.send_keys(username)
    password1_field.send_keys(password)
    password2_field.send_keys(password)

    # Submit the form
    password2_field.send_keys(Keys.RETURN)

    # Locate and click the "Create User" button
    create_user_btn = driver.find_element(By.XPATH, '/html/body/form/button')
    create_user_btn.click()

    # Wait for the form submission to process
    time.sleep(2)

# Print "Login Page" after all users have been created
print('All users have been signed up.')

# Close the browser
driver.quit()
