# twitter-tfidf-python
Mengukur bobot kata di dalam tweet dengan metode TF-IDF

Untuk menggunakan script ini yang harus dilakukan adalah:
1. Install Python 3.8 yang dapat didownload dari https://www.python.org/downloads/
2. Setelah Python terinstall, selanjutnya install modul-modul berikut:
   a. pandas
   b. re
   c. math
   d. json
   e. csv
   [Cara install modul melalui command prompt ketik "pip install nama_modul"]
3. Setelah semua modul terinstall, siapkan sebuah folder untuk aplikasi ini.
   Misalnya C:\Praktek_Python
   Simpan file "read_exceltweet.py", "stopword_list_tala.txt", dan file excel yang berisi data twitter (misal "twitter_data.xlsx") di dalam folder tersebut.
   Kemudian buat folder baru dengan nama "output" di dalam folder tersebut.
   Sehingga strukturnya adalah sebagai berikut:
   C:\Praktek_Python
		|-- output
		|-- read_exceltweet.py
		|-- stopword_list_tala.txt
		|-- twitter_data.xlsx
 4. Aplikasi sudah siap dijalankan melalui command prompt.
    a. buka Command Prompt
    b. Masuk ke folder yang telah dibuat pada nomor 3
       > cd C:\Praktek_Python <ENTER>
       C:\Praktek_Python> _
    c. jalankan file read_exceltweet.py
       C:\Praktek_Python> read_exceltweet.py <ENTER>
       Nama file :  twitter_data.xlsx
       Folder output :  output/
       Jumlah data awal :  xxxx  records
       Jumlah data bersih :  xxx  records
       C:\Praktek_Python> _
    d. Setelah proses selesai, silakan cek folder output untuk melihat hasil-hasil proses tsb.
       Agar lebih jelas silakan sambil dibaca penjelasan yang disertakan di dalam script read_exceltweet.py
