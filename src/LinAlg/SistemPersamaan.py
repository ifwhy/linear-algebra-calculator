import numpy as np
import sympy as sp
import tabulate as tl
from .Menu import isSave

class SistemPersamaan:
    # Attribut : __data (np.array), __const (np.array), __isReal (bool)
    
    # Konstruktor
    def __init__(self, matrix1:list, matrix2:list):
        self.__data = np.array(matrix1)
        self.__const = np.array(matrix2)
    
    # Getter untuk __data
    def getData(self):
        return self.__data.astype(float) if self.__isReal else self.__data.astype(complex)
    
    # Getter untuk __const
    def getConst(self):
        return self.__const if self.__isReal else self.__const.astype(complex)
    
    def __joinRight(self):
        return np.hstack((self.getData(), self.getConst()))
    
    # Mengambil input dari user
    def takeInput(self):
        var = int(input("Banyak Variabel\t\t\t\t: "))
        eq = int(input("Banyak Persamaan\t\t\t: "))
        complexNum = str(input("Apakah terdapat bil. compleks (y/n)\t: ".capitalize()))
        print("-"*50)
        
        A = []
        B = []
        print("Masukkan Koefisien dan pisahkan dengan spasi".capitalize())
        print("Konstanta ada di sebelah kanan tanda sama dengan".capitalize())
        print("Untuk bagian bilangan imaginer, gunakan j".capitalize())
            
        isReal = False if complexNum == 'y' or complexNum == 'Y' else True
        self.__isReal = isReal
        if(isReal):
            print("-"*50)
            print("\t\t   Bilangan Real")
            print("-"*50)
            for i in range(eq):
                matriks_A = input(f"Persamaan ke-{i+1}\t: ").split()
                matriks_B = input(f"Konstanta ke-{i+1}\t: ")
                print()
                matriks_A = [float(num) for num in matriks_A]
                matriks_B = [matriks_B]
                A.append(matriks_A)
                B.append(matriks_B)
                for i in A:
                    if len(i) != var:
                        print("Masukan Anda Salah!")
            else:
                A = np.array(A)
                B = np.array(B)
                self.__data = A
                self.__const = B
            print("-"*50)
        
        # Dengan Bilangan Kompleks
        else:
            print("-" * 50)
            print("\t\t Bilangan Kompleks")
            print("-" * 50)

            A = []
            B = []

            for i in range(eq):
                matriks_A_str = input(f"Persamaan ke-{i+1}\t: ").split()
                matriks_B_str = input(f"Konstanta ke-{i+1}\t: ")
                print()
                # Convert input strings to complex numbers
                matriks_A = [complex(row) for row in matriks_A_str]
                matriks_B = complex(matriks_B_str)
                
                # Append to lists
                A.append(matriks_A)
                B.append([matriks_B])
                
                for row in A:
                    if len(row) != var:
                        print("Masukan Anda Salah!")
                        break
            else:
                # Convert lists to numpy arrays
                A = np.array(A).astype(complex)
                B = np.array(B).astype(complex)
                
                self.__data = A
                self.__const = B
    
    # Membuat variabel sebanyak var
    def __create_var(self) -> sp.Matrix:
        variables = []
        
        for i in range(self.__data.shape[1]):
            variables.append(f"x{i+1}")
        
        var_arr = np.array(variables).reshape(-1, 1)
        return sp.Matrix(var_arr)
        
    # Menyelesaikan SPL dengan metode Balikan Matriks
    def __solvingSPL(self):
        if(self.__isReal):
            A = self.getData().astype(float)
            aug = self.__joinRight().astype(float)
            rank_A = np.linalg.matrix_rank(A)
            rank_aug = np.linalg.matrix_rank(aug)
        else :
            A = self.getData().astype(complex)
            aug = self.__joinRight().astype(complex)
            rank_A = np.linalg.matrix_rank(A)
            rank_aug = np.linalg.matrix_rank(aug)
        if rank_A == rank_aug == A.shape[1]:
            return "Tunggal".capitalize()
        elif rank_A == rank_aug and rank_A < A.shape[1]:
            return "Banyak".capitalize()
        elif rank_A < rank_aug:
            return "Tidak Ada".capitalize()
    
    def printSolvingInv(self) :
        solusi = self.__solvingSPL()
        output = "Sistem Persamaan Linear dengan Metode balikan matriks\n".upper()
        output += "-"*50 + "\n"
        
        if(self.__isReal):
            A = self.getData().astype(float)
            B = self.getConst().astype(float)
            var = self.__create_var()
            # Menampilkan matrix Koefisien
            print("Matriks Koefisien (Coef) : ")
            print(tl.tabulate(A, tablefmt="fancy_grid"))
            
            output += "Matriks Koefisien (Coef) : \n"
            output += tl.tabulate(A, tablefmt="fancy_grid") + "\n"
            
            if(A.shape[1] == A.shape[0]):
                print(f"\nDeterminan A : {np.linalg.det(A).round(5)}")
                output += f"Determinan A : {np.linalg.det(A).round(5)}\n"
                if(np.linalg.det(A) == 0):
                    print("Matriks A adalah Matriks Singular")
                    print(f"\nSOLUSI : {solusi}")
                    A = sp.Matrix(A)
                    var = sp.Matrix(var)
                    B = sp.Matrix(B)
                    eq = sp.Eq(A * var, B)
                    solution = sp.solve(eq)
                    
                    output += "Matriks A adalah Matriks Singular\n"
                    output += f"SOLUSI : {solusi}\n"
                    
                    if len(solution) != 0:
                        rows = []
                        for key, values in solution.items():
                            rows.append([key] + [values])

                        baris = []
                        for row in rows:
                            dummy = [f"{row[0]} = {row[1]}"]
                            baris.append(dummy)
                        print(tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid")) 
                        
                        output += tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid") + "\n"
                        
                else :
                    print("Invers Matriks Koefisien inv(Coef) : ")
                    print(tl.tabulate(np.linalg.inv(A), tablefmt="fancy_grid"))
                    # Menampilkan matrix Konstanta
                    print("Matriks Konstanta (Const) : ")
                    print(tl.tabulate(B, tablefmt="fancy_grid"))
                    
                    # Menampilkan solusi
                    print("Perkalian inv(Coef) dengan (Const) adalah solusi SPL")
                    print(f"\nSOLUSI : {solusi}")
                    
                    output += "Invers Matriks Koefisien inv(Coef) : \n"
                    output += tl.tabulate(np.linalg.inv(A), tablefmt="fancy_grid") + "\n"
                    output += "Matriks Konstanta (Const) : \n"
                    output += tl.tabulate(B, tablefmt="fancy_grid")
                    
                    output += "\nPerkalian inv(Coef) dengan (Const) adalah solusi SPL\n"
                    output += f"SOLUSI : {solusi}\n"
                    
                    if(solusi == "Tunggal"):
                        solution = np.dot(np.linalg.inv(A), B)
                        var = self.__create_var()
                        
                        lastSol = []
                        for i in range(len(solution)):
                            sol = [f"{var[i]} = {solution[i]}"]
                            lastSol.append(sol)
                        
                        print(tl.tabulate(lastSol, tablefmt="fancy_grid"))
                        output += tl.tabulate(lastSol, tablefmt="fancy_grid") + "\n"
                        
                    elif(solusi == "Banyak"):
                        A = sp.Matrix(A)
                        var = sp.Matrix(var)
                        B = sp.Matrix(B)
                        eq = sp.Eq(A * var, B)
                        solution = sp.solve(eq)
                        
                        if len(solution) != 0:
                            rows = []
                            for key, values in solution.items():
                                rows.append([key] + [values])
                            
                            # Mencetak Tabel
                            baris = []
                            for row in rows:
                                dummy = [f"{row[0]} = {row[1]}"]
                                baris.append(dummy)
                            print(tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid")) 
                            
                            output += tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid") + "\n"
            else :
                print("\nMatriks yang Anda berikan bukan matriks persegi".upper())
                print("Tidak dapat diselesaikan menggunakan metode invers".upper())
                
                output += "Matriks yang Anda berikan bukan matriks persegi\n".upper()
                output += "Tidak dapat diselesaikan menggunkan metode invers".upper()
                
            print("-"*50)
            output += "-"*50 + "\n"
        
        # Handling bilangan kompleks
        else:
            A = self.getData().astype(complex)
            B = self.getConst().astype(complex)
            var = self.__create_var()
            
            # Casting ke string agar bisa ditampilkan tabulate
            A = [[str(num) for num in row] for row in A]
            B = [[str(num) for num in row] for row in B]
            
            print("Matriks Koefisien (Coef) : ")
            print(tl.tabulate(A, tablefmt="fancy_grid"))
            
            output += "Matriks Koefisien (Coef) : \n"
            output += tl.tabulate(A, tablefmt="fancy_grid") + "\n"
            
            # Casting ke complex untuk perhitung numpy/sympy
            A = np.array(A).astype(complex)
            B = np.array(B).astype(complex)
            
            if(A.shape[1] == A.shape[0]):
                print(f"\nDeterminan A : {np.linalg.det(A).round(5)}")
                output += f"Determinai A : {np.linalg.det(A).round(5)}\n"
                
                if(np.linalg.det(A) == 0):
                    print("Matriks A adalah Matriks Singular")
                    print(f"\nSOLUSI : {solusi}")
                    
                    output += "Matriks A adalah Matriks Singular\n"
                    output += f"SOLUSI : {solusi}\n"
                    
                    A = sp.Matrix(A)
                    var = sp.Matrix(var)
                    B = sp.Matrix(B)
                    eq = sp.Eq(A * var, B)
                    solution = sp.solve(eq)
                    
                    # Memastikan Ada solusi
                    if len(solution) != 0:
                        rows = []
                        for key, values in solution.items():
                            rows.append([key] + [values])
                        baris = []
                        for row in rows:
                            dummy = [f"{row[0]} = {row[1]}"]
                            baris.append(dummy)
                        print(tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid")) 
                        output += tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid") + "\n"
                else :
                    inv = np.linalg.inv(A).round(5)
                    invStr = [[str(num) for num in row] for row in inv]
                    
                    print("Invers Matriks Koefisien inv(Coef) : ")
                    print(tl.tabulate(invStr, tablefmt="fancy_grid"))
                    
                    output += "Invers Matriks Koefisien inv(Coef) : \n"
                    output += tl.tabulate(invStr, tablefmt="fancy_grid") + "\n"
                    
                    # Casting ke string agar bisa ditampilkan tabulate
                    A = [[str(num) for num in row] for row in A]
                    B = [[str(num) for num in row] for row in B]
                    
                    # Menampilkan matrix Konstanta
                    print("Matriks Konstanta (Const) : ")
                    print(tl.tabulate(B, tablefmt="fancy_grid"))
                    
                    output += "Matriks Konstanta (Const) \n"
                    output += tl.tabulate(B, tablefmt="fancy_grid") + "\n"
                    
                    # Menampilkan solusi
                    print("Perkalian inv(Coef) dengan (Const) adalah solusi SPL")
                    print(f"\nSOLUSI : {solusi}")
                    
                    output += "Perkalian inv(Coef) dengan (Const) adalah solusi SPL\n"
                    output += f"SOLUSI : {solusi}\n"
                    
                    # Casting ke complex untuk perhitung numpy/sympy
                    A = np.array(A).astype(complex)
                    B = np.array(B).astype(complex)
                    
                    if(solusi != "Tidak Ada"):
                        solution = np.dot(np.linalg.inv(A), B).round(5)
                        solutionStr = [[str(num) for num in row] for row in np.hstack((var, solution))]
                        
                        lastSol = []
                        for i in range(len(solutionStr)):
                            sol = [f"{solutionStr[i][0]} = {solutionStr[i][1]}"]
                            lastSol.append(sol)                
                        
                        print(tl.tabulate(lastSol, tablefmt="fancy_grid"))
                        output += tl.tabulate(lastSol, tablefmt="fancy_grid") + "\n"
                        
                    elif(solusi == "Banyak"):
                        A = sp.Matrix(A)
                        var = sp.Matrix(var)
                        B = sp.Matrix(B)
                        eq = sp.Eq(A * var, B)
                        solution = sp.solve(eq)
                        if len(solution) != 0:
                            rows = []
                            for key, values in solution.items():
                                rows.append([key] + [values])

                            # Mencetak Tabel
                            baris = []
                            for row in rows:
                                dummy = [f"{row[0]} = {row[1]}"]
                                baris.append(dummy)
                            print(tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid")) 
                            output += tl.tabulate(baris, tablefmt="fancy_grid") + "\n"
                            
            else :
                print("\nMatriks yang Anda berikan bukan matriks persegi".upper())
                print("Tidak dapat diselesaikan menggunakan metode invers".upper())
                
                output += "Matriks yang Anda berikan bukan matriks persegi\n".upper()
                output += "Tidak dapat diselesaikan menggunakan metode invers\n".upper()
            output += "-"*50 + "\n"
            print("-"*50)
        isSave(output)
    
    # Metode Gaussian Elimination
    def __gaussianElimination(self) -> np.array:
        data = self.__joinRight()
        data = sp.Matrix(data)
        return np.array(data.echelon_form())
    
    def printGaussianElimination(self):
        aug = self.__joinRight()
        echelon = self.__gaussianElimination()
        solusi = self.__solvingSPL()
        
        output = "Sistem persamaan linear dengan gaussian elimination\n".upper()
        output += "-"*50 + "\n"
        
        aug = [[str(num) for num in row] for row in aug] if(self.__isReal == False) else aug
        echelon = [[str(num) for num in row] for row in echelon] if(self.__isReal == False) else echelon
        
        print("Matriks Augmented \t: ")
        print(tl.tabulate(aug, tablefmt="fancy_grid"))
        print("Matriks Bentuk Echelon \t: ")
        print(tl.tabulate(echelon, tablefmt="fancy_grid"))
        print(f"Solusi \t\t\t: {solusi}")
        
        output += "Matriks Augmented \t: \n"
        output += tl.tabulate(aug, tablefmt="fancy_grid") + "\n"
        output += "Matriks Bentuk Echelon \t: \n"
        output += tl.tabulate(echelon, tablefmt="fancy_grid") + "\n"
        output += f"Solusi \t\t\t: {solusi}\n" 
        
        aug = self.__joinRight()
        echelon = self.__gaussianElimination()
        
        # Iterasi untuk mendapatkan persamaan dari echelon_form
        equations = []
        for row in echelon:
            if np.count_nonzero(row[:-1]) == 0:
                continue  # Melakukan skip jika 0 semua di satu baris
            lhs = []
            for i, coeff in enumerate(row[:-1]):
                if coeff != 0:
                    lhs.append(coeff.round(5) * sp.symbols(f'x{i+1}'))
            rhs = row[-1]
            equations.append((sum(lhs), sp.simplify(rhs)))
        
        if(solusi == "Tunggal"):
            print("Diperoleh Persamaan \t: ")
            output += "Diperoleh Persamaan \t: \n"
            linEq = []
            equations = equations[::-1]
            for eq in equations:
                eq = np.array([eq[0], eq[1]])
                eq = [f"{eq[0]} = {eq[1].round(5)}"]
                linEq.append(eq)
            print(tl.tabulate(linEq, tablefmt="fancy_grid", numalign="right"))
            output += tl.tabulate(linEq, tablefmt="fancy_grid", numalign="right") + "\n"
            
            print("Solve persamaaan pertama dan substitusikan ke persamaan berikunya")
            output += "Solve persamaaan pertama dan substitusikan ke persamaan berikunya\n"
            
            print("Diperoleh Solusi SPL \t: ")
            output += "Diperoleh Solusi SPl \t: \n"
            var = sp.Matrix(self.__create_var())
            A = sp.Matrix(self.getData())
            B = sp.Matrix(self.getConst())
            
            eq = sp.Eq(A * var, B)
            solution = sp.solve(eq)
                    
            if len(solution) != 0:
                rows = []
                for key, values in solution.items():
                    rows.append([key] + [values.round(5)])

            baris = []
            for row in rows:
                dummy = [f"{row[0]} = {row[1]}"]
                baris.append(dummy)
            print(tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid")) 
            output += tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid") + "\n"
            
        elif (solusi == "Banyak"):
            A = sp.Matrix(self.getData())
            var = sp.Matrix(self.__create_var())
            B = sp.Matrix(self.getConst())
            eq = sp.Eq(A * var, B)
            solution = sp.solve(eq)
            
            print("Diperoleh Persamaan \t: ")
            output += "Diperoleh Persamaan \t: \n"
            linEq = []
            equations = equations[::-1]
            for eq in equations:
                eq = [f"{eq[0]} = {eq[1]}"]
                linEq.append(eq)
            print(tl.tabulate(linEq, tablefmt="fancy_grid", numalign="right"))
            output += tl.tabulate(linEq, tablefmt="fancy_grid", numalign="right") + "\n"
            
            if len(solution) != 0:
                rows = []
                for key, values in solution.items():
                    rows.append([key] + [values])
                            
                # Mencetak Tabel
                baris = []
                for row in rows:
                    dummy = [f"{row[0]} = {row[1]}"]
                    baris.append(dummy)
                print("Diperoleh Solusi SPL \t: ")
                print(tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid"))
                output += tl.tabulate(baris, tablefmt="fancy_grid", numalign="right") + "\n"

        print("-"*50)
        output += "-"*50 + "\n"
        isSave(output)
    
    # Metode Gauss Jordan
    def __gaussJordan(self) -> np.array:
        data = self.__joinRight()
        data = sp.Matrix(data)
        return np.array(data.rref()[0])
    
    def printGaussJordan(self):
        aug = self.__joinRight() if self.__isReal else self.__joinRight().astype(complex)
        rref = self.__gaussJordan() if self.__isReal else self.__gaussJordan().astype(complex)
        solusi = self.__solvingSPL() if self.__isReal else self.__solvingSPL()
        
        aug = [[str(num) for num in row] for row in aug] if(self.__isReal == False) else aug
        rref = [[str(num) for num in row] for row in rref] if(self.__isReal == False) else rref
        
        output = "Sistem Persamaan Linear dengan Metode Gauss Jordan\n".upper()
        output += "-"*50 + "\n"
        
        print("Matriks Augmented \t: ")
        print(tl.tabulate(aug, tablefmt="fancy_grid"))
        print("Echelon Tereduksi \t: ")
        print(tl.tabulate(rref, tablefmt="fancy_grid"))
        print(f"Solusi \t\t\t: {solusi}")
        
        output += "Matriks Augmented \t: \n"
        output += tl.tabulate(aug, tablefmt="fancy_grid") + "\n"
        output += "Echelon Tereduksi \t: \n"
        output += tl.tabulate(rref, tablefmt="fancy_grid") + "\n"
        output += f"Solusi \t\t\t: {solusi}\n"
        
        aug = self.__joinRight()
        rref = self.__gaussJordan()
        
        # Iterasi untuk mendapatkan persamaan dari rref
        equations = []
        for row in rref:
            if np.count_nonzero(row[:-1]) == 0:
                continue  # Melakukan skip jika 0 semua di satu baris
            lhs = []
            for i, coeff in enumerate(row[:-1]):
                if coeff != 0:
                    lhs.append(coeff.round(5) * sp.symbols(f'x{i+1}'))
            rhs = row[-1]
            equations.append((sum(lhs), sp.simplify(rhs)))
        
        if(solusi == "Tunggal"):
            print("Diperoleh Solusi \t: ")
            output += "Diperoleh Solusi \t: \n"
            linEq = []
            # equations = equations[::-1]
            for eq in equations:
                eq = [f"{eq[0]} = {eq[1].round(5)}"]
                linEq.append(eq)
            print(tl.tabulate(linEq, tablefmt="fancy_grid", numalign="right"))
            output += tl.tabulate(linEq, tablefmt="fancy_grid", numalign="right") + "\n"
        
        elif (solusi == "Banyak"):
            A = sp.Matrix(self.getData())
            var = sp.Matrix(self.__create_var())
            B = sp.Matrix(self.getConst())
            eq = sp.Eq(A * var, B)
            solution = sp.solve(eq)
            
            linEq = []
            equations = equations[::-1]
            for eq in equations:
                eq = [f"{eq[0]} = {eq[1]}"]
                linEq.append(eq)
            print(tl.tabulate(linEq, tablefmt="fancy_grid", numalign="right"))
            output += tl.tabulate(linEq, tablefmt="fancy_grid", numalign="right") + "\n"
            
            if len(solution) != 0:
                rows = []
                for key, values in solution.items():
                    rows.append([key] + [values])
                            
                # Mencetak Tabel
                baris = []
                for row in rows:
                    dummy = [f"{row[0]} = {row[1]}"]
                    baris.append(dummy)
                print("Diperoleh Solusi SPL \t: ")
                print(tl.tabulate(baris, headers="firstrow", tablefmt="fancy_grid"))
                output += tl.tabulate(baris, tablefmt="fancy_grid", numalign="right") + "\n"
            
        print("-"*50)  
        output += "-"*50 + "\n"
        isSave(output)