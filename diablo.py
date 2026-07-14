#!/usr/bin/env python3
"""
Diablo - Advanced Proxy Tool by IllusiveHacks
Combines proxy scraping, checking, and management in one powerful tool
"""

import os
import sys
import time
import json
import threading
import webbrowser
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    from colorama import init, Fore, Style, Back
    import pyperclip
except ImportError as e:
    print(f"[!] Missing required module: {e}")
    print("[+] Please run: pip install -r requirements.txt")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

# Constants
VERSION = "1.0.0"
AUTHOR = "IllusiveHacks"
MAX_THREADS = 50
TIMEOUT = 5
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt"
]

# Diablo Banner
DIABLO_BANNER = r"""
{red}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣤⡼⠀⢀⡀⣀⢱⡄⡀⠀⠀⠀⢲⣤⣤⣤⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⡿⠛⠋⠁⣤⣿⣿⣿⣧⣷⠀⠀⠘⠉⠛⢻⣷⣿⣽⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⣞⣽⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠠⣿⣿⡟⢻⣿⣿⣇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣟⢦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣿⡾⣿⣿⣿⣿⣿⠿⣻⣿⣿⡀⠀⠀⠀⢻⣿⣷⡀⠻⣧⣿⠆⠀⠀⠀⠀⣿⣿⣿⡻⣿⣿⣿⣿⣿⠿⣽⣦⡀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⠟⣩⣾⣿⣿⣿⢟⣵⣾⣿⣿⣿⣧⠀⠀⠀⠈⠿⣿⣿⣷⣈⠁⠀⠀⠀⠀⣰⣿⣿⣿⣿⣮⣟⢯⣿⣿⣷⣬⡻⣷⡄⠀⠀⠀
⠀⠀⢀⡜⣡⣾⣿⢿⣿⣿⣿⣿⣿⢟⣵⣿⣿⣿⣷⣄⠀⣰⣿⣿⣿⣿⣿⣷⣄⠀⢀⣼⣿⣿⣿⣷⡹⣿⣿⣿⣿⣿⣿⢿⣿⣮⡳⡄⠀⠀
⠀⢠⢟⣿⡿⠋⣠⣾⢿⣿⣿⠟⢃⣾⢟⣿⢿⣿⣿⣿⣾⡿⠟⠻⣿⣻⣿⣏⠻⣿⣾⣿⣿⣿⣿⡛⣿⡌⠻⣿⣿⡿⣿⣦⡙⢿⣿⡝⣆⠀
⠀⢯⣿⠏⣠⠞⠋⠀⣠⡿⠋⢀⣿⠁⢸⡏⣿⠿⣿⣿⠃⢠⣴⣾⣿⣿⣿⡟⠀⠘⢹⣿⠟⣿⣾⣷⠈⣿⡄⠘⢿⣦⠀⠈⠻⣆⠙⣿⣜⠆
⢀⣿⠃⡴⠃⢀⡠⠞⠋⠀⠀⠼⠋⠀⠸⡇⠻⠀⠈⠃⠀⣧⢋⣼⣿⣿⣿⣷⣆⠀⠈⠁⠀⠟⠁⡟⠀⠈⠻⠀⠀⠉⠳⢦⡀⠈⢣⠈⢿⡄
⣸⠇⢠⣷⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⠿⠋⠀⢻⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢾⣆⠈⣷
⡟⠀⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣶⣤⡀⢸⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⢹
⡇⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠈⣿⣼⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⢸
⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠶⣶⡟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼
⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡁⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣼⣀⣠⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{reset}
{cyan}╔══════════════════════════════════════════════════════════════════╗
║  Diablo v{VERSION} - Advanced Proxy Tool by {AUTHOR}  
║  [+] Multi-threaded Proxy Checker                                  
║  [+] Auto Proxy Scraper (13+ Sources)                             
║  [+] Real-time Results Display  (Password: Illusivehacks)                                  
║  [+] Proxy File Import & Export                                   
╚══════════════════════════════════════════════════════════════════╝
{reset}"""


