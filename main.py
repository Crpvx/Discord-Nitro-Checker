import requests
from requests.exceptions import ProxyError
from colorama import Fore, init
import os
import time
import random 
import concurrent.futures
from datetime import datetime
import pytz

# Initialize colorama for colored output
init()

# Initial counts
valid_count = 0
claimed_count = 0
invalid_count = 0
unknown_count = 0

# Function to update the window title
def addcount(counter):
    global valid_count, claimed_count, invalid_count, unknown_count
    
    if counter == "valid":
        valid_count += 1
    elif counter == "claimed":
        claimed_count += 1
    elif counter == "invalid":
        invalid_count += 1
    elif counter == "unknown":
        unknown_count += 1
    update_window_title()

def update_window_title(timer=None):
    title = f"Nitro Checker | Valid: {valid_count} | Claimed: {claimed_count} | Invalid: {invalid_count} | Unknown: {unknown_count}"

    if timer is not None:
        title += f" | Countdown: {timer} Seconds"

    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)  # For Windows
    except:
        print(title)  # For Unix

proxy_activity = False

class Utils:
    @staticmethod
    def GetFormattedProxy(filename):
        proxy = random.choice(open(filename, encoding="cp437").read().splitlines()).strip()
        if '@' in proxy:
            return proxy
        elif len(proxy.split(':')) == 2:
            return proxy
        else:
            if '.' in proxy.split(':')[0]:
                return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
            else:
                return ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])
    @staticmethod
    def file_has_content(filename):
     if not os.path.exists(filename):
        return False  # The file doesn't exist
     if os.path.getsize(filename) > 0:
        return True  # The file has content
     return False  # The file exists but is empty
    

def time_difference_in_words(date_string):
    try:
        # Parse the input date string
        date = datetime.fromisoformat(date_string)
        now = datetime.now(pytz.utc)

        # Make both datetimes aware of the UTC timezone
        date = date.replace(tzinfo=pytz.utc)

        # Calculate the time difference
        time_difference = date - now

        # Extract hours, minutes, and seconds
        seconds = time_difference.total_seconds()
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)

        # Generate the human-readable output
        if hours > 0:
            return f"In {hours} Hours"
        elif minutes > 0:
            return f"In {minutes} Minutes"
        elif seconds > 0:
            return f"In {seconds} Seconds"
        else:
            return "Now"

    except ValueError:
        return "Idk Bro"
# Function to check if a file exists and has content
def file_has_content(filename):
    return os.path.exists(filename) and os.path.getsize(filename) > 0

# Function to clear a file
def clear_file(filename):
    with open(filename, "w") as file:
        file.truncate(0)
start_time = None
def start():
    print(Fore.WHITE + " ")
    print(Fore.GREEN + "Starting...")
    time.sleep(3)
    update_window_title()
    global start_time
    start_time = datetime.now()
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(Fore.MAGENTA + """
          

███╗   ██╗██╗████████╗██████╗  ██████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
████╗  ██║██║╚══██╔══╝██╔══██╗██╔═══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██╔██╗ ██║██║   ██║   ██████╔╝██║   ██║    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██║╚██╗██║██║   ██║   ██╔══██╗██║   ██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║ ╚████║██║   ██║   ██║  ██║╚██████╔╝    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝      ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

                                                                                                     
""")
    
# Check If The User Is Connected To The Internet
url = "https://google.com"
try:
    response = requests.get(url)  # Get the response from the URL
    time.sleep(0.4)
except requests.exceptions.ConnectionError:
    # Tell the user
    input("You are not connected to the internet, check your connection and try again.\nPress enter to exit")
    exit()  # Exit the program
if not Utils.file_has_content("input/GiftCodes.txt"):
   input("The input/GiftCodes.txt File Doesn't Exist Or Is Empty.\nPress Enter To Exit...")
   exit()

output_files = ["output/ValidCodes.txt", "output/UsedGifts.txt", "output/InvalidCodes.txt", "output/UnknownCodes.txt"]
if any(file_has_content(filename) for filename in output_files):
 clear_all_files_response = input("Files In Output Have Some Content Wanna Clear Them? (y/n): ")
 if clear_all_files_response.lower() == "y":
  for filename in output_files:
    if file_has_content(filename):
        clear_file(filename)
        print(Fore.GREEN + f"{filename} has been cleared.")
gift_codes = []

print(Fore.WHITE + " ")
reply = input('Do You Wanna Delete Dupliacted Gift Links? (y/n): ')
with open("input/GiftCodes.txt", "r") as file:
     gift_codes = file.read().splitlines()
if reply.lower() == "y":
     gift_codes = list(set(gift_codes))  # Remove duplicates

     if not gift_codes:
        raise ValueError("Error: GiftCodes.txt is empty after removing duplicates.")

     # Write unique gift codes back to the file
     with open("input/GiftCodes.txt", "w") as file:
        file.write('\n'.join(gift_codes))
        print(Fore.GREEN + "Successfully Deleted All Duplicated Gift Link!")

hidden_valids = False

