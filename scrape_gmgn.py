from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--headless")  # Run in background
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def get_roi_winrate(wallet_address):
    
    """
    Given a wallet address, open tab, get ROI and Winrate from gmgn.ai, then close tab.
    """
    try:
        url = f"https://gmgn.ai/sol/address/{wallet_address}"
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        wait = WebDriverWait(driver, 5)

        # WINRATE
        winrate_value = 0
        try:
            # winrate_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-1vihibg")))
            winrate_element = driver.find_element(By.XPATH, "//*[text()='Win Rate']/following-sibling::div[1]")
            winrate_text = winrate_element.text.strip()
            winrate_value = winrate_text.replace("%", "")
            print('Winrate =>', winrate_value)
        except Exception:
            print("Winrate not found")
        
        time.sleep(1)

        # ROI
        roi_value = 0
        roi_element = driver.find_element(By.XPATH, "//*[text()='7D Realized PnL']/following-sibling::div[1]")
        if roi_element:
            roi_text = roi_element.text.strip() 
            roi_value = roi_text.split('%')[0] + '%'
            roi_value = roi_value.replace("+", "").replace("%", "")  # Remove + and % signs
            print('ROI =>', roi_value) 
        else:
            print("ROI not found")
        
        return {
            "roi": roi_value,
            "winrate": winrate_value
        }

    except Exception as e:
        print(f"Error scraping {wallet_address}: {str(e)}")
        return None

    finally:
        if driver:
            driver.quit()