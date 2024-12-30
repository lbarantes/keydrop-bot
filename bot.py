from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from win10toast import ToastNotifier
import threading

stopEvent = threading.Event()
driver = None
toaster = ToastNotifier()

def showNotification(title, message, duration = 5):
    try:
        threading.Thread(target=lambda: toaster.show_toast(
            title,
            message,
            duration=duration,
            threaded=True
        )).start()
    except:
        print(f"{title}: {message}")

def execute(tipoSorteio, valorMinimo):
    global driver
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")

    userDataDir = os.path.join(os.getenv('LOCALAPPDATA'), "Google", "Chrome", "User Data")
    options.add_argument(f"user-data-dir={userDataDir}")

    driver = webdriver.Chrome(options=options)
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    while not stopEvent.is_set():
        driver.get('https://key-drop.com/pt/giveaways/list')

        container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="div-active-giveaways-list-section"]'))
        )

        WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="div-active-giveaways-list-single-card"]'))
        )

        giveawayItems = container.find_elements(By.CSS_SELECTOR, '[data-testid="div-active-giveaways-list-single-card"]')

        lastItem = giveawayItems[-1]

        if tipoSorteio in lastItem.text:
            preco = lastItem.find_element(By.XPATH, ".//*[contains(text(), 'R$')]")
            textoPreco = preco.text.replace('R$', '').replace(',', '.').strip()
            valor = float(textoPreco)
            if valor >= valorMinimo:
                print(f"Um sorteio de valor superior a R${valorMinimo} foi encontrado")
                link = lastItem.find_element(By.CSS_SELECTOR, 'a.button')
                driver.execute_script("arguments[0].click();", link)
                try:
                    participar = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="btn-giveaway-join-the-giveaway"]'))
                    )
                    try:
                        textoParticipar = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="btn-giveaway-join-the-giveaway"] span'))
                        ).text
                    except:
                        textoParticipar = None
                except:
                    participar = None

                if participar:
                    if not participar.get_attribute("disabled"):
                        participar.click()
                    if participar.get_attribute("disabled"):
                        time.sleep(5)
                        try:
                            textoParticipar = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="btn-giveaway-join-the-giveaway"] span'))
                            ).text
                        except:
                            textoParticipar = None
                        if textoParticipar:
                            if textoParticipar == "JÁ ADERIU A ESTE SORTEIO":
                                showNotification("KeyDrop Bot", "Você entrou em um sorteio")
                                time.sleep(30)
                            elif textoParticipar == "PARTICIPE NO SORTEIO":
                                showNotification("KeyDrop Bot", "Confirme sua entrada realizando o teste \"Você não é um robô\". Você tem 60 segundos para realizar esta ação")
                                time.sleep(60)
                            elif textoParticipar.count(":") >= 2:
                                showNotification("KeyDrop Bot", "Você deve aguardar suas participações resetarem")
                                stop_bot()
                                break
                            else:
                                print("erro")
                                time.sleep(30)
                        else:
                            print("Não foi encontrado o texto do botão de participar")
                            time.sleep(5)
                else:
                    print("Botão para participar não encontrado")
                    time.sleep(5)
            else:
                showNotification("KeyDrop Bot", f"Nenhum sorteio de valor superior à R${valorMinimo} encontrado")
                time.sleep(30)
        else:
            showNotification("KeyDrop Bot", f"Um card do sorteio \"{tipoSorteio}\" não foi encontrado.")
            time.sleep(5)

    stop_bot()

def stop_bot():
    global driver
    stopEvent.set()
    if driver:
        driver.quit()
        driver = None