print(Fore.WHITE + " ")
respond_to_validcodes = input("Do You Want The Codes Of Valid Gift Links To Be Hidden? (y/n): ")
if respond_to_validcodes.lower() == "y":
   hidden_valids = True
   print(Fore.GREEN + "Valid Codes Will Be Hidden!!")
   

def check_random_proxy():
   try:
      print(Fore.WHITE + " ")
      print(Fore.YELLOW + "Testing A Random Proxy From Your Provided Proxies...")
      proxy = Utils.GetFormattedProxy('./input/proxies.txt')
      proxies = {'http': f'http://{proxy}' , 'https': f'http://{proxy}'}
      response = requests.get('https://www.google.com', proxies=proxies)
      if response.status_code == 200:
       print(Fore.GREEN + f'{proxy} | is a valid proxy')
       global proxy_activity
       proxy_activity = True
       start()
   except ProxyError as e:
      print(Fore.RED + f'{proxy} | is not a valid proxy')
      print(Fore.WHITE + " ")
      reply = input("Do You Want To Continue? (y/n): ")
      if reply.lower() == "y":
         start()
      else:
       print(Fore.RED + "Closing...")
       time.sleep(2)
       exit()

if not Utils.file_has_content("input/proxies.txt"):
   print(Fore.WHITE + " ")
   noproxy_reponse = input("The input/proxies.txt File Doesn't Exist Or Is Empty. NOT USING PROXIES WILL DEFINETLY GET YOU RATE LIMITED!!\nDo You Wanna Continue Without Using Proxies? (y/n): ")
   if noproxy_reponse.lower() == "y":
      start()
   else:
      print(Fore.RED + "Closing...")
      time.sleep(2)
      exit()
else:
   check_random_proxy()

def check_discord_gift_code(code):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    if proxy_activity == True:
     proxy = Utils.GetFormattedProxy("./input/proxies.txt")
     proxies =  {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
     response = requests.get(url, proxies=proxies)
    else :
     response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        uses = data.get("uses", 0)
        expiration = f'{data["expires_at"]}'
        time_left = time_difference_in_words(expiration)
        plan = data["subscription_plan"]["name"]
        if uses == 0:
            if hidden_valids == True:
               print(Fore.GREEN + f"Valid | https://discord.gift/hiddenlink" + Fore.WHITE + f' | Expires {time_left}' + Fore.WHITE + " | " + Fore.BLUE + plan)
            else:
               print(Fore.GREEN + f"Valid | https://discord.gift/{code}" + Fore.WHITE + f' | Expires {time_left}' + Fore.WHITE + " | " + Fore.BLUE + plan)
            with open("output/ValidCodes.txt", "a") as valid_file:
                valid_file.write(f"https://discord.gift/{code}\n")
                addcount("valid")
        else:
            print(Fore.YELLOW + f"Claimed | https://discord.gift/{code}")
            with open("output/UsedGifts.txt", "a") as used_file:
                used_file.write(f"https://discord.gift/{code}\n")
                addcount('claimed')
    elif response.status_code == 429:
        print(Fore.CYAN + "Rate Limited | Retrying...")
        rate_limit_reset_header = response.headers.get('X-RateLimit-Reset')
        if rate_limit_reset_header is not None:
            rate_limit_reset = int(rate_limit_reset_header)
            time_to_wait = max(1, rate_limit_reset - int(time.time()))
            time.sleep(time_to_wait)  # Wait for the rate limit reset time
        else:
            time.sleep(1)
        check_discord_gift_code(code)  # Retry the request after waiting
    elif response.status_code == 404:
        print(Fore.RED + f"Invalid | https://discord.gift/{code}")
        with open("output/InvalidCodes.txt", "a") as invalid_file:
            invalid_file.write(f"https://discord.gift/{code}\n")
            addcount("invalid")
    else:
        print(Fore.RED + f"Unknown | https://discord.gift/{code}")
        with open("output/UnknownCodes.txt", "a") as unknown_file:
            unknown_file.write(f"https://discord.gift/{code}\n")
            addcount("unknown")

def process_gift_codes(gift_codes):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for code in gift_codes:
            if code.startswith("https://discord.gift/"):
                code = code.replace("https://discord.gift/", "")
                executor.submit(check_discord_gift_code, code)

process_gift_codes(gift_codes)
end_time = datetime.now()
elapsed_time = end_time - start_time
# Format the elapsed time
hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)

# Display the elapsed time
elapsed_time_str = ""

if int(hours) > 0:
    elapsed_time_str += f"{int(hours)} hour{'s' if int(hours) > 1 else ''} "

if int(minutes) > 0:
    elapsed_time_str += f"{int(minutes)} minute{'s' if int(minutes) > 1 else ''} "

elapsed_time_str += f"{int(seconds)} second{'s' if int(seconds) > 1 else ''}"


print(Fore.WHITE + " ")
print(Fore.GREEN+ f'Successfully Checked {valid_count + claimed_count + invalid_count + unknown_count} Gift Links In {elapsed_time_str}')
print(Fore.LIGHTBLACK_EX + f'Valid : {valid_count} | Already Claimed : {claimed_count} | Invalid : {invalid_count} | Unknown : {unknown_count}')

print(Fore.WHITE + " ")
input("Press Enter to exit...")