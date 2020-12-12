
#   __   __   __   ______   ______   __   __       ______   ______   __    __   ______   ______   ______    
#  /\ \ /\ "-.\ \ /\  ___\ /\  __ \ /\ "-.\ \     /\  __ \ /\  ___\ /\ "-./  \ /\  __ \ /\  ___\ /\  __ \   
#  \ \ \\ \ \-.  \\ \___  \\ \  __ \\ \ \-.  \    \ \  __ \\ \___  \\ \ \-./\ \\ \  __ \\ \ \____\ \  __ \  
#   \ \_\\ \_\\"\_\\/\_____\\ \_\ \_\\ \_\\"\_\    \ \_\ \_\\/\_____\\ \_\ \ \_\\ \_\ \_\\ \_____\\ \_\ \_\ 
#    \/_/ \/_/ \/_/ \/_____/ \/_/\/_/ \/_/ \/_/     \/_/\/_/ \/_____/ \/_/  \/_/ \/_/\/_/ \/_____/ \/_/\/_/ 
#                                                                                                           

# Problem Set 2, insan_asmaca.py
# İsim: -
# Katkıda bulunanlar: Nazlıcan Kurt, Onur Ekim, Ahmed Al-murtadha, Ozan Dalgalı
# Harcanan Zaman: 14 saat

# İnsan Asmaca Oyunu

# -----------------------------------

import random
import string
import pandas as pd 

KELIME_LISTESI_DOSYASI = "tdk_sozcukler2.csv"
TÜRKÇE_ALFABE = 'abcçdefgğhıijklmnoöprsştuüvyz'
insanCizim = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']


def kelimeleri_yükle():
    print("Dosyadan kelime listesi okunuyor...")
    dosya = pd.read_csv("tdk_sozcukler2.csv")
    dosya['SOZCUKLER'] = dosya['SOZCUKLER'].str.lower() 
    kelime_listesi = dosya['SOZCUKLER'].tolist()
    print(f"{len(kelime_listesi)} kelimelik liste hazırlandı.")
    return kelime_listesi

def kelime_seç(kelime_listesi):
    return random.choice(kelime_listesi)

# -----------------------------------

kelime_listesi = kelimeleri_yükle()
gizli_kelime = kelime_seç(kelime_listesi)

def kelime_tahmin_edildi_mi(gizli_kelime, tahmin_edilen_harfler):
    acilanKelime = tahmin_edilen_kelimeyi_al(gizli_kelime, tahmin_edilen_harfler)
    if "_" not in acilanKelime: # tahmin_edilen_kelime'de kapalı harf (_) kalmadıysa kelime bulunmuştur
        return True
    return False

def tahmin_edilen_kelimeyi_al(gizli_kelime, tahmin_edilen_harfler):
    liste, u, st = [], 0, ""
    while u < len(gizli_kelime):
        liste.append("_ ")
        u += 1 
    for a in range(len(gizli_kelime)):
        for i in range(len(tahmin_edilen_harfler)):
            if tahmin_edilen_harfler[i] in gizli_kelime[a]: 
                liste[a] = gizli_kelime[a]
    return st.join(liste)

def uygun_harfleri_al(tahmin_edilen_harfler, alfabe = TÜRKÇE_ALFABE):
    yeniAlfabe = alfabe.replace(tahmin_edilen_harfler[0], "")
    for p in range(1, len(tahmin_edilen_harfler)):
        yeniAlfabe = yeniAlfabe.replace(tahmin_edilen_harfler[p], "")
    return yeniAlfabe

def uyar(kalan_uyarılar):
	kalan_uyarılar -= 1
	if kalan_uyarılar < 0: # kalan_uyarılar negatife düştüğünde 0 döndür, negatife geçmesine izin verme
		return 0          
	return kalan_uyarılar

def boşluklarla_eşleştir(benim_kelimem, diğer_kelime):
    benim_kelimem_ilk = benim_kelimem.replace(" ", "")
    # kelimemizin(benim) uzunluğunu değişkene kaydettik
    length = len(benim_kelimem_ilk)
    # Daha sonra karşılaştırmak için kelime harflerinin listesini oluşturun
    kelimemin_harfleri = list(benim_kelimem_ilk)
    # sözcük uzunlukları eşitse kelimeleri karşılaştırmaya devam ediyoruz
    # her iki karakter de aynıysa, diğer konumları kontrol etmek için döngüye devam ediyoruz
    if len(diğer_kelime) == length:
      for i in range(length):
          if benim_kelimem_ilk[i] == diğer_kelime[i]:
            continue
          elif benim_kelimem_ilk[i] == "_" and diğer_kelime[i] not in kelimemin_harfleri:
            continue
          else:
            return False
      return True
    else: 
      return False

def olası_eşleşmeleri_göster(benim_kelimem):
    olası_eşleşmeler =  ""
    for diğer_kelime in kelime_listesi:
        if boşluklarla_eşleştir(benim_kelimem, diğer_kelime):
          olası_eşleşmeler += (diğer_kelime + " ")
        else:
          continue
    if olası_eşleşmeler == "":
        print("\nEşleşme bulunamadı!")
    else:
        print(olası_eşleşmeler)

def giriş(seçim):
    print("\nİnsan asmaca oyununa hoşgeldiniz!")
    while seçim != "1" and seçim != "2":
        seçim = input("\nOyun modunu seçiniz:\n 1. Klasik\n 2. İpuçları ile\n\nSeçiminiz: ")
    if seçim == "2":
        print("\nİpuçlu adam asmacaya hoşgeldiniz.\nİpucu alabilmek için gizli kelimenin harflerinin bir kısmını açmış olmanız gerekiyor.\nİpucu almak için (*) harfini kullanın.\nİyi şanslar!\n")
        return True
    return False
    
