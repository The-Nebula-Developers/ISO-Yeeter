from pystyle import Colors,Write,Box,Center
import json 
from rich.table import Table
from rich.console import Console 
#from rich import print_json
import aiohttp
import asyncio

logs_files = "logs//logs.txt"
config_file_location = "config.json"

class Banner: 
    def __init__(self): 
        pass

    def display_banner(self): 
        try:
            banner = '''
██╗███████╗ ██████╗     ██╗   ██╗███████╗███████╗████████╗███████╗██████╗ 
██║██╔════╝██╔═══██╗    ╚██╗ ██╔╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██║███████╗██║   ██║     ╚████╔╝ █████╗  █████╗     ██║   █████╗  ██████╔╝
██║╚════██║██║   ██║      ╚██╔╝  ██╔══╝  ██╔══╝     ██║   ██╔══╝  ██╔══██╗
██║███████║╚██████╔╝       ██║   ███████╗███████╗   ██║   ███████╗██║  ██║
╚═╝╚══════╝ ╚═════╝        ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
'''
            secondary_text = '''Designed by The Nebula Developer\nHave Fun Yeeting ISOs!'''

            Write.Print(Center.XCenter(banner),Colors.red_to_purple,interval=0.0025)
            print("")
            Write.Print(Box.Lines(secondary_text), Colors.red_to_purple, interval=0.0025)
            print("")
        except Exception as e: 
            with open(logs_files, "a") as log_file:
                log_file.writelines(f"\n[-] Error: Could not Display Banner - {e}")
            Write.Print(f"[-] Error: Could not Display Banner - {e}\n", Colors.red, interval=0.0025)

class Downloader:
    def __init__(self): pass

    def tabler(self,data, title,**kwargs):
            try:
                table = Table(title=title, show_header=True, header_style="bold magenta", style="red")
                table.add_column("Selector", style="cyan", justify="center")
                table.add_column("ISO", style="green", justify="center")

                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, dict):
                            for inner_key, inner_value in value.items():
                                table.add_row(inner_key, str(inner_value["details"]))
                                table.add_row("—" * 20, "—" * 20)
                        else:
                            table.add_row(key, str(value))
                console = Console()
                console.print(table, justify="center")
                with open(logs_files, "a") as log_file:
                    log_file.writelines(f"\n[+] Success: Printed Table")
            except Exception as e:
                with open(logs_files, "a") as log_file:
                    log_file.writelines(f"\n[-] Error: Table Could not be displayed - {e}")
                Write.Print(f"[-] Error: Table Could not be displayed - {e}\n", Colors.red, interval=0.0025)

    def open_iso_data(self,config_file_location):
        try:
            with open(config_file_location,"r") as iso_data_file: 
                iso_data = json.load(iso_data_file)
            return iso_data
        except Exception as e: 
            with open(logs_files, "a") as log_file:
                log_file.writelines(f"\n[-] Error: Could not Load data from Config File - {e}")
            Write.Print(f"[-] Error: Could not Load data from Config File - {e}\n", Colors.red, interval=0.0025)

    def select_iso(self,iso_data):    
        try:
            selected = Write.Input("""
Enter ISO to Download from Available ones on Table
==> """, Colors.red_to_purple,interval=0.0025)        
            selected_value = None
            for key in iso_data["mirrors"]:
                if selected.lower() == key.lower():
                    selected_value = iso_data["mirrors"][key]
                    Write.Print(f"""\nStarted Download of {key}\n""", Colors.red_to_purple,interval=0.0025)
                    return selected_value
            Write.Print("\nThe Entered Selection is not valid! Select a Valid Option!\n",Colors.light_green, interval=0.0025)
            return self.select_iso(iso_data)
        except Exception as e: 
            with open(logs_files, "a") as log_file:
                log_file.writelines(f"\n[-] Error: Could not Select ISO - {e}")
            Write.Print(f"[-] Error: Could not Select ISO - {e}\n", Colors.red, interval=0.0025)

    async def download_file(self, url, filename):
        try:
            timeout = aiohttp.ClientTimeout(total=None) 
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        with open(filename, 'wb') as f:
                            console = Console()
                            with console.status("[bold cyan]Downloading...", spinner="dots") as status:
                                while True:
                                    chunk = await response.content.read(1024*1024)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                            console.print("[green]Download complete")
                            with open(logs_files, "a") as log_file:
                                log_file.writelines(f"\n[+] Success: Downloaded ISO from {url}")
                            Write.Print(f"[+] Success: Downloaded ISO from {url}\n", Colors.light_green, interval=0.0025)
                    else:
                        with open(logs_files, "a") as log_file:
                            log_file.writelines(f"\n[-] Error: Failed to download {filename}")
                        Write.Print(f"[-] Error: Failed to download {filename}\n", Colors.red, interval=0.0025)
        except Exception as e: 
            with open(logs_files, "a") as log_file:
                log_file.writelines(f"\n[-] Error: Could not Download ISO - {e}")
            Write.Print(f"[-] Error: Could not Download ISO - {e}\n", Colors.red, interval=0.0025)

    async def download(self,iso_url,save_path):
        try:
            await self.download_file(iso_url, save_path)
        except Exception as e: 
            with open(logs_files, "a") as log_file:
                log_file.writelines(f"\n[-] Error: Could not Download ISO - {e}")
            Write.Print(f"[-] Error: Could not Download ISO - {e}\n", Colors.red, interval=0.0025)

    async def download(self,iso_url,save_path):
        await self.download_file(iso_url, save_path)

    def downloader_main(self): 
        try:
            iso_data = self.open_iso_data(config_file_location=config_file_location)
            self.tabler(data=iso_data,title="Available ISOs")
            data = self.select_iso(iso_data)
            if data == None: 
                Write.Print(f"[-] System Error!\n", Colors.red, interval=0.0025)
                with open(logs_files, "a") as log_file:
                    log_file.writelines(f"\n[-] Returned Selection Data is invalid!")
            else: 
                asyncio.run(self.download(data["download"],data["save-name"]))
                with open(logs_files, "a") as log_file:
                    log_file.writelines(f"\n[+] Sucess: Downloaded ISO to {data['save-name']}")
                Write.Print(f"[+] Sucess: Downloaded ISO to {data['save-name']}\n", Colors.light_green, interval=0.0025)
        except Exception as e: 
            with open(logs_files, "a") as log_file:
                log_file.writelines(f"\n[-] Error: Internal System Error - {e}")
            Write.Print(f"[-] Error: Internal System Error - {e}\n", Colors.red, interval=0.0025)
        except KeyboardInterrupt: 
            with open(logs_files, "a") as log_file:
                log_file.writelines(f"\n[-] Error: User Interrupted System - Aborting!")
            Write.Print(f"[-] Error: User Interrupted System - Aborting!\n", Colors.red, interval=0.0025)

class Systems: 
    def __init__(self): pass

    def main(self): 
        banner = Banner()
        banner.display_banner()
        download_system = Downloader()
        download_system.downloader_main()

system = Systems()
system.main()