import os 
import datetime
from colorama import Fore, Style

def clear_console():
    match os.name: # Penyesuaian ke sistem operasi
                case "nt": os.system("cls")
                case "posix": os.system("clear")

# Fungsi untuk menyimpan output / hasil operasi ke dalam arsip
def save_output(output, choice):
    # Membuat direktori untuk menyimpan arsip jika belum ada
    if not os.path.exists("Arsip Output"):
        os.makedirs("Arsip Output")

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    ArsipData = f"Arsip Output/{choice}_{current_time}.txt"
    with open(ArsipData, "w", encoding="utf-8") as file:
        file.write(str(output))
    print(f"Output telah disimpan ke dalam arsip: {ArsipData}")
    print("-"*50)

def isSave(output):
        isSimpan = input("Apakah output perlu disimpan? (y/n) : ")
        
        if(isSimpan == 'y' or isSimpan == 'Y'):
            choice = input("Nama File (untuk disimpan) : ")
            save_output(output, choice)
        else :
            print("Output tidak disimpan")
            print("-"*50)

class Menu:
    # Data Member : private int pilihan, private bool isLoop 
    
    # Konstruktor
    def __init__(self):
        self.__isLoop = True
        
    # Akses Private (Mulai)
    # Menampilkan Menu Utama
    def __printMenu(self):
        print("-"*50)
        print(Fore.YELLOW + "\t   KALKULATOR ALJABAR LINEAR")
        print(Style.RESET_ALL + "-"*50)
        print(Fore.CYAN + "         Farras Arkan Wardana - L0123052")
        print("\t  Fathoni Nur Habibi - L0123054")
        print("\t  Ivan Wahyu Nugroho - L0123068")
        print(Style.RESET_ALL +"-"*50)
        print(Fore.YELLOW + "\t\t Menu Kalkulator".upper())
        print(Style.RESET_ALL + "-"*50)
        print("1. Sistem Persamaan Linier")
        print("2. Determinan Matriks")
        print("3. Matriks Invers")
        print("4. Transpose Matriks")
        print("5. Operasi Aritmatika Matriks")
        print("6. LU Faktorisasi")
        print("7. Eigen Value, Eigen Vektor, dan Polinomial Karakteristiknya")
        print("8. Diagonalisasi Matriks")
        print("9. Singular Value Decomposition (SVD)")
        print("0. Keluar")
        print("-"*50)
        print("Masukkan Pilihan Anda : ", end='')
    
    # Menampilkan submenu
    def __printSubMenu(self):
        submenu = ""
        match self.getPilihan():
            case 1: submenu = "sistem persamaan linear".upper()
            case 2: submenu = "determinan matriks".upper()
            case 3: submenu = "matriks invers".upper()
        print(f"SUBMENU {submenu}")
        print("1. Metode Eliminasi Gauss")
        print("2. Metode Eliminasi Gauss-Jordan")
        print("3. Metode Balikan Matriks")
        print("-"*50)
        print("Masukkan Pilihan : ", end='')
    
    # Sub Menu bagian operasi aritmatika matriks
    def __subMenuAritmatikaMatriks(self):
        print("1. Perkalian")
        print("2. Penjumlahan atau Pengurangan")
        print("-"*50)
        print("Masukkan Pilihan : ", end='')
    
    # Setter untuk pilihan 
    def __setPilihan(self, pilihan:int):
        self.__pilihan = pilihan
    # Akses Private (Selesai)
    
    # Akses Public (Mulai)
    # Getter untuk pilihan
    getPilihan = lambda self : self.__pilihan
    
    # Getter untuk isLoop
    def getIsLoop(self) ->bool:
        return self.__isLoop
    
    # Setter untuk isLoop
    def setisLoop(self, isLoop:bool):
        self.__isLoop = isLoop
        
    # Menampilkan Menu
    def showMenu(self):
        self.__printMenu()
        choice = int(input())
        self.__setPilihan(choice)
        clear_console()
        
    # Menampilkan Submenu
    def showSubMenu(self):
        self.__printSubMenu()
        choice = int(input())
        self.__setPilihan(choice)
        clear_console()
    
    # Menampilkan SubMenu untuk operasi aritmatika matriks
    def showMenuAritmatika(self):
        self.__subMenuAritmatikaMatriks()
        choice = int(input())
        self.__setPilihan(choice)
        clear_console()
    
    def backTo(self):
        back = str(input("Kembali Ke Menu (y/n) : "))
        
        # Memberikan pengembalian ke menu atau tidak
        self.setisLoop(True) if (back == 'y' or back == 'Y') else self.setisLoop(False)
        
        # Jika kembali ke menu, maka console akan dibersihkan
        clear_console() if self.getIsLoop() else ""
        
    # Akses Public (Selesai)