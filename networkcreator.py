from colorama import init, Fore, Back, Style
import re
from time import sleep

# Initialize colorama
init()

# Set Color Schemes
whiteonred = (Fore.WHITE + Back.RED)
blue = (Fore.BLUE)
white = (Fore.WHITE)
reset = (Style.RESET_ALL)
green = (Fore.GREEN)
yellow = (Fore.YELLOW)

# Welcome Message
print("\n"*5)
print(blue + "#####################################################################")
print(blue + "#" + white + "Welcome to the:".center(66,' ') + blue + " #")
print(blue + "#" + white + "Network Creator Tool".center(66,' ') + blue + " #")
print(blue + "#" + white + "Vers: 1.0".center(66," ") + blue + " #")
print(blue + "#####################################################################" + reset + "\n")

print(Fore.LIGHTCYAN_EX + "\nUsage:" + yellow + "\t\tThis is meant for use with Class C IP Addresses" + reset)
print(yellow + "\t\tcommonly found in home networks\n" + reset)

print(Fore.LIGHTCYAN_EX +"Disclaimer:" + yellow + "\tYou cannot choose more that 64 networks when subnetting\n" + reset)

print(yellow + "\t\tBefore running this script, you" + reset)
print(yellow + "\t\tneed your IP and Subnet Mask.\n" + reset)

print(yellow + "\t\tFor Windows: Run ipconfig" + reset)
print(yellow + "\t\tFor LINUX:   Run ifconfig\n" + reset)

print(yellow + "\t\tIP address will start with:  192.168..." + reset)
print(yellow + "\t\tSubnet Mask will start with: 255.255...\n" + reset)



def get_orig_network_details():
    Orig_IP = input("[?] What is your IP Address?  : ")
    Orig_SM = input("[?] What is your Subnet Mask? : ")
    
    return (Orig_IP,Orig_SM)

def check_orig_network_details(Orig_IP, Orig_SM):    
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    ippaterrmsg = "Your IP address must be in the form \"xxx.xxx.xxx.xxx\" where x represents a digit between 0 and 9"
    smpaterrmsg = "Your Subnet Mask must be in the form \"xxx.xxx.xxx.xxx\" where x represents a digit between 0 and 9"
    
    ip_valid = re.match(pattern,Orig_IP) is not None
    sm_valid = re.match(pattern,Orig_SM) is not None
    
    print("[-]")
    print("[-] Validating IP and Subnet Mask...")
    print("[-]")
    sleep(1.3)
    
    
    if not ip_valid:
        print("[" + whiteonred + "X" + reset + "]", ippaterrmsg)
    if not sm_valid:
        print("[" + whiteonred + "X" + reset + "]", smpaterrmsg)
        
    return ip_valid and sm_valid

def choose_options():
    print("[1] Show binary/CIDR format of network")
    print("[2] Show subnetting network into multiple networks")
    print("[3] Quit\n")
    selection = input("[-] Select?: ")
    
    return(selection)

def check_choice(selection):    
    pattern = r'^(1|2|3)$'
    selection_valid = re.match(pattern,selection)
    
    if not selection_valid:
        print("[-]")
        print("[" + whiteonred + "X" + reset + "] You must choose 1,2 or 3 only")
        
    return selection_valid
    
def show_bin_network(Orig_IP,Orig_SM):
    ip_octets = Orig_IP.split('.')
    sm_octets = Orig_SM.split('.')
    
    ip_binary_octets = []
    sm_binary_octets = []
    count = 0
    
    for ip_octet in ip_octets:
        ip_binary_octet = int(bin(int(ip_octet))[2:])
        ip_binary_octet = f'{ip_binary_octet:08d}'
        ip_binary_octets.append(ip_binary_octet)
    binary_ip_address = '.'.join(ip_binary_octets)
    
    for sm_octet in sm_octets:
        sm_binary_octet = int(bin(int(sm_octet))[2:])
        sm_binary_octet = f'{sm_binary_octet:08d}'
        count += sm_binary_octet.count("1")
        sm_binary_octets.append(sm_binary_octet)
    binary_sm_address = '.'.join(sm_binary_octets)
    
    print("[" + green + "+" + reset + f"]   IP Address:  {Orig_IP}")
    print(blue + "\t\t" + yellow + "In Binary" + blue + " >>>\t" + green + binary_ip_address + reset)
    print(blue + "\t\t" + yellow + "In CIDR" + blue + "   >>>\t" + green + Orig_IP + "/" + str(count) + reset)
    print("[" + green + "+" + reset + f"]   Subnet Mask: {Orig_SM}")
    print(blue + "\t\t" + yellow + "In Binary" + blue + " >>>\t" + green + binary_sm_address + reset)