def benzersizHarfler(gizli_kelime):
    benzersizHarfler = []
    for m in range(0, len(gizli_kelime)): # gizli_kelime boyunca m yi say
        if gizli_kelime[m] not in benzersizHarfler: # gizli_kelime deki mevcut harf benzersizHarfler listesinde değilse ekle
            benzersizHarfler.append(gizli_kelime[m])
        else: # listede zaten bulunuyorsa eklemeden bir sonraki harfe geç
            continue
    return benzersizHarfler

def ipucuVerilebilir(mevcut_kelime):
    mevcut_kelimem = mevcut_kelime.replace(" ", "")
    if (len(mevcut_kelimem) / mevcut_kelimem.count("_")) >= 1.5: # kelime uzunluğunun kapalı harf sayısına bölümü 1.5 den büyükse ipucu verilebilir
        return True
    return False

def insan_asmaca(gizli_kelime, alfabe = TÜRKÇE_ALFABE):
    kalan_tahminler, kalan_uyarılar, unluler =  6, 3, ["a","e","ı","i","o","ö","u","ü"]
    tahmin_edilen_harfler, kelime_uzunluk, ipuçlu, seçim = [], len(gizli_kelime), False, 0
    ipuçlu = giriş(seçim)
    print(f"{kelime_uzunluk} harfli bir kelime düşünüyorum.")
    while kalan_tahminler > 0 and not kelime_tahmin_edildi_mi(gizli_kelime,tahmin_edilen_harfler) :
        print(f"\nKalan tahmin hakkınız: {kalan_tahminler} \nKalan hata hakkınız:   {kalan_uyarılar}\n" + insanCizim[-kalan_tahminler-1] + "\n")
        print(f"Uygun harfler: {alfabe}\nMevcut kelime: {tahmin_edilen_kelimeyi_al(gizli_kelime,tahmin_edilen_harfler)} ({len(gizli_kelime)} harfli)")
        mevcut_kelime = tahmin_edilen_kelimeyi_al(gizli_kelime,tahmin_edilen_harfler)
        girdi = input("Bir harf tahmin edin: ").casefold()
        print("-" * 45)
        if girdi in alfabe and not girdi == "": # girdi alfabe elemanı ise ve girdi boş girilmediyse, girdi == "" kontrolü yapılmazsa doğrudan kazandınız mesajı yazdırılıyor
            tahmin_edilen_harfler.append(girdi) # tahmin_edilen_harfler listesine girdi'yi ekle
            alfabe = uygun_harfleri_al(tahmin_edilen_harfler,alfabe) # alfabe'yi fonksiyondan dönen harf eksiltilmiş alfabe haline getir
            if girdi in gizli_kelime: # eğer girdi alfabe elemanı ve gizli kelimede buluyorsa
                print("\nGüzel tahmin! :" , tahmin_edilen_kelimeyi_al(gizli_kelime,tahmin_edilen_harfler))
            else: # eğer girdi alfabe elemanı ama gizli_kelimede bulunmuyorsa
                if girdi in unluler: # unluler listesinde bulunuyorsa 2 tahmin eksilt
                    kalan_tahminler -= 2
                else: # unluler listesinde degilse 1 tahmin eksilt
                    kalan_tahminler -=1
                print("Oops! Bu harf benim kelimemde yok: ", mevcut_kelime)
        elif girdi in tahmin_edilen_harfler: # girdi tahmin_edilen_harfler içerisinde ise puan düşürmeden uyarı göster
                print(f"{girdi} harfini zaten tahmin ettiniz: ",  mevcut_kelime)
        elif ipuçlu == True and girdi == "*":
            if ipucuVerilebilir(mevcut_kelime):
                print("İpuçları: ")
                olası_eşleşmeleri_göster(mevcut_kelime)
            else:
                print("İpucu alabilmek için kelimede daha fazla harf bulmalısın.\n")
        else: # eğer girdi alfabe elemanı değilse kalan_uyarıları 1 azalt
            if kalan_uyarılar == 0: # kalan_uyarılar bittiğinde her hatada tahminlerden azaltmaya başla
                kalan_tahminler -= 1   
            else: # kalan_uyarılar bitmediyse kalan_uyarı sayısıyla beraber kullanıcıyı uyar
                print("\nYalnızca bir alfabe harfi giriniz!")
            kalan_uyarılar = uyar(kalan_uyarılar) # burada fonksiyon olmasının sebebi hatayı azaltarak devam ettikçe 3 hatadan sonra -1 hatanız kaldı gibi bir çıktı veriyordu
    if kelime_tahmin_edildi_mi(gizli_kelime,tahmin_edilen_harfler): # kelime_tahmin_edildi fonksiyonu True döndürdüğünde 
        print("\nTebrikler! Kazandınız. ") # tebrik mesajını yazdır
        print("Bu oyun için toplam puanınız: ", len(benzersizHarfler(gizli_kelime)) * kalan_tahminler) # puan fonksiyonu ile puan hesapla ve yazdır
        return # insan_asmaca fonksiyonunu sonlandırıp programdan çık
    print(f"{insanCizim[6]}\n\nKaybettiniz :( Bulmaya çalıştığınız kelime: {gizli_kelime}\n") # kelime_tahmin_edildi True dönmediyse kaybedildiğini yazdır
    return #programdan çık

if __name__ == "__main__":
        gizli_kelime = kelime_seç(kelime_listesi)
        insan_asmaca(gizli_kelime, alfabe=TÜRKÇE_ALFABE)