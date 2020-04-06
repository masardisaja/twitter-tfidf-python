# Menghitung bobot kata dari hasil crawling twitter dengan metode TF-IDF
# Dibuat oleh Ardiansyah
# NIM 14002404

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import re
import math
import json
import csv

data_file = "twitter_data.xlsx"	# Nama file hasil crawling data Twitter
output_dir = "output/"			# Nama folder untuk menulis output

print("Nama file : ",data_file)
print("Folder output : ",output_dir)


def write_csv(dict,filename):
	w = csv.writer(open(output_dir + filename + ".csv", "w"))
	for key, val in dict.items():
		w.writerow([key, val])
		
#Fungsi membuat list stopword dari file txt
def stopword():
	file = open('tokens/stopword_list_tala.txt', 'r') 
	Lines = file.readlines() 
	listStopword = []
	
	# Strips the newline character 
	for line in Lines: 
		listStopword.append(line.strip())
		
	return listStopword

#Fungsi change case (ubah text menjadi huruf kecil semua)
def change_case(txt):
	return(txt.lower())

#Fungsi remove linebreaks (mengubah newline pada text menjadi spasi sehingga tweet menjadi 1 baris)
def rem_linebreak(txt):
	return(txt.replace('\n', ' ').replace('\r', ''))

#Fungsi remove RT (menghapus kata RT)
def rem_rt(txt):
	return(re.sub(r'rt @', '@', txt))

#Fungsi remove http/https ( menghapus link/url di dalam tweet)
def rem_http(txt):
	return(re.sub(r'(https?|http)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]', '', txt))

#Fungsi remove @mention (menghapus username mention di dalam tweet)
def rem_mention(txt):
	return(re.sub(r'@[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]', '', txt))
	
#Fungsi remove #hashtag (menghapus hashtag di dalam tweet)
def rem_hashtag(txt):
	return(re.sub(r'#[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]', '', txt))
	
#Fungsi remove non-alphabet (menghapus karakter yang bukan alphabet)
def rem_nonalpha(txt):
	return(re.sub(r'[^a-z]',' ',txt))
	
#Fungsi remove stopword (menghapus stopword di dalam tweet)
def rem_stopword(txt):
	stopwords = stopword()
	querywords = txt.split()

	resultwords  = [word for word in querywords if word.lower() not in stopwords]
	result = ' '.join(resultwords)

	return result

#Fungsi remove multiple spaces (mengganti karakter spasi yang lebih dari 1 menjadi hanya 1 spasi)
def rem_spaces(txt):
	txt = re.sub(' +', ' ', txt)
	return(txt.lstrip())

#fungsi remove short length (menghapus kata-kata yang memiliki jumlah karakter <4)
def rem_short(txt):
	if len(txt)<4:
		txt = ""
	return txt

# ------------------------------------------------------------------------------------
# Proses menghitung nilai TF-IDF
# ------------------------------------------------------------------------------------

df = pd.read_excel(data_file) 	#Baca file excel data twitter
listText = df['Text']			#Ambil kolom Text dan buat sebagai sebuah list dengan nama listText
listNewText = []				#Buat sebuah list baru dengan nama listNewText untuk menampung hasil pre-processing

# Lakukan pre-processing dengan menjalankan fungsi-fungsi yang telah didefinisikan di atas
for t in listText:
	t = change_case(t)
	t = rem_linebreak(t)
	t = rem_rt(t)
	t = rem_http(t)
	t = rem_mention(t)
	t = rem_hashtag(t)
	t = rem_nonalpha(t)
	t = rem_short(t)
	t = rem_spaces(t)
	t = rem_stopword(t)
	# Masukkan hasil pre-processing ke dalam listNewText
	listNewText.append(t)

#remove duplicates in list : Hapus duplikasi data dari hasil pre-processing
NA = len(listNewText) 							# Hitung jumlah data awal di dalam listNewtext
listNewText = list(dict.fromkeys(listNewText))	# Gunakan hanya unique value dari listNewText (hapus duplikasi)
N = len(listNewText)							# Hitung jumlah data akhir di dalam listNewText
print("Jumlah data awal : ",NA," records")
print("Jumlah data bersih : ",N," records")

