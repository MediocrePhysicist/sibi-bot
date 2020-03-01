from selenium import webdriver
from datetime import date
import time
import secrets


start = time.time()


# Setup Browser
login_page = 'https://primofs01.sibi.usp.br/pds?func=load-login&calling_system=primo&institute=USP&lang=por&isMobile=false&url=http://www.buscaintegrada.usp.br:80/primo_library/libweb/action/login.do?targetURL=http%3a%2f%2fwww.buscaintegrada.usp.br%2fprimo_library%2flibweb%2faction%2fsearch.do%3fvid%3dUSP%26amp%3bdscnt%3d0%26amp%3bdstmp%3d1583081070253%26amp%3binitializeIndex%3dtrue'

browser = webdriver.Firefox()
browser.implicitly_wait(10)
browser.get(login_page)
browser.find_element_by_link_text('Senha da biblioteca').click()


# Login
login_user = browser.find_element_by_id('bor_id')
login_pass = browser.find_element_by_id('bor_verification')

login_user.send_keys(secrets.NUSP)
login_pass.send_keys(secrets.PASS)

browser.find_element_by_xpath('//*[@value = "OK"]').click()
browser.find_element_by_id('exlidMyAccount').click()


# Book Info
checkboxes = browser.find_elements_by_xpath('//*[@type = "checkbox"]')
titles = browser.find_elements_by_xpath('//*[@class = "MyAccount_Loans_2 MyAccount_Loans_title"]')
dates = browser.find_elements_by_xpath('//*[@class = "MyAccount_Loans_4 MyAccount_Loans_dueDate"]')
locals = browser.find_elements_by_xpath('//*[@class = "MyAccount_Loans_7 MyAccount_Loans_location"]')

checkboxes.pop() # Last element is not associated with a book
td = date.today().strftime("%d/%m/%y")
N = len(dates)
selected = [] # Books that must be renewed

for i in range(N):
    if dates[i].text == td:
        checkboxes[i].click()
        selected.append(i)

browser.find_element_by_link_text('Renovar selecionados').click()
new_dates = browser.find_elements_by_xpath('//*[@class = "MyAccount_Loans_4 MyAccount_Loans_dueDate"]')


# Output
for i in range(N):
    print('\nBook {0}: "{1}"'.format(str(i), titles[i].text))

    if i in selected:
        # Return date didn't change after selection => the book must be returned
        if dates[i].text == new_dates[i].text:
            print('\t... Must be returned to {}.'.format(locals[i].text))
        else:
            print('\t... Successful renewal.')

    else:
        print('\t... OK.')


# Logout
browser.find_element_by_id('exlidSignOut').click()
browser.quit()

time_exec = time.time() - start
print('\n\nDONE! (in {0:.2f} seconds)'.format(time_exec))