def clear_screen():
    """Clear terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_animated(text, color=Fore.CYAN, delay=0.001):
    """Print text with animation effect"""
    for char in text:
        sys.stdout.write(f'{color}{Style.BRIGHT}{char}{Style.RESET_ALL}')
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loading_animation(text, duration=1.5):
    """Display loading animation with spinner"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    start_time = time.time()
    while time.time() - start_time < duration:
        sys.stdout.write(f'\r{Fore.CYAN}{Style.BRIGHT}{text} {chars[i]}{Style.RESET_ALL}')
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(chars)
    sys.stdout.write('\r' + ' ' * 50 + '\r')


def parse_proxy(proxy):
    """Parse proxy string to appropriate format"""
    if isinstance(proxy, dict):
        proxy = proxy.get('http', proxy.get('https', ''))
    if not proxy.startswith('http://') and not proxy.startswith('https://'):
        proxy = 'http://' + proxy
    return proxy


class DiabloProxyChecker:
    """Main proxy checker class with scraping and testing capabilities"""
    
    def __init__(self):
        self.working_proxies = []
        self.checked_proxies = []
        self.failed_proxies = []
        self.total_checked = 0
        self.lock = threading.Lock()
        self.start_time = None
        
    def fetch_proxies(self, num_proxies=None):
        """Fetch proxies from multiple online sources"""
        print_animated("[+] Fetching proxies from 13+ online sources...", Fore.YELLOW)
        proxies = set()
        fetched_count = 0
        
        for source in PROXY_SOURCES:
            try:
                loading_animation(f"[+] Scraping: {source[:40]}...")
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    new_proxies = set(response.text.strip().split('\n'))
                    # Filter valid proxy format (IP:PORT)
                    valid_proxies = {p.strip() for p in new_proxies if ':' in p and len(p.split(':')) == 2}
                    proxies.update(valid_proxies)
                    fetched_count += len(valid_proxies)
                    print(f"\r[+] Source: {source[:40]}... - Found {len(valid_proxies)} proxies    ")
            except Exception:
                continue
        
        proxy_list = list(proxies)
        if num_proxies and num_proxies < len(proxy_list):
            proxy_list = proxy_list[:num_proxies]
            
        print(f"\n[+] Total unique proxies fetched: {len(proxy_list)}")
        return proxy_list
    
    def check_proxy_online(self, proxy):
        """Check proxy by accessing httpbin.org/ip"""
        start_time = time.time()
        try:
            proxy_dict = {
                "http": parse_proxy(proxy),
                "https": parse_proxy(proxy)
            }
            
            response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=TIMEOUT)
            
            if response.status_code == 200:
                speed = time.time() - start_time
                with self.lock:
                    self.working_proxies.append((proxy, speed))
                    self.display_working_proxy(proxy, speed)
                return True
        except:
            pass
        
        with self.lock:
            self.failed_proxies.append(proxy)
        return False
    
    def check_proxy_local(self, proxy):
        """Check proxy by accessing example.com (for local file testing)"""
        start_time = time.time()
        try:
            proxy_dict = {
                "http": parse_proxy(proxy),
                "https": parse_proxy(proxy)
            }
            
            response = requests.get('http://www.example.com', proxies=proxy_dict, timeout=TIMEOUT)
            
            if response.status_code == 200:
                speed = time.time() - start_time
                with self.lock:
                    self.working_proxies.append((proxy, speed))
                    print(f"{Fore.GREEN}[+] WORKING: {proxy} (Speed: {speed:.2f}s){Style.RESET_ALL}")
                return True
        except:
            pass
        
        with self.lock:
            self.failed_proxies.append(proxy)
            print(f"{Fore.RED}[-] FAILED: {proxy}{Style.RESET_ALL}")
        return False
    
    def display_working_proxy(self, proxy, speed):
        """Display a working proxy in a fancy box format"""
        box = f"{Fore.CYAN}{Style.BRIGHT}╔═════════════════════════╣ {Fore.GREEN}WORKING PROXY{Fore.CYAN} ╠═════════════════════════╗\n"
        box += f"║ {Fore.WHITE}IP:PORT: {Fore.GREEN}{proxy:<52}{Fore.CYAN} \n"
        box += f"║ {Fore.WHITE}Speed: {Fore.YELLOW}{speed:.2f}s{' ' * 45}{Fore.CYAN} \n"
        box += f"╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}"
        print(box)
    
    def check_proxies_threaded(self, proxies, check_type='online', max_workers=MAX_THREADS):
        """Check proxies using multi-threading"""
        self.working_proxies = []
        self.failed_proxies = []
        self.total_checked = 0
        self.start_time = time.time()
        
        print(f"\n[+] Starting proxy check with {max_workers} threads...")
        print(f"[+] Total proxies to check: {len(proxies)}\n")
        
        # Print initial progress line
        print(f"\n[+] Progress: 0/{len(proxies)} (0.0%) Working: 0")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            if check_type == 'online':
                futures = {executor.submit(self.check_proxy_online, proxy): proxy for proxy in proxies}
            else:
                futures = {executor.submit(self.check_proxy_local, proxy): proxy for proxy in proxies}
            
            for future in as_completed(futures):
                with self.lock:
                    self.total_checked += 1
                    if self.total_checked % 5 == 0 or self.total_checked == len(proxies):
                        # Move cursor up one line to overwrite the progress line
                        progress = (self.total_checked / len(proxies)) * 100
                        sys.stdout.write(f'\033[F')  # Move cursor up one line
                        sys.stdout.write(f'\r[+] Progress: {self.total_checked}/{len(proxies)} ({progress:.1f}%) Working: {len(self.working_proxies)}')
                        sys.stdout.write('\n')  # Move to next line for new output
                        sys.stdout.flush()
        
        print(f"\n\n[+] Proxy checking complete!")
        print(f"[+] Working proxies: {len(self.working_proxies)}")
        print(f"[+] Failed proxies: {len(self.failed_proxies)}")
        print(f"[+] Total time: {time.time() - self.start_time:.2f}s")
        
        return self.working_proxies
    
    def save_proxies(self, filename, proxies, include_speed=False):
        """Save proxies to file"""
        try:
            with open(filename, 'w') as f:
                if include_speed:
                    for proxy, speed in sorted(proxies, key=lambda x: x[1]):
                        f.write(f"{proxy}\t# Speed: {speed:.2f}s\n")
                else:
                    for proxy in proxies:
                        f.write(f"{proxy}\n")
            print(f"[+] Successfully saved to: {filename}")
            return True
        except Exception as e:
            print(f"[!] Error saving file: {e}")
            return False
    
    def load_proxies_from_file(self, filename):
        """Load proxies from a local file"""
        try:
            with open(filename, 'r') as f:
                proxies = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Handle JSON format if present
                        try:
                            proxy = json.loads(line)
                            if isinstance(proxy, dict):
                                proxy = proxy.get('http', proxy.get('https', ''))
                            proxies.append(proxy)
                        except json.JSONDecodeError:
                            proxies.append(line)
                print(f"[+] Loaded {len(proxies)} proxies from {filename}")
                return proxies
        except FileNotFoundError:
            print(f"[!] File not found: {filename}")
            return []
        except Exception as e:
            print(f"[!] Error loading file: {e}")
            return []
    
    def list_files(self):
        """List all files in current directory"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
        
        print("\n[+] Files in current directory:")
        for i, file in enumerate(files, 1):
            print(f"  {i}) {file}")
        return files


def main():
    """Main function to run Diablo Proxy Tool"""
    try:
        clear_screen()
        
        # Display banner
        banner_colors = {
            'red': Fore.RED,
            'cyan': Fore.CYAN,
            'reset': Style.RESET_ALL,
            'VERSION': VERSION,
            'AUTHOR': AUTHOR
        }
        print(DIABLO_BANNER.format(**banner_colors))
        
        # Password protection
        print(f"{Fore.YELLOW}[+] Password required to access Diablo tool{Style.RESET_ALL}")
        password = input(f"{Fore.CYAN}[?] Enter password: {Style.RESET_ALL}")
        
        if password != "Illusivehacks":
            print(f"{Fore.RED}[!] Invalid password! Access denied.{Style.RESET_ALL}")
            input("\nPress Enter to exit...")
            return
        
        # Copy password to clipboard (feature from first script)
        try:
            pyperclip.copy("Illusivehacks")
            print(f"{Fore.GREEN}[+] Copied to clipboard{Style.RESET_ALL}")
        except:
            pass
        
        # Initialize checker
        checker = DiabloProxyChecker()
        
        while True:
            clear_screen()
            banner_colors = {
                'red': Fore.RED,
                'cyan': Fore.CYAN,
                'reset': Style.RESET_ALL,
                'VERSION': VERSION,
                'AUTHOR': AUTHOR
            }
            print(DIABLO_BANNER.format(**banner_colors))
            
            print(f"{Fore.CYAN}{Style.BRIGHT}[+] Diablo Main Menu:{Style.RESET_ALL}")
            print("  1) Fetch and Check Proxies (Online)")
            print("  2) Check Local Proxy File")
            print("  3) View Statistics")
            print("  4) Exit")
            
            choice = input(f"\n{Fore.YELLOW}[?] Select option (1-4): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                # Fetch and check proxies from online sources
                try:
                    num_input = input(f"\n{Fore.YELLOW}[?] How many proxies to fetch (1-10000, 0 for all): {Style.RESET_ALL}")
                    num_proxies = int(num_input) if num_input and int(num_input) > 0 else None
                except ValueError:
                    num_proxies = None
                
                proxies = checker.fetch_proxies(num_proxies)
                
                if not proxies:
                    print(f"{Fore.RED}[!] No proxies fetched. Please try again.{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    continue
                
                # Check proxies
                working = checker.check_proxies_threaded(proxies, 'online')
                
                # Ask to save results
                if working:
                    save_choice = input(f"\n{Fore.YELLOW}[?] Save working proxies to file? (y/n): {Style.RESET_ALL}").lower()
                    if save_choice == 'y':
                        filename = input(f"{Fore.YELLOW}[?] Enter filename: {Style.RESET_ALL}")
                        if not filename:
                            filename = "working_proxies.txt"
                        if not filename.endswith('.txt'):
                            filename += '.txt'
                        checker.save_proxies(filename, working, include_speed=True)
                
                input("\nPress Enter to continue...")
                
            elif choice == '2':
                # Check local proxy file
                files = checker.list_files()
                
                try:
                    file_choice = input(f"\n{Fore.YELLOW}[?] Select file number: {Style.RESET_ALL}")
                    if file_choice and file_choice.isdigit():
                        file_idx = int(file_choice) - 1
                        if 0 <= file_idx < len(files):
                            selected_file = files[file_idx]
                            proxies = checker.load_proxies_from_file(selected_file)
                            
                            if proxies:
                                print(f"\n{Fore.GREEN}[+] Checking {len(proxies)} proxies from {selected_file}{Style.RESET_ALL}")
                                working = checker.check_proxies_threaded(proxies, 'local')
                                
                                # Save locally tested proxies
                                if working:
                                    save_choice = input(f"\n{Fore.YELLOW}[?] Save locally tested working proxies? (y/n): {Style.RESET_ALL}").lower()
                                    if save_choice == 'y':
                                        filename = input(f"{Fore.YELLOW}[?] Enter filename (default: locally_tested_proxies.txt): {Style.RESET_ALL}")
                                        if not filename:
                                            filename = "locally_tested_proxies.txt"
                                        if not filename.endswith('.txt'):
                                            filename += '.txt'
                                        checker.save_proxies(filename, working, include_speed=True)
                        else:
                            print(f"{Fore.RED}[!] Invalid file selection{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[!] Invalid input{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
                
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                # View statistics
                clear_screen()
                print(f"{Fore.CYAN}{Style.BRIGHT}[+] Diablo Statistics{Style.RESET_ALL}")
                print("=" * 50)
                print(f"  Total proxies checked: {checker.total_checked}")
                print(f"  Working proxies found: {len(checker.working_proxies)}")
                print(f"  Failed proxies: {len(checker.failed_proxies)}")
                if checker.working_proxies:
                    avg_speed = sum(speed for _, speed in checker.working_proxies) / len(checker.working_proxies)
                    print(f"  Average speed: {avg_speed:.2f}s")
                    fastest = min(checker.working_proxies, key=lambda x: x[1])
                    print(f"  Fastest proxy: {fastest[0]} ({fastest[1]:.2f}s)")
                print("=" * 50)
                input("\nPress Enter to continue...")
                
            elif choice == '4':
                print(f"\n{Fore.GREEN}[+] Thank you for using Diablo by IllusiveHacks!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}[+] Stay connected: t.me/Illusivehacks{Style.RESET_ALL}")
                break
                
            else:
                print(f"{Fore.RED}[!] Invalid choice{Style.RESET_ALL}")
                time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Process interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] An error occurred: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()