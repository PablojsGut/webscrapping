#scrapping.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from pyzbar.pyzbar import decode

def votar_cupon(mail, psw, local, estrellas, cod):
    # Configuración de Selenium
    driver = webdriver.Chrome()  # Asegúrate que chromedriver está en PATH
    wait = WebDriverWait(driver, 20)
    
    try:
        # Abrir página
        driver.get("https://savemoney.cl/descuentos/the1one")
        
        # Opciones de usuario
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='MuiBox-root css-g2z5de'])[2]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='MuiBox-root css-84p2vz'])[1]"))).click()
        
        # Registro
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineAlways MuiLink-button css-4165u6'])[2]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@class='MuiInputBase-input MuiOutlinedInput-input MuiInputBase-inputAdornedStart css-1ixds2g'])[1]"))).send_keys(mail)
        driver.find_element(By.XPATH, "(//input[@class='MuiInputBase-input MuiOutlinedInput-input MuiInputBase-inputAdornedStart MuiInputBase-inputAdornedEnd css-1gnht4k'])[1]").send_keys(psw)
        driver.find_element(By.XPATH, "(//input[@class='MuiInputBase-input MuiOutlinedInput-input MuiInputBase-inputAdornedStart MuiInputBase-inputAdornedEnd css-1gnht4k'])[2]").send_keys(psw)
        
        driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
        
        # Seleccionar tarjeta
        wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[@class='MuiBox-root css-1f3xc36'])[{local}]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='MuiButtonBase-root MuiButton-root MuiLoadingButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-root MuiLoadingButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary css-s9b231'])[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-fullWidth css-10wsyib'])[1]"))).click()
        
        wait = WebDriverWait(driver, 20) # Esperar a que aparezca el SVG completo 
        svg = wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Código QR del cupón']")) ) 
        # Captura del QR directamente como PNG 
        svg.screenshot("qr.png") 
        # Leer el QR 
        img = Image.open('qr.png')
        qr_data = decode(img)
        
        if qr_data:
            url = qr_data[0].data.decode('utf-8')
            print("QR detectado:", url)
            driver.execute_script(f"window.open('{url}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            
            # Validar código
            wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@class='MuiInputBase-input MuiOutlinedInput-input css-1x5jdmq'])[1]"))).send_keys(cod)
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-fullWidth css-177ko57'])[1]"))).click()
            
            time.sleep(5)  # Espera cookies
            driver.close()  # Cierra la pestaña del QR
            driver.switch_to.window(driver.window_handles[0])  # Volver a la primera
            
            # Votar
            time.sleep(5)
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary css-1ouvl1c'])[1]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, f"(//button[@class='MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeMedium css-14za61z'])[ {estrellas} ]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary css-gvt6cw'])[1]"))).click()
            
            print("Voto realizado correctamente.")
        else:
            print("No se detectó QR")

    finally:
        time.sleep(5)
        driver.quit()