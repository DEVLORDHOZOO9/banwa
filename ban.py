import smtplib
import ssl
import json
import base64
import os
import time
import random
import requests
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import getpass
import threading
import sys

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class EncryptionManager:
    def __init__(self, key_file='.key.bin'):
        self.key_file = key_file
        self.key = self._load_or_generate_key()

    def _load_or_generate_key(self):
        key_path = Path(self.key_file)
        if key_path.exists():
            with open(key_path, 'rb') as f:
                return f.read()
        else:
            new_key = get_random_bytes(32)
            with open(key_path, 'wb') as f:
                f.write(new_key)
            return new_key

    def encrypt_data(self, data):
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(iv + encrypted).decode()

    def decrypt_data(self, encrypted_data):
        data = base64.b64decode(encrypted_data)
        iv, encrypted = data[:16], data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode()

class BENWEAGACOR:
    def __init__(self, config_file='config.enc', key_file='.key.bin'):
        self.enc_manager = EncryptionManager(key_file)
        self.config_file = config_file
        self.servers = self._load_config()
        self.authenticated = False
        self.support_targets = [
            'support@whatsapp.com', 'abuse@whatsapp.com', 'info@whatsapp.com', 
            'security@whatsapp.com', 'privacy@whatsapp.com', 'phish@whatsapp.com', 
            'support@meta.com', 'abuse@meta.com', 'security@meta.com', 
            'report@meta.com', 'phish@meta.com', 'android_web@support.whatsapp.com', 
            'iphone_web@support.whatsapp.com', 'webclient_web@support.whatsapp.com', 
            'business_web@support.whatsapp.com'
        ]
        
        # Gmail configuration - HARDCODED
        self.gmail_username = "lkali8154"
        self.gmail_password = "Sembiring01"
        self.gmail_domain = "@gmail.com"
        
        # Daftar nomor telepon yang akan diproses
        self.phone_numbers = []

    def _load_config(self):
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    encrypted_data = f.read()
                    decrypted_data = self.enc_manager.decrypt_data(encrypted_data)
                    return json.loads(decrypted_data)
            except Exception as e:
                print(f"{Colors.RED}Error loading config: {e}{Colors.END}")
                return []
        else:
            return []

    def _save_config(self):
        try:
            encrypted_data = self.enc_manager.encrypt_data(json.dumps(self.servers))
            with open(self.config_file, 'w') as f:
                f.write(encrypted_data)
        except Exception as e:
            print(f"{Colors.RED}Error saving config: {e}{Colors.END}")

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _show_loading_bar(self, duration=5, message="Loading"):
        """Menampilkan loading bar yang keren"""
        bar_length = 50
        steps = 20
        delay = duration / steps
        
        print(f"\n{Colors.CYAN}{message}...{Colors.END}")
        print(f"{Colors.BLUE}[{Colors.END}", end="")
        
        for i in range(steps + 1):
            progress = i / steps
            bars = int(bar_length * progress)
            spaces = bar_length - bars
            
            # Tampilkan progress bar dengan animasi
            sys.stdout.write('\r')
            sys.stdout.write(f"{Colors.BLUE}[{Colors.GREEN}{'=' * bars}{Colors.CYAN}{'>' if i < steps else '='}{Colors.WHITE}{'.' * spaces}{Colors.BLUE}]{Colors.END}")
            sys.stdout.write(f" {Colors.YELLOW}{int(progress * 100)}%{Colors.END}")
            sys.stdout.flush()
            time.sleep(delay)
        
        print(f"\n{Colors.GREEN}✅ {message} Complete!{Colors.END}")

    def _check_password(self):
        try:
            response = requests.get('https://github.com/DEVLORDHOZOO9/banwa/blob/main/pw.txt', timeout=10)
            if response.status_code == 200:
                correct_password = response.text.strip()
                entered_password = getpass.getpass(f'{Colors.CYAN}🔐 MASUKKAN PASSWORD: {Colors.END}')
                if entered_password == correct_password:
                    self._show_loading_bar(3, "Verifying Access")
                    self._show_epic_animation(f'{Colors.GREEN}[✓] AKSES DITERIMA! BEN WEA GACOR AKTIF{Colors.END}')
                    self.authenticated = True
                    time.sleep(2)
                    return True
                else:
                    self._animate_text(f'{Colors.RED}[!] PASSWORD SALAH!{Colors.END}', 'red')
                    self._show_wrong_password_animation()
                    print(f'{Colors.YELLOW}📞 Hubungi: 6283852751527{Colors.END}')
                    threading.Timer(1.0, lambda: os.system('xdg-open \'https://wa.me/+628999859595?text=KAKSAYAMAUBELIUNBANBEAPABULANKAK??\'')).start()
                    time.sleep(3)
                    return False
            else:
                self._animate_text(f'{Colors.RED}[!] Gagal mengambil password dari server{Colors.END}', 'red')
                return False
        except Exception as e:
            self._animate_text(f'{Colors.RED}[!] Verifikasi password gagal: {str(e)}{Colors.END}', 'red')
            return False

    def _show_wrong_password_animation(self):
        frames = [f'{Colors.RED}🚫 ACCESS DENIED 🚫{Colors.END}', 
                 f'{Colors.RED}🚨 INTRUDER ALERT 🚨{Colors.END}', 
                 f'{Colors.YELLOW}⛔  UNAUTHORIZED ACCESS ⛔{Colors.END}', 
                 f'{Colors.RED}🔐 WRONG PASSWORD 🔐{Colors.END}']
        for _ in range(3):
            for frame in frames:
                sys.stdout.write('\r' + frame)
                sys.stdout.flush()
                time.sleep(0.3)

    def _animate_text(self, text, color='green', speed=0.03):
        color_codes = {'green': Colors.GREEN, 'red': Colors.RED, 'yellow': Colors.YELLOW, 
                      'blue': Colors.BLUE, 'cyan': Colors.CYAN, 'magenta': Colors.MAGENTA, 
                      'white': Colors.WHITE, 'reset': Colors.END}
        for char in text:
            print(f"{color_codes.get(color, '')}{char}{color_codes['reset']}", end='', flush=True)
            time.sleep(speed)
        print()

    def _show_epic_animation(self, message):
        self._clear_screen()
        matrix_chars = '▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░▓▒░'
        for i in range(10):
            print(f"{Colors.GREEN}{''.join(random.choice(matrix_chars) for _ in range(60))}{Colors.END}")
            time.sleep(0.05)
        self._clear_screen()
        print(message)

    def load_phone_numbers(self):
        """Memuat atau membuat daftar nomor telepon"""
        print(f"\n{Colors.CYAN}📱 MANAGER NOMOR TELEPON{Colors.END}")
        
        # Contoh nomor telepon Indonesia
        default_numbers = [
            "+628123456789",
            "+628987654321", 
            "+628112233445",
            "+628556677889",
            "+628998877665"
        ]
        
        print(f"{Colors.YELLOW}1. Gunakan nomor default (5 nomor)")
        print(f"2. Masukkan nomor manual")
        print(f"3. Load dari file{Colors.END}")
        
        choice = input(f"\n{Colors.CYAN}Pilih opsi (1-3): {Colors.END}").strip()
        
        if choice == '1':
            self.phone_numbers = default_numbers
            print(f"{Colors.GREEN}✅ Menggunakan {len(default_numbers)} nomor default{Colors.END}")
        elif choice == '2':
            self._input_manual_numbers()
        elif choice == '3':
            self._load_numbers_from_file()
        else:
            self.phone_numbers = default_numbers
            print(f"{Colors.YELLOW}⚠️  Pilihan tidak valid, menggunakan nomor default{Colors.END}")
        
        # Tampilkan nomor yang dimuat
        print(f"\n{Colors.GREEN}📋 DAFTAR NOMOR YANG AKAN DIPROSES:{Colors.END}")
        for i, number in enumerate(self.phone_numbers, 1):
            print(f"   {i}. {number}")

    def _input_manual_numbers(self):
        """Input nomor telepon manual"""
        print(f"\n{Colors.YELLOW}Masukkan nomor telepon (format: +628xxxxxxxxx){Colors.END}")
        print(f"{Colors.YELLOW}Ketik 'selesai' ketika sudah selesai{Colors.END}")
        
        while True:
            number = input(f"{Colors.CYAN}Nomor {len(self.phone_numbers) + 1}: {Colors.END}").strip()
            if number.lower() == 'selesai':
                break
            if number and number.startswith('+'):
                self.phone_numbers.append(number)
                print(f"{Colors.GREEN}✅ Nomor ditambahkan!{Colors.END}")
            else:
                print(f"{Colors.RED}❌ Format nomor tidak valid!{Colors.END}")
        
        if not self.phone_numbers:
            print(f"{Colors.YELLOW}⚠️  Tidak ada nomor yang dimasukkan, menggunakan default{Colors.END}")
            self.phone_numbers = ["+628123456789", "+628987654321"]

    def _load_numbers_from_file(self):
        """Load nomor dari file"""
        filename = input(f"{Colors.CYAN}Masukkan nama file: {Colors.END}").strip()
        try:
            with open(filename, 'r') as f:
                numbers = [line.strip() for line in f if line.strip()]
                self.phone_numbers = numbers
                print(f"{Colors.GREEN}✅ Load {len(numbers)} nomor dari file{Colors.END}")
        except:
            print(f"{Colors.RED}❌ Gagal load file, menggunakan nomor default{Colors.END}")
            self.phone_numbers = ["+628123456789", "+628987654321"]

    def generate_custom_message(self, phone_number):
        """Generate pesan custom berdasarkan nomor telepon"""
        base_message = """Dear WhatsApp Support Team,

I hope you are doing well. I recently found out that my WhatsApp account has been banned. I'm not sure why, but I've always tried to use WhatsApp responsibly. If I broke any rules without knowing, I truly apologize.

Please review my account. I promise to follow all WhatsApp guidelines from now on. Thank you for your time and help.

Best regards,"""
        
        return f"{base_message}\n{phone_number}"

    def auto_setup_gmail(self):
        """Setup Gmail SMTP secara otomatis dengan credentials yang sudah ditentukan"""
        self._show_loading_bar(3, "Setting up Gmail SMTP")
        
        full_email = f"{self.gmail_username}{self.gmail_domain}"
        
        gmail_config = {
            'host': 'smtp.gmail.com',
            'port': 587,
            'email': full_email,
            'password': self.gmail_password
        }
        
        print(f"{Colors.YELLOW}🔧 Menggunakan Gmail: {full_email}{Colors.END}")
        print(f"{Colors.YELLOW}🔑 Password: {'*' * len(self.gmail_password)}{Colors.END}")
        
        # Test koneksi
        print(f"{Colors.CYAN}🧪 Testing koneksi ke Gmail SMTP...{Colors.END}")
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(gmail_config['host'], gmail_config['port']) as server:
                server.starttls(context=context)
                server.login(gmail_config['email'], gmail_config['password'])
                print(f"{Colors.GREEN}[✓] Koneksi Gmail berhasil!{Colors.END}")
                
                # Simpan konfigurasi
                self.servers = [gmail_config]
                self._save_config()
                return True
                
        except smtplib.SMTPAuthenticationError:
            print(f"{Colors.RED}[!] Gagal autentikasi Gmail{Colors.END}")
            return False
        except Exception as e:
            print(f"{Colors.RED}[!] Gagal koneksi ke Gmail: {e}{Colors.END}")
            return False

    def send_unlimited_emails(self):
        """Kirim email unlimited ke semua target WhatsApp"""
        if not self.servers:
            print(f"{Colors.RED}[!] Tidak ada server SMTP! Setup otomatis...{Colors.END}")
            if not self.auto_setup_gmail():
                return False

        # Load nomor telepon jika belum ada
        if not self.phone_numbers:
            self.load_phone_numbers()

        # Konfigurasi email
        subject = "Permohonan Review Akun WhatsApp - Account Ban Appeal"
        base_message = """Dear WhatsApp Support Team,

I hope you are doing well. I recently found out that my WhatsApp account has been banned. I'm not sure why, but I've always tried to use WhatsApp responsibly. If I broke any rules without knowing, I truly apologize.

Please review my account. I promise to follow all WhatsApp guidelines from now on. Thank you for your time and help.

Best regards,"""

        # Tampilkan konfigurasi
        print(f"\n{Colors.GREEN}✅ KONFIGURASI EMAIL:{Colors.END}")
        print(f"{Colors.CYAN}📧 Subject: {subject}{Colors.END}")
        print(f"{Colors.CYAN}📝 Message: Custom untuk setiap nomor telepon{Colors.END}")
        print(f"{Colors.CYAN}📱 Nomor Telepon: {len(self.phone_numbers)} nomor{Colors.END}")
        print(f"{Colors.CYAN}🎯 Target Email: {len(self.support_targets)} alamat{Colors.END}")
        print(f"{Colors.CYAN}🔧 Server: {self.servers[0]['email']}{Colors.END}")

        # Konfirmasi pengiriman unlimited
        print(f"\n{Colors.RED}⚠️  MODE UNLIMITED AKTIF!{Colors.END}")
        print(f"{Colors.YELLOW}♾️  Pengiriman akan berjalan terus sampai dihentikan (Ctrl+C){Colors.END}")
        
        confirm = input(f"\n{Colors.RED}Lanjutkan pengiriman UNLIMITED? (y/n): {Colors.END}").strip().lower()
        if confirm != 'y':
            print(f"{Colors.YELLOW}Pengiriman dibatalkan.{Colors.END}")
            return False

        # Mulai pengiriman unlimited
        return self._start_unlimited_sending(subject, base_message)

    def _start_unlimited_sending(self, subject, base_message):
        """Mulai pengiriman email unlimited"""
        print(f"\n{Colors.GREEN}🚀 MULAI PENGIRIMAN UNLIMITED...{Colors.END}")
        print(f"{Colors.CYAN}⏰ Waktu mulai: {time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        
        total_sent = 0
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n{Colors.BOLD}{Colors.MAGENTA}=== ITERASI {iteration} ==={Colors.END}")
                
                # Kirim ke semua target dengan semua nomor
                sent_this_iteration = self._send_to_all_targets(subject, base_message, iteration)
                total_sent += sent_this_iteration
                
                # Tampilkan statistik
                print(f"{Colors.GREEN}📊 Iterasi {iteration} selesai!")
                print(f"📨 Berhasil dikirim: {sent_this_iteration} email")
                print(f"📈 Total terkirim: {total_sent} email")
                print(f"📱 Nomor diproses: {len(self.phone_numbers)} nomor")
                print(f"⏰ Waktu: {time.strftime('%H:%M:%S')}{Colors.END}")
                
                # Jeda sebelum iterasi berikutnya
                print(f"{Colors.YELLOW}⏳ Menunggu 20 detik untuk iterasi berikutnya...{Colors.END}")
                self._show_loading_bar(20, "Preparing next iteration")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⏹️  Pengiriman dihentikan oleh user{Colors.END}")
            print(f"{Colors.GREEN}🎯 TOTAL EMAIL TERKIRIM: {total_sent}{Colors.END}")
            print(f"{Colors.GREEN}📱 TOTAL NOMOR DIPROSES: {len(self.phone_numbers)}{Colors.END}")
            print(f"{Colors.GREEN}⏰ Waktu selesai: {time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
            return False

    def _send_to_all_targets(self, subject, base_message, iteration):
        """Kirim email ke semua target dalam satu iterasi"""
        successful_sends = 0
        total_targets = len(self.support_targets)
        
        print(f"{Colors.CYAN}🎯 Mengirim ke {total_targets} target dengan {len(self.phone_numbers)} nomor...{Colors.END}")
        
        for i, target_email in enumerate(self.support_targets, 1):
            try:
                # Progress bar untuk setiap target
                progress_percent = (i / total_targets) * 100
                bars = int(progress_percent / 2)
                sys.stdout.write(f'\r📤 [{Colors.GREEN}{"="*bars}{Colors.CYAN}{">" if i < total_targets else "="}{Colors.WHITE}{"."*(50-bars)}{Colors.CYAN}] {i}/{total_targets} ({progress_percent:.1f}%) - {target_email}{Colors.END}')
                sys.stdout.flush()
                
                # Kirim email untuk setiap nomor telepon
                for phone_number in self.phone_numbers:
                    custom_message = self.generate_custom_message(phone_number)
                    if self._send_single_email(self.servers[0], target_email, subject, custom_message, iteration, phone_number):
                        successful_sends += 1
                        time.sleep(0.5)  # Jeda singkat antar pengiriman
                
            except Exception as e:
                print(f"\n{Colors.RED}[!] Error mengirim ke {target_email}: {e}{Colors.END}")
        
        print()  # New line setelah progress complete
        return successful_sends

    def _send_single_email(self, server, target_email, subject, message, iteration, phone_number):
        """Kirim single email dengan handling error yang lebih baik"""
        try:
            # Buat pesan email
            msg = MIMEMultipart()
            msg['From'] = server['email']
            msg['To'] = target_email
            
            # Variasikan subject
            variations = ["", " - Urgent", " - Important", " - Request", " - Appeal"]
            variation = random.choice(variations)
            msg['Subject'] = f"{subject}{variation} | Batch {iteration} | {phone_number}"
            
            # Template email profesional
            email_body = f"""
{message}

---
Iteration: {iteration}
Phone Number: {phone_number}
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
Sent via: Automated Appeal System
"""
            
            msg.attach(MIMEText(email_body, 'plain'))
            
            # Kirim email dengan timeout
            context = ssl.create_default_context()
            with smtplib.SMTP(server['host'], server['port'], timeout=30) as smtp_server:
                smtp_server.starttls(context=context)
                smtp_server.login(server['email'], server['password'])
                smtp_server.send_message(msg)
            
            # Tampilkan status berhasil dengan loading effect
            sys.stdout.write(f'\r{Colors.GREEN}✅ Berhasil dikirim ke {target_email} untuk nomor {phone_number}{" " * 50}{Colors.END}\n')
            sys.stdout.flush()
            
            return True
            
        except Exception as e:
            sys.stdout.write(f'\r{Colors.RED}❌ Gagal mengirim ke {target_email} untuk {phone_number}: {e}{" " * 50}{Colors.END}\n')
            sys.stdout.flush()
            return False

    def run_enhanced_mode(self):
        """Jalankan mode enhanced dengan semua fitur baru"""
        if not self._check_password():
            return
        
        self._clear_screen()
        print(f"\n{Colors.BOLD}{Colors.RED}" + "="*80)
        print("           🚀 BEN WEA GACOR - ENHANCED UNLIMITED MODE 🚀")
        print("="*80 + f"{Colors.END}")
        
        print(f"\n{Colors.YELLOW}⚠️  FITUR UNLIMITED EMAIL DENGAN NOMOR TELEPON{Colors.END}")
        print(f"{Colors.CYAN}📧 Gmail: {self.gmail_username}{self.gmail_domain}")
        print(f"🔑 Password: {'*' * len(self.gmail_password)}")
        print(f"📱 Fitur: Multiple phone number support")
        print(f"🎯 Target: {len(self.support_targets)} email WhatsApp/Meta")
        print(f"🔄 Mode: Pengiriman berulang otomatis")
        print(f"♾️  Akan berjalan sampai dihentikan manual (Ctrl+C){Colors.END}")
        
        # Setup SMTP otomatis
        if not self.servers:
            print(f"\n{Colors.YELLOW}📧 Setup SMTP otomatis...{Colors.END}")
            if not self.auto_setup_gmail():
                print(f"{Colors.RED}❌ Gagal setup SMTP. Program dihentikan.{Colors.END}")
                return
        
        # Load nomor telepon
        self.load_phone_numbers()
        
        # Tampilkan konfigurasi lengkap
        print(f"\n{Colors.GREEN}✅ KONFIGURASI SIAP:{Colors.END}")
        print(f"   📧 Server: {self.servers[0]['email']}")
        print(f"   🌐 Host: {self.servers[0]['host']}:{self.servers[0]['port']}")
        print(f"   📱 Nomor: {len(self.phone_numbers)} nomor telepon")
        print(f"   🎯 Target: {len(self.support_targets)} email support")
        print(f"   💬 Template: Appeal message untuk unbanned WhatsApp{Colors.END}")
        
        # Tampilkan contoh message
        print(f"\n{Colors.CYAN}📝 CONTOH PESAN:{Colors.END}")
        sample_message = self.generate_custom_message(self.phone_numbers[0])
        print(f"{Colors.WHITE}{sample_message[:200]}...{Colors.END}")
        
        # Mulai pengiriman unlimited
        print(f"\n{Colors.RED}🎯 MEMULAI PENGIRIMAN UNLIMITED DENGAN FITUR BARU...{Colors.END}")
        self._show_loading_bar(5, "Initializing Enhanced System")
        self.send_unlimited_emails()

def main():
    try:
        app = BENWEAGACOR()
        app.run_enhanced_mode()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⏹️  Program dihentikan oleh pengguna.{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")

if __name__ == "__main__":
    main()
