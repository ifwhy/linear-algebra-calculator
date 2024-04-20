import LinAlg as la
from colorama import Fore, Style 

menu = la.Menu()
matriks = la.Matriks([])
spl = la.SistemPersamaan([], [])

if __name__ == "__main__":
    la.clear_console()
    while(menu.getIsLoop()):
        menu.showMenu()
        match menu.getPilihan():
            
            # Menu Sistem Persamaan Linear
            case 1 :
                print("\t     Sistem Persamaan linier".upper())
                print("-"*50)
                menu.showSubMenu()
                
                # Pengondisian untuk submenu
                match menu.getPilihan():
                    # Metode Gaussian
                    case 1: 
                        print("Metode Eliminasi Gaussian".upper())
                        print("-"*50)
                        spl.takeInput()
                        spl.printGaussianElimination()
                        
                    # Metode Gauss Jordan
                    case 2:
                        print("Metode Eliminasi Gauss Jordan".upper())
                        print("-"*50)
                        spl.takeInput()
                        spl.printGaussJordan()
                        
                    # Metode Balikan Matriks
                    case 3:
                        print("Metode Balikan Matriks".upper())
                        print("-"*50)
                        spl.takeInput()
                        spl.printSolvingInv()
                    
                    # User memberikan pilihan yang tidak dikenali
                    case _:
                        print("Masukan Anda Salah!")
                        menu.setisLoop(False)
                        break
                menu.backTo()
            
            # Menu Determinan Matriks
            case 2 :
                print("Determinan Matriks".upper())
                print("-"*50)
                menu.showSubMenu()
                
                # Pengondisian untuk submenu
                match menu.getPilihan():
                    # Gaussian
                    case 1: 
                        print("Metode Eliminasi Gaussian".upper())
                        matriks.takeSquareInput()
                        matriks.printGaussianDet()
                        
                    # Gauss Jordan
                    case 2:
                        print("Metode Eliminasi Gauss Jordan".upper())
                        matriks.takeSquareInput()
                        matriks.printGaussJordanDet()
                        
                    # Metode Balikan Matriks
                    case 3:
                        print("Metode Balikan Matriks".upper())
                        matriks.takeSquareInput()
                        matriks.printInversMatriksDet()
                        
                    # User memberikan masukan yang tidak dikenali
                    case _:
                        print("Masukan Anda Salah!")
                        menu.setisLoop(False)
                        break
                        
                menu.backTo()
            
            # Menu Matriks Invers
            case 3 :
                print("Matriks Invers".upper())
                print("-"*50)
                menu.showSubMenu()
                
                # Pengondisian untuk submenu
                match menu.getPilihan():
                    # Gaussian
                    case 1: 
                        print("Metode Eliminasi Gaussian".upper())
                        matriks.takeSquareInput()
                        matriks.printGaussianInverse()
                        
                    # Gauss Jordan
                    case 2:
                        print("Metode Eliminasi Gauss Jordan".upper())
                        matriks.takeSquareInput()
                        matriks.printGaussJordanInv()
                        
                    # Metode Balikan Matriks
                    case 3:
                        print("Metode Balikan Matriks".upper())
                        matriks.takeSquareInput()
                        matriks.printInverseMatrix()
                    
                    # User memberikan masukan yang tidak dikenali
                    case _:
                        print("Masukan Anda Salah!")
                        menu.setisLoop(False)
                        break
                        
                menu.backTo()

            # Transpose Matriks
            case 4 :
                print("Transpose Matriks".upper())
                matriks.takeInput()
                matriks.printTranspose()
                menu.backTo()
                
            # Operasi Aritmatika Matriks
            case 5 :
                print("Operasi Aritmatika Matriks".upper())
                print("-"*50)
                menu.showMenuAritmatika()
                
                # Pengondisian untuk submenu operasi aritmatika matriks
                match (menu.getPilihan()):
                    case 1:
                        print("Perkalian Matriks".upper())
                        print("-"*50)
                        matriks.printDot()
                        
                    case 2:
                        print("Penjumlahan dan Pengurangan Matriks".upper())
                        print("-"*50)
                        matriks.printAddSubtract()
                    
                    case _:
                        print("Masukan Anda Salah")
                        menu.setisLoop(False)
                        break
                menu.backTo()
            
            # Menu LU faktorisasi
            case 6 :
                print("LU Faktorisasi".upper())
                matriks.takeInput()
                matriks.printLUFactorization()                
                menu.backTo()

            # Menu Eigen
            case 7 :
                print("Eigen Value, Eigen Vektor, dan Persamaan Polinomial Karakteristiknya".upper())
                matriks.takeSquareInput()
                matriks.printEigen()
                menu.backTo()
            
            # Menu Diagonalisasi Matriks
            case 8 :
                print("Diagonalisasi Matriks".upper())
                matriks.takeSquareInput()
                matriks.printDiagonalization()
                menu.backTo()
            
            # Menu Singular Value Decomposition
            case 9 :
                print("Singular Value Decomposition (SVD)".upper())
                matriks.takeInput()
                matriks.printSVD()
                menu.backTo()
            
            # Exit
            case 0 :
                menu.setisLoop(False)
                break
            
            # Jika user memberikan masukan yang tidak dikenali, program akan keluar
            case _:
                print("Masukan Anda Salah! Program Diakhiri...")
                menu.setisLoop(False)
                break
    
    print("-"*50)
    print(Fore.BLUE + " Terima Kasih telah  menggunakan Kalakulator kami".upper())
    print(Style.RESET_ALL, end='')
    print("-"*50)
    print()