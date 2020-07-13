# Version 1.0 only for linux systems
# Made by DisruptorCode

import random
import subprocess
import re
import time

from colorama import Fore, Style

interface = input('Interface > ')

def set_random_mac():
    symbols = '123456789032456abcdefg'
    symbols_list = []

    for i in symbols:
        symbols_list.append(i)

    random.shuffle(symbols_list)

    MAC_random_list = []

    for el in range(1, 13):
        MAC_random_list.append(random.choice(symbols_list))

    MAC_address_dirty = ''.join(MAC_random_list)
    
    idx = 0
    MAC_address = ''

    for i in MAC_address_dirty:
        MAC_address += i
        idx += 1
        if idx % 2 == 0:
            MAC_address += ':'

    return MAC_address.strip(':')

def change_mac(interface, MAC_address, current_mac):
    print(f'[+] Changing MAC address for {interface} from {current_mac} to {MAC_address}')

    subprocess.call(['ip', 'link', 'set', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', MAC_address])
    subprocess.call(['ip', 'link', 'set', interface, 'up'])
                
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_search_res = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result))

    if mac_search_res:
        return mac_search_res.group(0)
    else:
        print('[-] Could not read a MAC address.')

def check_mac(interface, current_mac):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_search_res = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result))

    if current_mac == mac_search_res.group(0):
        print(Fore.RED + "[-] MAC address doesn't changed!")
        print(Fore.RED + '[!] Trying set another MAC address.')
        print(Style.RESET_ALL + '----------------------------------')
        time.sleep(1.5)
        main_fun()
    elif current_mac != mac_search_res.group(0):
        print(Fore.GREEN + '[+] Your MAC address has been changed!' + Style.RESET_ALL)

def main_fun():
    MAC_address = set_random_mac()

    current_mac = get_current_mac(interface)
    change_mac(interface, MAC_address, current_mac)

    check_mac(interface, current_mac)

    return MAC_address, interface, current_mac

MAC_address, interface, current_mac = main_fun()