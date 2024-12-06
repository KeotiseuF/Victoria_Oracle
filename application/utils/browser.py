from selenium import webdriver

def manage_browser(url: str, browser: webdriver.Chrome | None, quit = True):
  if(quit is False):
    browser = webdriver.Chrome()
    browser.get(url)
    return(browser)
  else:
    browser.quit()
