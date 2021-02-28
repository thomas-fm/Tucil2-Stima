# Thomas Ferdinand Martin
# 13519099
# Tucil 2 : Decrease and Conquer

# run : python Tucil2_13519099.py
# berhasil di run menggunakan python versi 3.9.0

# Representasi graf menggunakan struktur array multidimensi
# Bentuk fisik :
# Elemen G[i][0] adalah nama simpul, G[i][1] - G[i][n] adalah nama simpul dari sisi yang masuk ke simpul i
#  [
#   [simpul1, simpul_masuk_1, simpul_masuk_2], 
#   [simpul2, simpul_masuk_1],
#   [simpul3]
# ]

# Membuka dan membaca file
def readFile(namaFile):
    f = open("../test/" + namaFile, 'r')
    matkul_dan_prereq = []

    for line in f:
        matkul = line.replace(" ","").replace(".", "").replace("\n","").split(",")
        matkul_dan_prereq.append(matkul)
    
    return matkul_dan_prereq

# Fungsi menambahkan matkul yang saat itu pre requisitnya terpenuhi atau seolah-olah tidak memiliki pre requisit ke dalam list mata kuliah per semester
# Fungsi kemudian mengubah kondisi graf dengan menghapus mata kuliah yang memiliki derajat masuk
# Variabel result berisi simpul-simpul hasil akhir topologicalSort
# Bentuk fisik array : [[C1], [C2, C3], [C4,C5,C6]]
# Menunjukkan semester 1 perlu mengambil matkul dengan kode C1, semester 2 mengambil C2 dan C3, semester 3 mengambil C4, C5, C6
def hapusZeroInDegree(kumpulan_mata_kuliah, result):
    # List berisi mata kuliah yang harus diambil pada semester tertentu
    current_semester = []

    # Untuk setiap data mata kuliah dengan pre requisitnya
    # Graf tersimpan pada variabel mata kuliah
    for elm in kumpulan_mata_kuliah:
        # Jika saat itu mata kuliah tidak memiliki pre requisit, maka tambahkan ke dalam array mata kuliah yang bisa diambil dalam satu semester itu (current_semester)
        if (len(elm) == 1):
            current_semester.append(elm[0])
    
    # Hapus mata kuliah yang diambil pada semester tersebut dari daftar mata kuliah yang masih perlu diambil (hapus simpul dari graf)
    for matkul in current_semester:
        kumpulan_mata_kuliah.remove([matkul])

    # Tambahkan data mata kuliah semester tersebut ke dalam array hasil
    result.append(current_semester)
    return current_semester

# Fungsi menghapus derajat masuk dari mata kuliah yang pra syaratnya sudah diambil atau berada pada array matkul_terambil
def hapusSimpulTetangga(mata_kuliah, current_semester):
    for matkul in current_semester:
        for sisa_matkul in mata_kuliah:
            # Jika ditemukan matkul pra syarat yang sudah terambil maka seolah-olah hapus sisi masuk graf
            if (sisa_matkul.count(matkul) == 1):
                sisa_matkul.remove(sisa_matkul[sisa_matkul.index(matkul)])

# Topological sort pendekatan decrease and conquer
def topologicalSort(mata_kuliah, result):
    # Basis ketika sudah tidak ada mata kuliah yang perlu diambil (tersisa 0 simpul)
    if len(mata_kuliah) == 0:
        return
    else:
        # Pemanggilan fungsi penghapusan simpul derajat masuk 0
        current_semester = hapusZeroInDegree(mata_kuliah, result)
        # Pemanggilan fungsi penghapusan sisi yang bersisian dengan simpul yang terhapus
        hapusSimpulTetangga(mata_kuliah, current_semester)
        # Pemanggilan rekursif
        topologicalSort(mata_kuliah, result)

# Fungsi menulis hasil ke layar
def printHasil(result):
    print("============++++============")
    for i in range(len(result)):
        print("Semester",i+1,": ", end="")
        for matkul in result[i]:
            print(matkul, end=" ")
        print("\r")

    # Apabila jumlah semester yang harus diambil lebih dari 8
    if len(result) > 8:
        print("Sayang sekali sepertinya nanti kelulusan Anda harus ditunda jika mau mengikuti seluruh mata kuliah ini.")
    print("============++++============")

# Fungsi menulis info matkul ke layar
def printMatkul(kumpulan_matkul):
    print("============++++============")
    for info_matkul in kumpulan_matkul:
        print("Kode mata kuliah :", info_matkul[0])
        print("Prasyarat : ", end ="")

        if (len(info_matkul) == 1):
            print("-")
            continue
        else:
            for kode in info_matkul:
                if (kode != info_matkul[0]):
                    print(kode, end=" ")
        print("\r")
    print("============++++============")

# Program utama
# Input nama file
x = input("Masukkan nama file [1-8].txt : ")
# Pembacaan file dan transformasi ke graf
matkul = readFile(x)
# Print info matkul
printMatkul(matkul)
# Topological sort
result = []
topologicalSort(matkul, result)
# Print hasil sort
printHasil(result)