def get_num_nets():
    num_networks_needed = int(input("[?] How many networks do you need?: "))
    
    return num_networks_needed

def check_num_nets(num):
    num_networks_needed_valid = num <= 64
    
    if not num_networks_needed_valid:
        print("[-]")
        print("[" + whiteonred + "X" + reset + "] You cannot choose more than 64 networks")
    
    return num_networks_needed_valid
    
def subnetting_network(Orig_IP,Orig_SM,num):
    
    print("[-]")
    print("[" + green + "+" + reset + "]" + " Creating new networks...")
    sleep(1.3)
    print("[-]")
    print("[" + green + "+" + reset + "]" + f" Original IP Address: {Orig_IP}")
    print("[" + green + "+" + reset + "]" + f" Original Subnet Mask: {Orig_SM}")
    print("[-]")
    print("[" + green + "+" + reset + "]" + yellow + " New IP Addresses: " + reset)
    print("[-]")
    
    sm_octets = Orig_SM.split('.')
    sm_binary_octets = []
    converted_sm = []
    
    for sm_octet in sm_octets:
        sm_binary_octet = int(bin(int(sm_octet))[2:])
        sm_binary_octet = f'{sm_binary_octet:08d}'
        sm_binary_octets.append(sm_binary_octet)
        
    chart_dict = {264:8,128:7,64:6,32:5,16:4,8:3,4:2,2:1}
    x = num

    hops = None

    for key in sorted(chart_dict.keys()):
        if key >= x:
            hops = chart_dict[key]
            break

    if hops is not None:
        char_list = list(sm_binary_octets[3])
        for i in range(hops):
            char_list[i] = '1'
            sm_binary_octets[3] = ''.join(char_list)
    
    for octet in sm_binary_octets:
        dec_num = int(octet,2)
        converted_sm.append(str(dec_num))
        New_SM = '.'.join(converted_sm)
        
    ip_address = Orig_IP
    segment_size = num 
    x = 0
    z = 0
    output = []
    output1 = []
    output2 = []
    output3 = []

    # Split the IP address into its octets
    octets = ip_address.split(".")
    octets.pop(3)

    # Calculate the number of segments based on the segment size
    increment = 256 // segment_size

    for i in range(0, 256, increment):
        x += 1
        start_value = i
        end_value = i + increment - 1
        last_octet = f"{start_value}-{end_value}"
        octets.append(last_octet)
        adjusted_ip = '.'.join(octets)
        output.append(adjusted_ip)
        output1.append("[" + green + "+" + reset + "]\t" + yellow + "Network" + " " + str(x) + " " + "will have the following attributes:" + reset)
        output2.append("[" + green + "+" + reset + "]\t" + blue + ">>>\t" + yellow + "IP Address Range: " + reset + output[z])
        output3.append("[" + green + "+" + reset + "]\t" + blue + ">>>\t" + yellow + "Subnet Mask:\t  " + reset + New_SM)
        print(output1[z])
        print(output2[z])
        print(output3[z])
        z += 1
        octets.pop(3)
    
def Main():
    while True:
        while True:
            (Orig_IP, Orig_SM) = get_orig_network_details()
            if check_orig_network_details(Orig_IP, Orig_SM):
                print("[" + green + "+" + reset + "] IP Address and Subnet Mask are valid")
                print("[-]")
                print("[" + yellow + "!" + reset + "] Choose one of the following:\n")
                break
            else:
                print("[-]")
                print("[" + yellow + "!" + reset + "] IP and Subnet Mask must be valid, re-enter them")
                print("[-]")

        while True:
            choice = choose_options()
            if check_choice(choice):
                print("[-]")
                sleep(1.3)
                break
            else:
                print("[-]")
                print("[" + yellow + "!" + reset + "] Select again:")
                print("[-]")

        if int(choice) == 1:
            show_bin_network(Orig_IP, Orig_SM)

        elif int(choice) == 2:
            while True:
                num = get_num_nets()
                if check_num_nets(num):
                    subnetting_network(Orig_IP, Orig_SM, num)
                    break
                else:
                    print("[-]")
                    print("[" + yellow + "!" + reset + "] try again")
                    print("[-]")

        else:
            print("[-] Ending....")
            sleep(1.3)

        quit_choice = input("Do you want to quit? (Y/N): ")
        if quit_choice.lower() == "y":
            break

Main()   


