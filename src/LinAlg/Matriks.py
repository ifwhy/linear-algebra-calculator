import numpy as np
import sympy as sp
import scipy.linalg as sl
import tabulate as tl
from colorama import Fore, Style
import math
from .Menu import isSave
sp.init_printing()
np.set_printoptions(precision=5, suppress=True, linewidth=100, floatmode='fixed')

class Matriks:
    # Data Member : private data, shape
    
    # Konstruktor untuk kelas Matriks
    def __init__(self, data:list):
        self.__data = np.array(data)
        self.__shape = self.__data.shape
    
    # Mengambil input dari user
    def takeInput(self):
        print("-"*50)
        print("Masukkan Ordo Matriks")
        baris = int(input("Banyaknya Baris : "))
        kolom = int(input("Banyaknya Kolom : "))
        print("-"*50)
        
        try:
            if(baris > 0 and kolom > 0):
                print("Masukkan Elemen Matriks Tiap Baris (pisahkan dengan tanda spasi)")
                print(f"Masukkan {kolom} Elemen Setiap Baris")
                print("-"*50)
                
                matriks = []
                for i in range(baris):
                    userInput = input(f"Baris ke-{i+1} : ").split()
                    numberInput = [float(num) for num in userInput]
                    matriks.append(numberInput)
                print("-"*50)
                
                # Mengecek apakah matriks yang diberikan sesuai ordo atau tidak
                if(len(matriks) == baris and len(matriks[0]) == kolom):
                    self.__data = np.array(matriks)     
                else:
                    print("Matriks yang Anda masukkan tidak sesuai dengan ordo yang Anda masukkan")
            else:
                print("Ordo Matriks Salah!")   
        except ValueError:
            print("Masukan Anda Salah!")
    
    # Mengambil input matriks persegi
    def takeSquareInput(self):
        print("-"*50)
        print("Masukkan Ordo Matriks Persegi")
        kolom = int(input("Baris/Kolom : "))
        print("-"*50)
        
        try:
            if(kolom > 0):
                print("Masukkan Elemen Matriks Tiap Baris (pisahkan dengan tanda spasi)")
                print(f"Masukkan {kolom} Elemen Setiap Baris")
                print("-"*50)
                
                matriks = []
                for i in range(kolom):
                    userInput = input(f"Baris ke-{i+1} : ").split()
                    numberInput = [float(num) for num in userInput]
                    matriks.append(numberInput)
                print("-"*50)
                
                # Mengecek apakah matriks yang diberikan sesuai ordo atau tidak
                if(len(matriks) == kolom and len(matriks[0]) == kolom):
                    self.__data = np.array(matriks)     
                else:
                    print("Matriks yang Anda masukkan tidak sesuai dengan ordo yang Anda masukkan")
            else:
                print("Ordo Matriks Salah!")
        except:
            print("Masukan Anda salah!")
    
    # Getter untuk data
    getData = lambda self: self.__data
    
    # Mencetak matriks
    def showMatriks(self, data:np.array):
        print("Matriks Anda : ")
        print(data)
        print("-"*50)
    
    # LU Factorization
    def __LUFactorization(self, data:np.array) ->tuple:
        P, L, U = sl.lu(data)
        return (P, L, U)
    def printLUFactorization(self):
        P, L, U = self.__LUFactorization(self.getData())

        print("Matriks Awal (A) : ")
        print(tl.tabulate(self.getData(), tablefmt="fancy_grid"))
        print("Matriks Permutasi (P) : ")
        print(tl.tabulate(P, tablefmt="fancy_grid"))
        print("\nMatriks Lower (L) : ")
        print(tl.tabulate(L, tablefmt="fancy_grid"))
        print("\nMatriks Upper (U) : ")
        print(tl.tabulate(U, tablefmt="fancy_grid"))
        
        print("\nValdidasi : ".upper())
        product1 = np.dot(L, U)
        product2 = np.dot(P, self.getData())
        toleransi = 1e-8
        if(np.all(np.abs(product1 - product2)) < toleransi):
            tambahan = "BENAR"
        else:
            tambahan = "SALAH"
        print(f"Apakah LU = PA ? : {tambahan}")
        print("-"*50)
        
        output = ""
        output += "lu factorization\n".upper()
        output += "-"*50
        output += f"\nBanyak Baris : {self.getData().shape[0]}\n"
        output += f"Banyak Kolom : {self.getData().shape[1]}\n"
        output += "-"*50
        output += "\bMatriks yang Anda inputkan (A) : \n"
        output += tl.tabulate(self.getData(), tablefmt="fancy_grid")
        output += "\n\nMatriks Permutasi (P) : \n"
        output += tl.tabulate(P, tablefmt="fancy_grid")
        output += "\n\nMatriks Lower (L) : \n"
        output += tl.tabulate(L, tablefmt="fancy_grid")
        output += "\n\nMatriks Upper (U) : \n"
        output += tl.tabulate(U, tablefmt="fancy_grid")
        output += "\n\nValidasi : \n"
        output += f"Apakah LU = PA ? : {tambahan}\n"
        output += "-"*50
        isSave(output, "LU_Factorization")
    
    # Determinan matriks
    def det(self, data:np.array) -> np.array:
        if(data.shape[0] != data.shape[1]):
            return "Matriks Tidak Berbentuk Persegi"
        return np.linalg.det(data) 
    
    # Metode Gaussian untuk Determinan
    def __determinan_dan_bentuk_eselon(self):
        # Mengonversi matriks input ke tipe data floating-point
        matriks_eselon = self.getData().astype(float)

        # Mendapatkan jumlah baris dan kolom dalam matriks
        num_baris, num_kolom = matriks_eselon.shape

        # Inisialisasi variabel untuk melacak baris pivot saat ini
        baris_pivot = 0

        # Iterasi di setiap kolom
        for j in range(num_kolom):
            # Menemukan elemen non-nol pertama dalam kolom saat ini di bawah baris pivot saat ini
            indeks_non_nol = np.nonzero(matriks_eselon[baris_pivot:, j])[0]
            if indeks_non_nol.size == 0:
                continue  # Pindah ke kolom berikutnya jika semua elemen nol
            baris_pivot_index = baris_pivot + indeks_non_nol[0]

            # Menukar baris saat ini dengan baris pivot
            matriks_eselon[[baris_pivot, baris_pivot_index]] = matriks_eselon[[baris_pivot_index, baris_pivot]]

            # Nolkan elemen di bawah elemen pivot dalam kolom saat ini
            for i in range(baris_pivot + 1, num_baris):
                faktor = matriks_eselon[i, j] / matriks_eselon[baris_pivot, j]
                matriks_eselon[i, j:] -= faktor * matriks_eselon[baris_pivot, j:]

            # Memindah ke baris pivot berikutnya
            baris_pivot += 1

            # Menghentikan pengulangan jika baris pivot melebihi jumlah baris
            if baris_pivot >= num_baris:
                break

        # Ekstrak elemen diagonal dari bentuk eselon
        elemen_diagonal = np.diag(matriks_eselon)

        # Kembalikan determinan dan bentuk eselon sebagai tuple
        return (elemen_diagonal, matriks_eselon)
    
    def printGaussianDet(self):
        elemen_diagonal, echelon_form = self.__determinan_dan_bentuk_eselon()
        print("Matriks Echelon : ")
        print(tl.tabulate(echelon_form, tablefmt="fancy_grid"))
        print("\nDeterminan sama dengan hasil perkalian dari elemen\npada diagonal utama matriks echelon di atas")
        count = 0
        for i in elemen_diagonal:
            if count == len(elemen_diagonal) - 1:
                print(i.round(5), end='')
            else:
                print(f"{i.round(5)} * ", end="")
            count += 1
        print(f"1 = {np.prod(elemen_diagonal).round(5)}")
        print(f"\nDeterminan : {np.linalg.det(self.getData()).round(5)}")
        print("-"*50)
        
        output = ""
        output += "Invers matriks dengan eliminasi gauss jordan\n".upper()
        output += "-"*50 + "\n"
        output += "Matriks yang Anda inputkan : \n"
        output += tl.tabulate(self.getData(), tablefmt="fancy_grid")
        output += "\nMatriks Echelon : \n"
        output += tl.tabulate(echelon_form, tablefmt="fancy_grid")
        output += "\nDeterminan sama dengan hasil perkalian dari elemen\npada diagonal utama matriks echelon di atas\n"
        output += "Determinan : {np.linalg.det(self.getData()).round(5)}\n"
        output += "-"*50 + "\n"
        isSave(output)
        
    def __determinant_and_echelon_form(self):
        echelon_matrix = self.getData().astype(float)
        num_rows, num_cols = echelon_matrix.shape
        pivot_row = 0

        # Iterasi tiap kolom
        for j in range(num_cols):
            non_zero_indices = np.nonzero(echelon_matrix[pivot_row:, j])[0]
            if non_zero_indices.size == 0:
                continue  # Geser ke elemen berikutnua
            pivot_row_index = pivot_row + non_zero_indices[0]

            # Swap baris sekarang dengan pivot
            echelon_matrix[[pivot_row, pivot_row_index]] = echelon_matrix[[pivot_row_index, pivot_row]]

            for i in range(num_rows):
                if i != pivot_row:
                    factor = echelon_matrix[i, j] / echelon_matrix[pivot_row, j]
                    echelon_matrix[i, :] -= factor * echelon_matrix[pivot_row, :]

            pivot_row += 1
            if pivot_row >= num_rows or pivot_row >= num_cols:
                break

        return (np.diag(echelon_matrix), echelon_matrix)
    
    def printGaussJordanDet(self):
        elemen_diagonal, echelon_form = self.__determinant_and_echelon_form()
        print("Matriks Echelon Tereduksi : ")
        print(tl.tabulate(echelon_form, tablefmt="fancy_grid"))
        print("\nDeterminan sama dengan hasil perkalian dari elemen\npada diagonal utama matriks echelon di atas")
        count = 0
        for i in elemen_diagonal:
            if count == len(elemen_diagonal) - 1:
                print(i.round(5), end='')
            else:
                print(f"{i.round(5)} * ", end="")
            count += 1
        print(f" = {np.prod(elemen_diagonal.round(5))}")
        print(f"\nDeterminan : {np.linalg.det(self.getData()).round(5)}")
        print("-"*50)
        
        output = ""
        output += "Invers matriks dengan eliminasi gauss jordan\n".upper()
        output += "-"*50 + "\n"
        output += "Matriks yang Anda inputkan : \n"
        output += tl.tabulate(self.getData(), tablefmt="fancy_grid")
        output += "\nMatriks Echelon Tereduksi : \n"
        output += tl.tabulate(echelon_form, tablefmt="fancy_grid")
        output += "\nDeterminan sama dengan hasil perkalian dari elemen\npada diagonal utama matriks echelon di atas\n"
        output += "Determinan : {np.linalg.det(self.getData()).round(5)}\n"
        output += "-"*50 + "\n"
        isSave(output)
        
    # Mencari determinan menggunakan invers matriks
    def __determinan_dari_invers_matriks(self, data:np.array) -> tuple:
        inv_matriks = np.linalg.inv(data)
        det = 1/(np.linalg.det(inv_matriks))
        return (inv_matriks, det)
    def printInversMatriksDet(self) -> float:
        inv_matriks, det = self.__determinan_dari_invers_matriks(self.getData()) 
        print("Matriks Awal (A) : ")
        print(tl.tabulate(self.getData(), tablefmt="fancy_grid"))
        print("Matriks Invers (inv(A)): ")
        print(tl.tabulate(inv_matriks, tablefmt="fancy_grid"))
        print(f"Determinan Matriks Invers di atas adalah {det}\n")
        print("Det(A) = 1/(Det(inv(A)))")
        print(f"Determinan Matriks A adalah {1/det}")
        print("-"*50)
        
        output = ""
        output += "Matriks Awal (A) : \n"
        output += tl.tabulate(self.getData(), tablefmt="fancy_grid")
        output += "\nMatriks Invers (inv(A)) : \n"
        output += tl.tabulate(inv_matriks, tablefmt="fancy_grid")
        output += f"\n\nDeterminan Matriks Invers di atas adalah {det}\n"
        output += "Det(A) = 1/(Det(inv(A)))\n"
        output += f"Determinan Matriks A adalah {1/det}\n"
        output += "-"*50 + "\n"
        isSave(output)
    
    # Invers matriks
    def invers(self):
        if(self.det() == 0):
            return "Matriks Singular"
        return np.linalg.inv(self.__data)

        # Mengunakan Gaussian untuk mencari inverse matriks
    def __gaussianInverse(self, matrix:np.array) -> tuple:
        matrix_join = np.hstack((matrix, np.eye(matrix.shape[0])))
        matriks = sp.Matrix(matrix_join)
        matriks_akhir = np.array(matriks.echelon_form()).astype(float).round(3)

        matriks_akhir2 = np.array(matriks.rref()[0]).astype(float).round(3)
        inverse_part = np.array(matriks_akhir2[:, matrix.shape[1]:]).astype(float)
        return (matriks_akhir, matriks_akhir2, inverse_part)
    
    # Mencetak gaussian untuk inverse matriks
    def printGaussianInverse(self):
        output = "" 
        output += "Matriks Invers dengan Metode Elimnasi Gausssian\n".upper()
        output += "-"*50 + "\n"
        if(self.det(self.getData() == 0)):
            print("Matriks Anda (A) : ")
            print(tl.tabulate(data, tablefmt="fancy_grid"))
            print("Determinan matriks : 0".upper())
            print("Matriks singular".upper())
            print("-"*50)
            
            output += "Matriks Anda (A) : \n"
            output += tl.tabulate(data, tablefmt="fancy_grid")
            output += "\nDeterminan matriks : 0\n".upper()
            output += "Matriks Singular\n".upper()
            output += "-"*50 + "\n"
        else :
            data = self.getData()
            echelon, rref, inv = self.__gaussianInverse(data)
            
            print("Matriks Anda (A) : ")
            print(tl.tabulate(data, tablefmt="fancy_grid"))
            print("Bentuk Echelon : ")
            print(tl.tabulate(echelon, tablefmt="fancy_grid"))
            print("Dilakukan OBE sedemikian sehingga diperoleh bentuk [I inv(A)]")
            
            output += "Matriks Anda (A) : \n"
            output += tl.tabulate(data, tablefmt="fancy_grid") + "\n"
            output += "Bentuk Echelon : \n"
            output += tl.tabulate(echelon, tablefmt="fancy_grid")
            output += "\nDilakukan OBE sedemikian sehingga diperoleh bentuk [I inv(A)]\n"
            
            output += self.__handlingGaussInv()
            output += "-"*50 + "\n"
        isSave(output)
        
    # Menggunakan Gauss Jordan untuk menemukan matriks invers
    def printGaussJordanInv(self):
        output = "" 
        output += "Matriks Invers dengan Metode Elimnasi Gauss Jordan\n".upper()
        output += "-"*50 + "\n"
        
        if(self.det(self.getData().round(3) == 0)):
            print("Matriks Anda (A) : ")
            print(tl.tabulate(data, tablefmt="fancy_grid"))
            print("Determinan matriks : 0".upper())
            print("Matriks singular".upper())
            print("-"*50)
            
            output += "Matriks Anda (A) : \n"
            output += tl.tabulate(data, tablefmt="fancy_grid")
            output += "\nDeterminan matriks : 0\n".upper()
            output += "Matriks Singular\n".upper()
            output += "-"*50 + "\n"
        else :
            data = self.getData()
            _, rref, inv = self.__gaussianInverse(data)
            
            print("Matriks Anda (A) : ")
            print(tl.tabulate(data, tablefmt="fancy_grid"))
            
            output += "Matriks Anda (A) : \n"
            output += tl.tabulate(data, tablefmt="fancy_grid") + "\n"
            output += self.__handlingGaussInv()
        isSave(output)
    
    # Fungsi bantuan untuk gaussjordan dan gaussian untuk invers matriks
    def __handlingGaussInv(self):
        _, rref, inv = self.__gaussianInverse(self.getData())
        output = ""
        
        print("Bentuk [I inv(A)] (Echelon Tereduksi) : ")
        print(tl.tabulate(rref, tablefmt="fancy_grid"))
        print("Invers dari A : ")
        print(tl.tabulate(inv, tablefmt="fancy_grid"))
        
        output += "Bentuk [I inv(A)] (Echelon Tereduksi) : \n"
        output += tl.tabulate(rref, tablefmt="fancy_grid")
        output += "\nInvers dari A : \n"
        output += tl.tabulate(inv, tablefmt="fancy_grid")
        
        # Validasi Output
        print("Validasi : ")
        isIdentity = np.dot(self.getData(), inv).round(1)
        if(np.all(np.abs(isIdentity) == np.eye(self.getData().shape[0]))):
            validasi = "BENAR"
        else:
            validasi = "SALAH"
        print(f"Apakah A * inv(A) = I ? : {validasi}")
        print("-"*50)
        
        output += "\nValidasi : ".upper()
        output += f"\nApakah A * inv(A) = I ? : {validasi}\n"
        return output
    
    # Mengambil adjoin suatu matriks
    def __take_adjoin(self, matrix:np.array) -> np.array:
        matriks = sp.Matrix(matrix)
        adj_matriks = matriks.adjugate()
    
        return np.array(adj_matriks)
    
    # Mengambil invers dari balikan invers
    def printInverseMatrix(self):
        data = self.getData()
        output = ""
        output += "Matriks Invers menggunakan metode balikan matriks\n".upper()
        output += "-"*50 + "\n"
        
        if(self.det(data).round(3) == 0):
            print("Matriks Anda (A) : ")
            print(tl.tabulate(data, tablefmt="fancy_grid"))
            print("Determinan matriks : 0".upper())
            print("Matriks singular".upper())
            print("-"*50)
            
            output += "Matriks Anda (A) : \n"
            output += tl.tabulate(data, tablefmt="fancy_grid")
            output += "\nDeterminan matriks : 0".upper()
            output += "\nMatriks singular".upper()
            output += "-"*50 + "\n"
            
        else:
            adj = self.__take_adjoin(data)
            inv = np.linalg.inv(data)
            print("Matriks A : ")
            print(tl.tabulate(data, tablefmt='fancy_grid'))
            print(f"Determinan dari A (det(A)): {self.det(data)}")
            print("Adjoin dari A (adj(A)) : ")
            print(tl.tabulate(adj, tablefmt='fancy_grid'))
            print("Invers Matriks = (1/det(A)) * adj(A)")
            print("Invers Matriks : ")
            print(tl.tabulate(inv, tablefmt='fancy_grid'))
            
            output += "Matriks A : \n"
            output += tl.tabulate(data, tablefmt='fancy_grid')
            output += f"\nDeterminan dari A (det(A)): {self.det(data)}"
            output += "\nAdjoin dari A (adj(A)) : \n"
            output += tl.tabulate(adj, tablefmt='fancy_grid')
            output += "\nInvers Matriks = (1/det(A)) * adj(A)"
            output += "\nInvers Matriks : \n"
            output += tl.tabulate(inv, tablefmt='fancy_grid')
            
            # Validasi Output
            print("Validasi : ")
            isIdentity = np.dot(self.getData(), inv).round(1)
            if(np.all(np.abs(isIdentity) == np.eye(self.getData().shape[0]))):
                validasi = "BENAR"
            else:
                validasi = "SALAH"
            print(f"Apakah A * inv(A) = I ? : {validasi}")
            print("-"*50)
            output += "\nValidasi : ".upper()
            output += f"\nApakah A * inv(A) = I ? : {validasi}\n"
            output += "-"*50 + "\n"
            isSave(output)
        
    # Eigen Value, Eigen Vektor, dan persamaan karakteristik polinomial
    def __eigen(self, data:np.array) -> tuple:
        eig_val, eig_vec = np.linalg.eig(data)
        x = sp.symbols('x')
        data = sp.Matrix(data)
        char_pol = data.charpoly(x)
        roots_char_pol = sp.roots(char_pol)
        return (char_pol, roots_char_pol, eig_val, eig_vec)
    def printEigen(self):
        char_pol, roots_char_pol, eig_val, eig_vec = self.__eigen(self.getData())
        print("Matriks Anda (A) : ")
        print(tl.tabulate(self.getData(), tablefmt="fancy_grid"))
        print(f"\nPersamaan Polinomial Karakteristik : ")
        print(sp.pretty(char_pol))
        print(f"\nAkar-Akar Polinomial Karakteristik : ")
        print(roots_char_pol)
        print(f"\nEigen Value : ")
        count = 1
        for val in eig_val:
            print(f"{count}. {val.round(5)}")
            count += 1
        print(f"\nEigen Vektor : ")
        print(tl.tabulate(eig_vec, tablefmt="fancy_grid"))
        
        toleransi = 1e-10
        if(math.fabs(np.linalg.det(eig_vec)) < toleransi):
            print(f"Determinan matriks eigen vektor : 0".upper())
            print("Terdapat Eigen Vektor yang Tidak Bebas Linear".upper())
            print("Matriks yang Anda inputkan tidak memiliki diagonalisasi".upper())
        else:
            print(f"Determinan matriks eigen vektor : {np.linalg.det(eig_vec).round(5)}".upper())
            print("Matriks yang Anda inputkan memiliki diagonalisasi".upper())
        print("-"*50)
        
        output = ""
        output += "eigen value, eigen vektor dan polinomial karakteristiknya\n".upper()
        output += "-"*50
        output += "\nMatriks yang Anda berikan : \n"
        output += tl.tabulate(self.getData(), tablefmt="fancy_grid")
        output += "\n\nPersamaan Polinomial Karakteristik : \n"
        output += sp.pretty(char_pol)
        output += "\n\nAkar-Akar Polinomial Karakteristik : \n"
        output += f"{roots_char_pol}"
        output += "\n\nEigen Value : \n"
        count = 1
        for val in eig_val:
            output += f"{count}. {val.round(5)}\n"
            count += 1
        output += "\nEigen Vektor : \n"
        output += tl.tabulate(eig_vec, tablefmt="fancy_grid")
        toleransi = 1e-10
        if(math.fabs(np.linalg.det(eig_vec)) < toleransi):
            output += f"Determinan matriks eigen vektor : 0\n".upper()
            output += "Terdapat Eigen Vektor yang Tidak Bebas Linear\n".upper()
            output += "Matriks yang Anda inputkan tidak memiliki diagonalisasi\n".upper()
        else:
            output += f"\n\nDeterminan matriks eigen vektor : {np.linalg.det(eig_vec).round(5)}\n".upper()
            output += "Matriks yang Anda inputkan memiliki diagonalisasi".upper()
        isSave(output)
            
    # Diagonalization
    def __diagonalization(self, data: np.array) -> tuple:
        data = sp.Matrix(data)
        P, D = data.diagonalize()
        P = np.array(P).astype(float)
        D = np.array(D).astype(float)
        return (P, D)
    
    def printDiagonalization(self):
        P, D = np.array(self.__diagonalization(self.getData()))
        eig_val, eig_vec = np.linalg.eig(self.getData())
        toleransi = 1e-10
        if(math.fabs(np.linalg.det(eig_vec)) < toleransi):
            print("Matriks : ")
            print(tl.tabulate(self.getData(),  tablefmt="fancy_grid"))
            print("Matriks tidak memiliki diagonalisasi".upper())
            print(f"karena tidak memiliki {self.getData().shape[0]} eigen vektor yang bebas linier\n".upper())
        else:
            print(f"\nMatriks A  : ")
            print(tl.tabulate(self.getData(), tablefmt="fancy_grid"))
            print(f"\nMatriks P  : ")
            print(tl.tabulate(P, tablefmt="fancy_grid"))
            print(f"\nMatriks D  : ")
            print(tl.tabulate(D, tablefmt="fancy_grid"))
            
            tambahan = "(INVERTIBLE)" if(np.linalg.det(P) != 0) else "(NOT INVERTIBLE)"
            print(f"\nDeterminan P : {np.linalg.det(P).round(3)} {tambahan}")
            
            print("\nValidasi : ")
            product = np.dot(np.dot(np.linalg.inv(P), self.getData()), P)
            toleransi = 1e-8
            if(np.all(np.abs(product - D)) < toleransi):
                additon = "BENAR"
            else:
                additon = "SALAH"
            print(f"APAKAH D = inv(P) x A x P ? : {additon}")
        print("-"*50)
        
        # Handling save output ke .txt
        output = ""
        output += "diagonalisasi matriks\n".upper()
        output += "-"*50
        output += f"\nOrdo Matriks Persegi : {self.getData().shape[0]}\n"
        output += "Matriks yang Anda inputkan (A) : \n"
        output += tl.tabulate(self.getData(), tablefmt="fancy_grid")
        output += "\nMatriks P : \n"
        output += tl.tabulate(P, tablefmt="fancy_grid")
        output += "\nMatriks D : \n"
        output += tl.tabulate(D, tablefmt="fancy_grid")
        output += f"\nDeterminan P : {tambahan}\n"
        output += "Validasi : \n"
        output += f"Apakah D = inv(P) x A x P ? : {additon}"
        isSave(output)
        
    # Singular Value Decomposition
    def __svd(self, data:np.array) -> tuple:
        U, S, VT = np.linalg.svd(data, full_matrices=False)
        return (U, np.diag(S), VT)
    def printSVD(self):
        U, S, VT = self.__svd(self.getData())
        print(f"\nMatriks U : ")
        print(tl.tabulate(U, tablefmt="fancy_grid"))
        print(f"\nMatriks Sigma : ")
        print(tl.tabulate(S, tablefmt="fancy_grid"))
        print(f"\nMatriks V (V belum ditranspose) : ")
        print(tl.tabulate(VT.T, tablefmt="fancy_grid"))
        
        print("Validasi : ".upper())
        product = np.dot(np.dot(U, S), VT)
        toleransi = 1e-8
        if np.all(np.abs(product - self.getData()) < toleransi):
            tambahan = "BENAR"
        else:
            tambahan = "SALAH"
        print(f"Apakah U x Sigma x V.T = A ? : {tambahan}")
        print("-"*50)
    
        # Mengatasi untuk simpan output
        output = ""
        output += "SINGULAR VALUE DECOMPOSITION (SVD)\n"
        output += "-"*50
        output += "\nOrdo Matriks\n"
        output += f"Banyak Baris : {self.getData().shape[0]}\n"
        output += f"Banyak Kolom : {self.getData().shape[1]}\n"
        output += "-"*50
        output += f"\nMatriks yang Anda inputkan : \n"
        output += tl.tabulate(self.getData(), tablefmt="fancy_grid")
        output += "\n"
        output += "-"*50
        output += "\nMatriks U                       :\n"
        output += tl.tabulate(U, tablefmt="fancy_grid")
        output += "\nMatriks Sigma                    :\n"
        output += tl.tabulate(S, tablefmt="fancy_grid")
        output += "\nMatriks V (belum ditranspose)    :\n"
        output += tl.tabulate(VT, tablefmt="fancy_grid")
        output += "\nValidasi      : \n"
        output += f"Apakah U x Sigma x V.T = A ? : {tambahan}"
        isSave(output)
        
    # Transpose matriks
    def __transpose(self):
        return self.getData().T
    
    def printTranspose(self):
        data = self.getData()
        print("Matriks Awal (A) : ")
        print(tl.tabulate(data, tablefmt="fancy_grid"))
        print("Matriks Transpose (A.T) : ")
        print(tl.tabulate(self.__transpose(), tablefmt="fancy_grid"))
        print("-"*50)
        
        output = ""
        output += "transpose matriks\n".upper()
        output += "-"*50 + "\n"
        output += "Matriks yang Anda inputkan (A) : \n"
        output += tl.tabulate(data, tablefmt="fancy_grid")
        output += "\nMatriks Transpose (A.T) : \n"
        output += tl.tabulate(self.__transpose(), tablefmt="fancy_grid")
        output += "-"*50 + "\n"
        isSave(output)
        
    # Input untuk Perkalian matriks
    def __inputDot(self):
        baris1 = int(input("Masukkan Banyak Baris Matriks 1 : "))
        kolom1 = int(input("Masukkan Banyak Kolom Matriks 1 : "))
        print("-"*50)
        baris2 = int(input("Masukkan Banyak Baris Matriks 2 : "))
        kolom2 = int(input("Masukkan Banyak Kolom Matriks 2 : "))
        print("-"*50)
        
        if(baris1 > 0 and kolom1 > 0 and baris2 > 0 and kolom2 > 0):
            if(kolom1 == baris2):
                # Input untuk matriks pertama
                print("\nMatriks Pertama")
                print(f"Masukkan {kolom1} Elemen Setiap Baris")
                print("-"*50)
                matriks1 = []
                for i in range(baris1):
                    userInput = input(f"Baris ke-{i+1} : ").split()
                    numberInput = [float(num) for num in userInput]
                    matriks1.append(numberInput)
                print("-"*50)
                
                # Input untuk matriks kedua
                print("\nMatriks Kedua")
                print(f"Masukkan {kolom2} Elemen Setiap Baris")
                print("-"*50)
                matriks2 = []
                for i in range(baris2):
                    userInput = input(f"Baris ke-{i+1} : ").split()
                    numberInput = [float(num) for num in userInput]
                    matriks2.append(numberInput)
                print("-"*50)
                
                return (matriks1, matriks2)
            else:
                print("Masuka Anda Salah, Matriks 1 dan Matriks 2 Tidak Dapat Dikalikan")
    
    # Perkalian Matriks
    def __dot(self):
        matriks1, matriks2 = np.array(self.__inputDot())
        return np.dot(matriks1, matriks2)
    
    # Mencetak output perkalian matriks
    def printDot(self):
        matriks1, matriks2 = self.__inputDot()
        matriks1 = np.array(matriks1)
        matriks2 = np.array(matriks2)
        print("Matriks Pertama (A)  : ")
        print(tl.tabulate(matriks1, tablefmt="fancy_grid"))
        print("Matriks Kedua (B)    : ")
        print(tl.tabulate(matriks2, tablefmt="fancy_grid"))
        
        print("Hasil A x B : ")
        print(tl.tabulate(np.dot(matriks1, matriks2), tablefmt="fancy_grid"))
        print("-"*50)
        
        output = ""
        output += "Matriks Pertama (A) : \n"
        output += tl.tabulate(matriks1, tablefmt="fancy_grid") + "\n"
        output += "Matriks Kedua (B) : \n"
        output += tl.tabulate(matriks2, tablefmt="fancy_grid") + "\n"
        output += "Matriks A x B : \n"
        output += tl.tabulate(np.dot(matriks1, matriks2), tablefmt="fancy_grid") + "\n"
        output += "-"*50 + "\n"
        isSave(output)
    
    # masukan untuk penjumlahan dan pengurangan matriks
    def __inputAddSubtract(self):
        print("Masukkan Ordo Matriks")
        baris = int(input("Banyaknya Baris : "))
        kolom = int(input("Banyaknya Kolom : "))
        print("-"*50)
        
        try:
            if(baris > 0 and kolom > 0):
                print("Masukkan Elemen Matriks Pertama")
                print(f"Masukkan {kolom} Elemen Setiap Baris")
                print("-"*50)
                matriks1 = []
                for i in range(baris):
                    userInput = input(f"Baris ke-{i+1} : ").split()
                    numberInput = [float(num) for num in userInput]
                    matriks1.append(numberInput)
                print("-"*50)
                
                print("Masukkan Elemen Matriks Kedua")
                print(f"Masukkan {kolom} Elemen Setiap Baris")
                print("-"*50)
                matriks2 = []
                for i in range(baris):
                    userInput = input(f"Baris ke-{i+1} : ").split()
                    numberInput = [float(num) for num in userInput]
                    matriks2.append(numberInput)
                print("-"*50)
                
                # Mengecek apakah matriks1 yang diberikan sesuai ordo atau tidak
                if(len(matriks1) == baris and len(matriks1[0]) == kolom and len(matriks2) == baris and len(matriks2[0]) == kolom):
                    matriks1 = np.array(matriks1)    
                    matriks2 = np.array(matriks2)
                    return (matriks1, matriks2)
                   
                else:
                    print("Matriks yang Anda masukkan tidak sesuai dengan ordo yang Anda masukkan")
            else:
                print("Ordo Matriks Salah!")   
        except ValueError:
            print("Masukan Anda Salah!")
    
    # Mencetak pengurangan dan penjumlahan matriks
    def printAddSubtract(self):
        matriks1, matriks2 = self.__inputAddSubtract()
        
        print("Matriks Pertama (A)  : ")
        print(tl.tabulate(matriks1, tablefmt="fancy_grid"))
        print("Matriks Kedua (B)    : ")
        print(tl.tabulate(matriks2, tablefmt="fancy_grid"))
        print("Matriks A + B        : ")
        print(tl.tabulate(matriks1 + matriks2, tablefmt="fancy_grid"))
        print("Matriks A - B        : ")
        print(tl.tabulate(matriks1 - matriks2, tablefmt="fancy_grid"))
        print("-"*50)
        
        output  = "Matriks Pertama (A)  : \n"
        output += tl.tabulate(matriks1, tablefmt="fancy_grid") + "\n"
        output += "Matriks Kedua (B)    : \n"
        output += tl.tabulate(matriks2, tablefmt="fancy_grid") + "\n"
        output += "Matriks A + B        : \n"
        output += tl.tabulate(matriks1 + matriks2, tablefmt="fancy_grid") + "\n"
        output += "Matriks A - B        : \n"
        output += tl.tabulate(matriks1 - matriks2, tablefmt="fancy_grid") + "\n"
        output += "-"*50 + "\n"
        isSave(output)