# Version 1.0 only for linux systems
# Made by DisruptorCode

import subprocess
import sys
import re
import os
import time

from colorama import Fore, Style

def get_options():
    print('Specify self MAC address --> [1]')
    print('Get random MAC address --> [2]')

    menu = int(input('> '))

    if menu == 1:
        interface = input('Interface -> ')
        new_mac = input('Specify new MAC address --> ')
        return interface, new_mac
    elif menu == 2:
        os.system('python3 mac_random.py')
        exit()

def change_mac(interface, new_mac, current_mac):
    print(f'[+] Changing MAC address for {interface} from {current_mac} to {new_mac}')

    subprocess.call(['ip', 'link', 'set', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
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
        print(Fore.RED + '[!] Specify another MAC address.')
        print(Style.RESET_ALL + '----------------------------------')
        time.sleep(1.5)
        main()
    elif current_mac != mac_search_res.group(0):
        print(Fore.GREEN + '[+] Your MAC address has been changed.' + Style.RESET_ALL)

def main():
    interface, new_mac = get_options()
    current_mac = get_current_mac(interface)

    change_mac(interface, new_mac, current_mac)

    check_mac(interface, current_mac)

    return interface, new_mac, current_mac

interface, new_mac, current_mac = main()

