import telebot
from ngram import NGram
import numpy
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from flask import Flask, request
import time
from dotenv import load_dotenv
import os

load_dotenv()


def configure_routes(app, bot):
    @app.route("/")
    def index():
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=os.getenv("WEBHOOK"))
        return "ok", 200

    @app.route('/webhook', methods=['POST'])
    def webhook():
        update = telebot.types.Update.de_json(
            request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "ok", 200


bot = telebot.TeleBot(os.getenv("TOKEN"), threaded=False)
app = Flask(__name__)
configure_routes(app, bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Diagnosa akan dimulai:\n\n Silakan ketik gejala kucing anda dengan diawali "/diagnosa". \n contoh: /diagnosa kucing saya tidak nafsu makan.')


@bot.message_handler(commands=['diagnosa'])
def send_welcome(message):
    try:
        if len(message.text) > 10:
            jenis = proses(message.text)
            # print(jenis == None)
            if (jenis != None).any():
                # print(jenis.size)
                # bot.reply_to(message, jenis.size)
                if jenis != '0':
                    ukuran_diagnosa = jenis.size
                    # print(ukuran_diagnosa)
                    if ukuran_diagnosa > 1:
                        # print(ukuran_diagnosa)
                        message.text = "Terdapat " + str(
                            ukuran_diagnosa) + " jenis penyakit yang mungkin menyerang kucing anda"
                        bot.reply_to(message, message.text)
                        for i in range(ukuran_diagnosa):
                            hasil = str(i + 1) + ". Penyakit " + \
                                str(diagnosa(jenis[0][i]))
                            bot.reply_to(message, hasil)

                    else:
                        hasil = "Kemungkinan kucing anda menderita penyakit " + \
                            str(diagnosa(jenis[0][0]))
                        bot.reply_to(message, hasil)
                        desc = deskripsi_penyakit(jenis)
                        for i in range(desc.__len__()):
                            message.text = desc[i][0]
                            bot.reply_to(message, message.text)

                else:
                    message_res = "Diagnosa penyakit belum ditemukan, silahkan masukkan lebih banyak gejala yang terjadi pada anjing anda"
                    bot.reply_to(message, message_res)
            else:
                bot.reply_to(
                    message, 'Gejala tidak ditemukan. Silakan kirimkan gejala!')
        else:
            bot.reply_to(message, 'Silakan kirimkan gejala!')
    except Exception as e:
        bot.reply_to(message, 'Maaf, terjadi kesalahan. Silakan coba lagi!')


def deskripsi_penyakit(jenis):
    deskripsi = ""
    if (jenis == 0):
        deskripsi = (["Bartonellosis atau yang lebih dikenal dengan cat scratch disease adalah infeksi yang disebabkan oleh cakaran kucing yang terinfeksi bakteri Bartonella henselae. \n"
                      "Bakteri ini merupakan salah satu jenis bakteri paling umum di dunia, yang kerap ditemukan di mulut atau cakar kucing."],
                     ["Penanganan: \n"
                      "Pemberian antibiotik untuk mencegah infeksi sekunder atau infeksi lain, Pemberian terapi nebulizer untuk mengatasi penyumbatan pada saluran pernafasan, pemberian obat tetes mata."],
                     ["Pencegahan: \n"
                      "Jaga kbersihan kandang dan peralatan kucing, Jaga kwalitas pakan kucing, Berikan vaksinasi secara rutin."])
    elif (jenis == 1):
        deskripsi = (["Kecacingan atau helminthiasis adalah salah satu penyakit yang perlu diperhatikan pada kucing. \n"
                      "Kecacingan sering diabaikan karena tidak menimbulkan gejala klinis yang serius, kecuali pada infeksi berat dan kronis."],
                     ["Penanganan: \n"
                      "Memberi obat cacing pada kucing misalnya vermox, combantrin (pfizer), drontal plus (bayer), drontal cat (bayer), Jangan memberikan obat cacing pada kucing yang hamil karena dapat menyebabkan kematian pada anaknya."],
                     ["Pencegahan: \n"
                      "Memberikan obat cacing secara rutin, Membersihkan litter box (kotak) pasir, Wadah makan dan minum harus dibersihkan setiap hari, Periksakan kotoran hewan pada klinik hewan bagi hewanyang sedang dalam pengeobatan, Minimalkan kontak dengan hewan liar."])
    elif (jenis == 2):
        deskripsi = (["Feline Calicivirus adalah suatu penyakit yang disebabkan oleh virus dari famili caliciviridae. \n"
                      "Virus calici merupakan salah satu dari jenis cat flu yang paling sering menyerang kucing selain herpes virus (FHV)."],
                     ["Virus ini dapat masuk kedalam tubuh melalui mata, hidung (pernafasan) dan mulut.\n"
                      "karena partikel yang sangat kecil dan sangat mudah menempel pada sembarang tempat, seperti lantai, tempat tidur kucing, makanan, air minum, dan bahkan baju atau tangan manusia yang tidak steril, maka penularan dapat sangat cepat terjadi.\n"
                      "Masa inkubasi dari virus ini relatif cepat yaitu 2-4 hari"],
                     ["Penanganan: \n"
                      "Memberi obat anti biotik, Memberi cairan intravena."],
                     ["Pencegahan: \n"
                      "Vaksinasi kucing secara teratur."])
    elif (jenis == 3):
        deskripsi = (["Mite atau tungau merupakan parasit sejenis kutu yang berukuran sangat kecil dan tidak bisa dengan mudah dilihat dengan mata telanjang. \n"
                      "Parasit ini sangat mudah menular dari satu hewan ke hewan lain sehingga adanya tungau telinga pada kucing merupakan hal yang lazim dijumpai terutama pada kucing yang bebas berkeliaran di luar rumah atau pada kucing yang tinggal bersama kucing lain dalam satu rumah dimana kontak satu kucing dengan kucing lainnya akan memudahkan penularan."],
                     ["Penanganan: \n"
                      "Bersihkan kotoran telinga pada kucing menggunakan cutton bud, Bersihkan telinga kucing memakaikan astringent atau cairan pembersih telinga. \n"
                      "Teteskan obat antiparasit pada tengkuk (spot on) yang ada antiparasit seperti selamctine."],
                     ["Pencegahan: \n"
                      "Selalu bersihkan telinga kucing secara berkala."])
    elif (jenis == 4):
        deskripsi = (["Panleukopenia adalah penyakit menular yang disebabkan oleh parvovirus. \n"
                      "Virus ini sangat rentan menyerang anak kucing dan tidak menginfeksi manusia. \n"
                      "Panleukopenia menginfeksi kucing dengan cara membunuh sel-sel yang aktif membelah di sumsum tulang, usus dan janin yang sedang berkembang. \n"
                      "Meski lebih rentan menyerang anak kucing, kucing dari segala usia juga dapat terinfeksi panleukopenia, terutama pada kucing yang tidak mendapat vaksinasi."],
                     ["Penanganan: \n"
                      "Memisahkan kucing dengan kucing yang lain, Membawa kucing ke dokter hewan, sesegera mungkin, Bersihkan kandang dan tempat kucing bermain dengan desinfektan, Beri makan kucing sesering mungkin dengan makanan yang lunak dan mudah dicerna, Berikan vitamin Kis Kis Pastils MultiVit untuk meningkatkan kekebalan tubuh kucing."],
                     ["Pencegahan: \n"
                      "Vaksinasinasi teratur, Jaga kebersihan kan dang, Jaga pola makan kucing, Pemberian vitamin untuk menjaga kekebalan tubuh kucing."])
    elif (jenis == 5):
        deskripsi = (["Feline rhinotracheitis (FHV) adalah gangguan umum pada kucing dan anak kucing, dan bersama dengan feline calcivirus (FCV) dapat menyebabkan 'flu kucing'. "],
                     ["Feline viral rhinotracheitis ( FVR ) adalah infeksi saluran pernapasan atas atau paru-paru kucing yang disebabkan oleh Felid alphaherpesvirus 1 (FeHV-1), dari famili Herpesviridae. \n"
                      "Penyakit ini juga sering disebut sebagai feline influenza, feline coryza, dan feline pneumonia tetapi, karena istilah ini menggambarkan kumpulan gejala pernapasan lain yang sangat berbeda, istilah ini salah untuk kondisi tersebut. \n"
                      "Viral penyakit pernafasan pada kucing bisa serius, terutama di catteries dan kandang. \n"
                      "Menyebabkan setengah dari penyakit pernapasan pada kucing."],
                     ["Penanganan: \n"
                      "Memberi antibiotik spektrum luas, misalnya dengan obat tetrasiklin.Memberi obat tetes hidung yang berisi ephedrine sulfate o,25% sebanyak dua tetes untuk setiap lubang hidung."],
                     ["Pencegahan: \n"
                      "Vaksinasi rutin menggunakan vaksin FHV-1, Anak kucing berumur 6 -12 minggu diberi vaksin MLV, Isolasikan kucing yang sakit."])
    elif (jenis == 6):
        deskripsi = (["Feline Lower Urinary Tract Disease atau penyakit saluran kencing bagian bawah pada kucing adalah gangguan saluran kemih yang sering terjadi pada kucing, terutama kucing jantan.\n"
                      "Penyakit ini dulu disebut sindrom urologik kucing. \n"
                      "Masalah kesehatan ini mengganggu kandung kemih dan uretra kucing."],
                     ["Penanganan: \n"
                      "Memberi kucing dengan cairan antibiotik dan cairan IV, Melakukan diet bagi yang mengalami obositas atau berikan makanan khusus yang bisa melarutkan kristal mineral atau batu pada saluran urine kucing, Melakukan pembedahan untuk menghilang kan sumbatan pada uretra dan untuk mencegah terjadinya pengulangan timbulnya Kristal mineral."],
                     ["Pencegahan: \n"
                      "Pemberian pakan khusus yang rendah mg, tinggi Na atau pakan yang mempunyai PH cukup rendah. Diupayakan agar kucing diberikan pakan yang basah, penyediaan air segar sebagai sumber air minum yang cukupHindari kucing dari obesitas, Bersihkan kandangnya secara rutin."])
    elif (jenis == 7):
        deskripsi = (["Hepatitis pada kucing adalah salah satu penyakit yang menyerang organ hati atau liver. \n"
                      "Penyakit ini merupakan salah satu yang cukup mematikan jika dibiarkan tanpa penanganan yang tepat. \n"
                      "Penyebab kucing terkena hepatitis bisa beragam. \n"
                      "Salah satunya adalah tertular dari kucing lain yang menderita hepatitis melalui darah atau feses."],
                     ["Penanganan: \n"
                      "Memberi antibiotik dan steroid untuk membunuh bakteri, Melakukan kemoterapi dan pembedahan radiasi yang berguna untuk mengecilkan dan membunuh sel kanker, Melakukan transfusi darah."],
                     ["Pencegahan: \n"
                      "Menjaga agar berat badan kucing tetap stabil dan mengatur kolesterol dalam batas yang disarankan, Menjaga kebersihan kucing dan lingkungan nya, Rutin memandikan dan membersihkan daerah kuku, telinga dan mata kucing, Mencuci tempat pakan dan kandang secara rutin, Hindarkan kucing bergaul dengan kucing liar."])
    elif (jenis == 8):
        deskripsi = (["Otitis (radang pada telinga)  pada telinga kucing. \n"
                      "Penyakit yang sering terjadi pada kucing selain jamur adalah radang telinga atau otitis. \n"
                      "Otitis adalah sakit atau peradangan pada saluran pendengaran, yang ditandai dengan nyeri, demam, hilangnya pendengaran, tinitus dan vertigo. \n"
                      "Otitis sendiri dibagi menjadi 3 jenis berdasarkan tempat terjadinya peradangan, yaitu: otitis eksterna, otitis media dan otitis interna Otitis pada telinga luar sering terjadi karena telinga bagian luar lebih sering kontak dengan benda asing, bakteri, jamur, ear mites dan air yang kotor."],
                     ["Penanganan: \n"
                      "Memberikan obat antiradang dan antibiotik pada kucing, Memberikan obat yang mengandung anti ektoparasit."],
                     ["Pencegahan: \n"
                      "Memberikan hipoalergenik untuk membantu kucing yang alergi terhadap makanan, Sering memeriksa kondisi kesehatan telinga kucing, Melakukan grooming secara teratur, Harus selalu memperhatikan kebersihan tubuh kucing terutama pada bagian kepala dan telinga kucing"])
    elif (jenis == 9):
        deskripsi = (["Pyometra adalah satu penyakit yang sebagian besar diderita kucing di usia pertengahan. \n"
                      "Penyakit ini berupa infeksi rahim disebabkan oleh penyimpangan hormon yang bisa menimbulkan infeksi bakteri sekunder."],
                     ["Penanganan: \n"
                      "Melakukan operasi pada kucing, Memberi antibiotik."],
                     ["Pencegahan: \n"
                      "Membiaki kucing betina saat masih muda, Mengangkat rahim dan ovarium kucing."])
    elif (jenis == 10):
        deskripsi = (["Rabies adalah penyakit virus yang menyerang otak dan sumsum tulang belakang semua mamalia, termasuk kucing, anjing, dan manusia. \n"
                      "Rabies disebabkan oleh virus RNA untai tunggal dari genus Lyssavirus, yang ada dalam famili Rhabdoviridae."],
                     ["Penanganan: \n"
                      "Saat ini metode yang secara pasti dapat mengatasi rabies yang telah menimbulkan gejala belum ada. \n"
                      "Namun, penanganan rabies sudah dilakukan sejak hewan tergigit hewan penular yang diduga membawa virus rabies dan belum ada gejala yang muncul. \n"
                      "Untuk penanganan dapat dilakukan dengan pemberian imunogulobin yang berupa serum atau vaksin anti rabies. \n"
                      "Pemberian serum atau vaksin ini bertujuan untuk membantu tubuh dalam melawan virus penyebab infeksi pada otak dan sistem saraf."],
                     ["Pencegahan: \n"
                      "Memberi vaksinasi rabies pada kucing."])

    else:
        deskripsi = (["Scabies merupakan salah satu penyakit yang menyerang kulit dan disebabkan oleh Sarcoptes scabei. \n"
                      "Sarcoptes scabiei merupakan salah satu ektoparasit yang biasa menyerang kucing. Tungau ini hidup pada kulit dengan membuat terowongan pada stratum corneum dan melangsungkan hidupnya pada tempat tersebut. \n"
                      "Penyakit skabies dapat ditularkan melalui kontak langsung dengan hewan lain yang terkena skabies atau dengan adanya sumber tungau skabies di wilayah tempat tinggal kucing. \n"
                      "Hewan terserang mengalami penurunan kondisi tubuh, menimbulkan dampak negatif bagi pemelihara dan lingkungan."],
                     ["Penanganan: \n"
                      "Mencuci segera benda-benda yang berkaitan dengan kucing, Mengkarentina kucing yang terkena scabies. \n"
                      "Mengolesi salep pada tubuh kucing, Memberikan shampoo anti tungau Disuntik anti scabies."],
                     ["Pencegahan: \n"
                      "Jangan terlalu sering dimandikan, Sisir dengan sisir bergerigi halus, Bersihkan kandang, Hindari kucing dari cuaca ekstrim, Hindari kucing dehidrasi, Lakukan Desinfektan rutin, Suntik anti scabies."])
    return deskripsi


def diagnosa(jenis):
    penyakit_asli = (
        ['Bordetollosis'], ['Cacingan'], ['Calici Virus'],
        ['Ear Mites'], ['Feline Panleukopenia'], [
            'Feline Viral Rhinotracheitis'], ['FLUDT'],
        ['Hepatitis'], ['Jamur'], ['Pyometra'], ['Rabies'], ['Scabies'])
    return penyakit_asli[jenis][0]


def proses(pesan):
    # create stemmer
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    # Create factory
    stop_factory = StopWordRemoverFactory()

    stopword = stop_factory.create_stop_word_remover()
    sentence = (stopword.remove(pesan))

    # stem
    pesan = str(pesan)
    pesan = stemmer.stem(pesan)

    penyakit = (['demam'], ['tidak nafsu makan'], ['lesu'], ['bersin'], ['ingus meler'], ['mata rusak'], ['gangguan pernafasan'], ['diare'], ['bulu rontok'], ['warna gusi abnormal'], ['sariawan'], ['cacing kotoran'], ['gatal'], ['gangguan telinga'], ['muntah'], ['dehidrasi'], ['batuk'], [
                'air liur'], ['perut besar'], ['kurus'], ['gelisah'], ['gangguan air kecil'], ['sering minum'], ['kehausan'], ['kerak'], ['bentol merah'], ['cairan bau'], ['agresif'], ['suka menggigit'], ['takut cahaya dan air'], ['pilek'], ['darah dalam urine'], ['pendarahan'], ['luka berkusta'], ['panas'])

    pesan_array = pesan.split()

    for x in range(len(pesan_array)):
        # print(gejala_penyakit)
        print(pesan_array[x])
        if pesan_array[x] in str(penyakit):
            print('ada dong')
            uji = []
            jumlah_bobot = 0
            for x in range(penyakit.__len__()):
                bobot = NGram.compare(penyakit[x][0], pesan, N=3)
                if bobot > 0.0:
                    bobot = 1
                    jumlah_bobot += 1

                else:
                    bobot = 0
                uji.append(bobot)
            if (jumlah_bobot == 0):
                return 0

            latih = (
                [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0,
                    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                    1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0,
                    0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                    1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                    0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1])
            hasil2 = []
            for t in range(latih.__len__()):
                a = ((uji[0] - latih[t][0]) ** 2) + ((uji[1] - latih[t][1]) ** 2) + ((uji[2] - latih[t][2]) ** 2) + (
                    (uji[3] - latih[t][3]) ** 2) + ((uji[4] - latih[t][4]) ** 2) + (
                    (uji[5] - latih[t][5]) ** 2) + ((uji[6] - latih[t][6]) ** 2) + (
                    (uji[7] - latih[t][7]) ** 2) + ((uji[8] - latih[t][8]) ** 2) + (
                    (uji[9] - latih[t][9]) ** 2) + ((uji[10] - latih[t][10]) ** 2) + (
                    (uji[11] - latih[t][11]) ** 2) + ((uji[12] - latih[t][12]) ** 2) + (
                    (uji[13] - latih[t][13]) ** 2) + ((uji[14] - latih[t][14]) ** 2) + (
                    (uji[15] - latih[t][15]) ** 2) + ((uji[16] - latih[t][16]) ** 2) + (
                    (uji[17] - latih[t][17]) ** 2) + ((uji[18] - latih[t][18]) ** 2) + (
                    (uji[19] - latih[t][19]) ** 2) + ((uji[20] - latih[t][20]) ** 2) + (
                    (uji[21] - latih[t][21]) ** 2) + ((uji[22] - latih[t][22]) ** 2) + (
                    (uji[23] - latih[t][23]) ** 2) + ((uji[24] - latih[t][24]) ** 2) + (
                    (uji[25] - latih[t][25]) ** 2) + ((uji[26] - latih[t][26]) ** 2) + (
                    (uji[27] - latih[t][27]) ** 2) + ((uji[28] - latih[t][28]) ** 2) + (
                    (uji[29] - latih[t][29]) ** 2) + ((uji[30] - latih[t][30]) ** 2) + (
                    (uji[31] - latih[t][31]) ** 2)

                hasil2.append(a)
            hasil2 = numpy.array(hasil2)
            hasil2 = numpy.array(numpy.where(hasil2 == hasil2.min()))
            return (hasil2)
        else:
            print(penyakit)
            print('gejala tidak ada')