#create TF for each record : Menghitung nilai TF setiap kata/token di dalam setiap record
TFDict = []				# Buat sebuah list baru dengan nama TFDict
for t in listNewText:	# Baca list listNewText dan definiskan setiap recordnya sebagai variabel t
	tokens = t.split()	# Pisahkan setiap kata di dalam record menjadi sebuah list dengan nama tokens
	tf = {}				# Buat sebuah set baru dengan nama tf
	n = len(tokens)		# Hitung jumlah record di dalam list tokens, simpan sebagai nilai n
	for w in tokens:	# Baca list tokens dan definiskan setiap recordnya sebagai variabel w
		if w in tf:		
			tf[w]+=1	# Jika w sudah ada di dalam set tf maka nilai tf[w] ditambah 1
		else:
			tf[w]=1		# Jika w belum ada di dalam set tf maka nilai tf[w] = 1
	for w in tf:
		tf[w]=tf[w]/n	# Hitung nilai tf dari w dengan rumus tf[w]/n
		
	TFDict.append(tf)	# Masukkan nilai tf[w] ke dalam list TFDict

n = 0					# Set nilai n = 0
TF = {}					# Buat sebuah set baru dengan nama TF
for r in TFDict:		# Baca list TFDict dan definisikan setiap recordnya sebagai variabel r
	r = json.dumps(r)	# Ubah tipe data variabel r yang sebelumnya sebuah set menjadi string json
	TF[n] = {r}			# Masukkan r ke dalam set TF[n]
	n+=1				# Set nilai n = n + 1
write_csv(TF,"TF")		# Tuliskan set TF ke dalam file csv dengan nama TF

#create DF list for each token
DF_list = {}					# Buat sebuah listbaru dengan nama DF_List
n = 0							# Set nilai n = 0
for t in listNewText:			# Baca list listNewText dan definisikan setiap recordnya sebagai variabel t
	tokens = t.split();			# Pisahkan setiap kata di dalam record menjadi sebuah list dengan nama tokens
	for w in tokens:			# Baca list tokens dan definiskan setiap recordnya sebagai variabel w
		try:
			DF_list[w].add(n)	# Jika w sudah ada di dalam set DF_List maka tambahkan value n ke dalam list DF_List[w]
		except:
			DF_list[w] = {n}	# Jika w belum ada di dalam set DF_List maka buat list DF_List[w] dengan value n
	n+=1						# Set nilai n = n + 1
write_csv(DF_list,"DF_list")	# Tulis set DF_List ke dalam file csv dengan nama DF_List

#create DF count for each token
DF = {}							# Buat sebuah set baru dengan nama DF
for w in DF_list:				# Baca list DF_List dan definisikan setiap recordnya sebagai variabel w
	DF[w] = len(DF_list[w])		# Hitung jumlah record di dalam DF_List[w] dan simpan ke dalam set DF[w]
write_csv(DF,"DF")				# Tulis set DF ke dalam file csv dengan nama DF

#create IDF count for each token
IDF_val = {}							# Buat sebuah set baru dengan nama IDF_val
for w in DF:							# Baca set DF dan definisikan setiap recordnya sebagai variabel w
	IDF_val[w] = math.log(N/(DF[w]+1))	# Hitung nilai IDF dengan rumus log(N/(DF[w]+1)) dan simpan sebagai IDF_val[w]

IDF = {}								# Buat set baru dengan nama IDF
for key in sorted(IDF_val.keys()) :		# Baca key di dalam IDF_val diurutkan secara ascending
    IDF[key] = IDF_val[key]				# Masukkan nilai IDF_val[key] ke dalam set IDF
	
# Di sini kita sudah mendapatkan daftar nilai IDF dari setiap token yang berurut secara ascending
# Simpan set IDF tersebut ke dalam file dengan nama IDF.csv
f = open(output_dir+"IDF.csv","a")
for key,val in IDF.items():
		f.write(str(key)+","+str(val).translate({ord('{'):None, ord('}'):None})+"\n")
f.close
#print(IDF)

#Menghitung nilai TF*IDF
TF_IDF = []								# Buat sebuah list baru dengan nama TF_IDF
for i in TFDict:						# Baca list TFDict dan definisikan setiap recordnya sebagai variabel i
	tfidf = {}							# Buat sebuah list baru dengan nama tfidf
	for key, val in i.items():			# Baca key dan value di dalam variable i
		tfidf[key] = {val*IDF[key]}		# Hitung nilai TF-IDF dengan rumus val*IDF[key] dan simpan sebagai tfidf[key]
	TF_IDF.append(tfidf)				# Tambahkan set tfidf ke dalam list TF_IDF

# Di sini kita sudah mendapatkan daftar nilai TF-IDF dari setiap token di dalam setiap tweet
# Simpan list TF-IDF tersebut ke dalam file dengan nama TFIDF.csv
f = open(output_dir+"TFIDF.csv","a")
n=0
for r in TF_IDF:
	for key,val in r.items():
		f.write(str(n)+","+str(key)+","+str(val).translate({ord('{'):None, ord('}'):None})+"\n")
	n+=1
f.close	
