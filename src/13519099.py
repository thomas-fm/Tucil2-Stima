# Thomas Ferdinand Martin
# 13519099
# Tucil 2 : Decrease and Conquer

# run : python 13519099_versi2.py
# berhasil di run menggunakan python versi 3.9.0

# Definisi class beserta method dan atribut
class Graf:
    def __init__(self):
        # Graf = menyimpan list sisi yang masuk, indeks ke i pada graf berkorespondensi dengan simpul ke i pada simpul
        # Bentuk fisik :
        # graf = [[C2,C3], [C3], []]
        # simpul = [C1, C2, C3]
        # Menunjukkan C1 bersisian dengan C2 dan C3 dengan C2 dan C3 adalah sisi yang masuk ke C1. C3 tidak memiliki sisi masuk

        # List pada graf[i] = sisi yang masuk pada simpul[i]
        self.graf = [] 
        # List simpul-simpul (kode mata kuliah) yang ada pada graf
        self.simpul = []
        # Hasil dari topological sort
        self.result = []

    # Fungsi menambahkan simpul pada graf
    def addSimpul(self, simpul):
        self.simpul.append(simpul)
        self.graf.append([])
    
    # Fungsi menambahkan sisi masuk pada suatu simpul
    def addSisiMasuk(self, simpul, simpul_masuk):
        idx = self.simpul.index(simpul)
        self.graf[idx].append(simpul_masuk)

    # Fungsi menghapus suatu simpul dari graf
    def hapusSimpul(self, simpul):
        idx = self.simpul.index(simpul)
        self.simpul.remove(self.simpul[idx])
        
        sisi = self.graf[idx]
        self.graf.remove(sisi)
    
    # Menghapus sisi yang menghubungkan simpul dan simpul_masuk dari graf
    def hapusSisi(self, simpul, simpul_masuk):
        idx = self.simpul.index(simpul)
        self.graf[idx].remove(simpul_masuk)
    
    # Mengembalikan true apabila graf kosong
    def isEmpty(self):
        return self.simpul == []
    
    # Untuk keperluan testing
    def printGraf(self):
        print(self.graf)
        print(self.simpul)
    
    # Fungsi-fungsi utama topologicalSort
    # Fungsi menambahkan matkul yang saat itu pre requisitnya terpenuhi atau seolah-olah tidak memiliki pre requisit ke dalam list mata kuliah per semester
    # Fungsi kemudian mengubah kondisi graf dengan menghapus mata kuliah yang memiliki derajat masuk
    def hapusZeroInDegree(self):
        # List berisi mata kuliah yang harus diambil pada semester tertentu
        current_semester = []

        # Untuk setiap data mata kuliah dengan pre requisitnya
        i = 0
        for elm in self.graf:
            # Jika saat itu mata kuliah tidak memiliki pre requisit (jumlah derajat masuk = 0), maka tambahkan ke dalam array mata kuliah yang bisa diambil dalam satu semester itu (current_semester)
            if (len(elm) == 0):
                current_semester.append(self.simpul[i])
            i+=1
        
        # Hapus mata kuliah yang diambil pada semester tersebut dari daftar mata kuliah yang masih perlu diambil (hapus simpul dari graf)
        for matkul in current_semester:
            self.hapusSimpul(matkul)

        # Tambahkan data mata kuliah semester tersebut ke dalam array hasil
        self.result.append(current_semester)

        return current_semester

    # Fungsi menghapus derajat masuk dari mata kuliah yang pra syaratnya sudah diambil disemester tersebut atau yang ada pada array current_semester
    def hapusSimpulTetangga(self, current_semester):
        for matkul in current_semester:
            for sisa_matkul in self.graf:
                # Jika ditemukan matkul pra syarat yang sudah terambil maka seolah-olah hapus sisi masuk graf
                if (sisa_matkul.count(matkul) == 1):
                    self.hapusSisi(self.simpul[self.graf.index(sisa_matkul)], matkul)

    # Topological sort dengan decrease and conquer
    def topologicalSort(self):
        # Basis ketika sudah tidak ada mata kuliah yang perlu diambil (tersisa 0 simpul)
        if self.isEmpty():
            return
        else:
            # Pemanggilan fungsi penghapusan simpul derajat masuk 0
            current_semester = self.hapusZeroInDegree()
            # Pemanggilan fungsi penghapusan sisi yang bersisian dengan simpul yang terhapus
            self.hapusSimpulTetangga(current_semester)
            # Pemanggilan rekursif
            self.topologicalSort()

    # Mengembalikan hasil topological sort
    def getResult(self):
        return self.result

    # Fungsi menulis hasil ke layar
    def printHasil(self):
        print("============++++============")
        for i in range(len(self.result)):
            print("Semester",i+1,": ", end="")
            for matkul in self.result[i]:
                print(matkul, end=" ")
            print("\r")

        # Apabila jumlah semester yang harus diambil lebih dari 8
        if len(self.result) > 8:
            print("Sayang sekali sepertinya nanti kelulusan Anda harus ditunda jika mau mengikuti seluruh mata kuliah ini.")
        print("============++++============")

#---------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#

# Fungsi membuka dan membaca file dan mengubahnya ke dalam bentuk graf
def readFile(namaFile):
    try:
        f = open("../test/" + namaFile, 'r')
    except:
        print("Salah memasukkan nama file")
        return

    graf_matkul = Graf()

    print("============++++============")
    for line in f:
        matkul = line.replace(" ","").replace(".", "").replace("\n","").split(",")
        simpul = matkul[0]
        
        print("Kode matakuliah :", simpul)
        print("Prasyarat : ", end="")

        for kode in matkul:
            if kode == simpul:
                graf_matkul.addSimpul(kode)
            else:
                graf_matkul.addSisiMasuk(simpul, kode)
                print(kode, end=" ")
        
        if len(matkul) == 1:
            print("-", end=" ")
        
        print("\r")

    return graf_matkul

# Program utama
# Input nama file
g = Graf()
x = input("Masukkan nama file [1-8].txt : ")
# Pembacaan file dan transformasi ke graf
try:
    g = readFile(x)
    g.topologicalSort()
    g.printHasil()
# Bila terjadi error
except:
    print("Pastikan input benar")