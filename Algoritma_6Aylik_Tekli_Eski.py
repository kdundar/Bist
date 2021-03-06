import xlrd
import xlwt
from xlutils.copy import copy
import os.path

from Algoritma_old_1 import faaliyetKariRow

varBilancoDosyasi = ("D:\\bist\\bilancolar\\UZERB.xlsx")
varBilancoDonemi = 202006
varBondYield = 0.1022
varHisseFiyati = 4.48

reportFile = "D:\\bist\\Report_2020_06_6Ayliklar.xls"

def runAlgoritma(bilancoDosyasi, bilancoDonemi, bondYield, hisseFiyati):
    def birOncekiBilancoDoneminiHesapla(dnm):
        yil = int(dnm / 100)
        ceyrek = int(dnm % 100)

        if ceyrek == 6:
            return (yil - 1) * 100 + 12
        else:
            return yil * 100 + 6

    birOncekiBilancoDonemi = birOncekiBilancoDoneminiHesapla(bilancoDonemi)
    print("Bir Onceki Bilanco Donemi:", birOncekiBilancoDonemi)

    ikiOncekiBilancoDonemi = birOncekiBilancoDoneminiHesapla(birOncekiBilancoDonemi)
    print("Iki Onceki Bilanco Donemi:", ikiOncekiBilancoDonemi)

    ucOncekiBilancoDonemi = birOncekiBilancoDoneminiHesapla(ikiOncekiBilancoDonemi)
    print("Uc Onceki Bilanco Donemi:", ucOncekiBilancoDonemi)

    dortOncekiBilancoDonemi = birOncekiBilancoDoneminiHesapla(ucOncekiBilancoDonemi)
    print("Dort Onceki Bilanco Donemi:", dortOncekiBilancoDonemi)

    wb = xlrd.open_workbook(bilancoDosyasi)
    sheet = wb.sheet_by_index(0)

    def donemColumnFind(col):
        for columni in range(sheet.ncols):
            cell = sheet.cell(0, columni)
            if cell.value == col:
                return columni
        print("Uygun Ceyrek Bulunamadi!!!")
        return -1

    bilancoDonemiColumn = donemColumnFind(bilancoDonemi)
    birOncekibilancoDonemiColumn = donemColumnFind(birOncekiBilancoDonemi)
    ikiOncekibilancoDonemiColumn = donemColumnFind(ikiOncekiBilancoDonemi)
    ucOncekibilancoDonemiColumn = donemColumnFind(ucOncekiBilancoDonemi)
    dortOncekibilancoDonemiColumn = donemColumnFind(dortOncekiBilancoDonemi)

    def getBilancoDegeri(label, column):
        for rowi in range(sheet.nrows):
            cell = sheet.cell(rowi, 0)
            if cell.value == label:
                if sheet.cell_value(rowi, column)=="":
                    print ("Bilanço alanı boş!")
                    return 0
                else:
                    return sheet.cell_value(rowi, column)
        print("Uygun bilanco degeri bulunamadi:", label)
        return 0


    def getBilancoTitleRow(title):
        for rowi in range(sheet.nrows):
            cell = sheet.cell(rowi, 0)
            if cell.value == title:
                return rowi
        print("Uygun baslik bulunamadi!")
        return -1

    hasilatRow = getBilancoTitleRow("Hasılat")
    faaliyetKariRow = getBilancoTitleRow("ESAS FAALİYET KARI (ZARARI)");
    netKarRow = getBilancoTitleRow("Net Dönem Karı veya Zararı");

    def altiAyDegeriHesapla(r, c):
        quarter = (sheet.cell_value(0, c)) % (100)
        if (quarter == 6):
            return sheet.cell_value(r, c)
        else:
            return (sheet.cell_value(r, c) - sheet.cell_value(r, (c - 1)))

    def oncekiYilAyniAltiAyDegisimiHesapla(row, donem):
        donemColumn = donemColumnFind(donem)
        #print ("DonemColumn:", donemColumn)
        oncekiYilAyniDonemColumn = donemColumnFind(donem - 100)
        #print("Onceki Yıl Aynı DonemColumn:", oncekiYilAyniDonemColumn)
        #print("Row:",row, "Column:", donemColumn)
        ceyrekDegeri = altiAyDegeriHesapla(row, donemColumn)
        #print("Çeyrek Değeri:", ceyrekDegeri)
        oncekiCeyrekDegeri = altiAyDegeriHesapla(row, oncekiYilAyniDonemColumn)
        #print ("Önceki Çeyrek Değeri:", oncekiCeyrekDegeri)
        degisimSonucu = ceyrekDegeri / oncekiCeyrekDegeri - 1
        print(int(sheet.cell_value(0, donemColumn)), sheet.cell_value(row, 0), int(ceyrekDegeri))
        print(int(sheet.cell_value(0, oncekiYilAyniDonemColumn)), sheet.cell_value(row, 0), int(oncekiCeyrekDegeri))
        return degisimSonucu

    # def yilCeyrekAyir (a):
    #     yil = int (a/100)
    #     ceyrek = int (a % 100)
    #     return (yil, ceyrek)
    #
    # hesaplanacakYil, hesaplanacakCeyrek = yilCeyrekAyir(hesaplanacakDonem)
    # print ("Hesaplanacak Yıl:", hesaplanacakYil, "Hesaplanacak Çeyrek:", hesaplanacakCeyrek)
    #
    #
    # def yilCeyrekBirlestir (yil, ceyrek):
    #     return 100*yil + ceyrek

    def likidasyonDegeriHesapla(ceyrek):
        nakit = getBilancoDegeri("Nakit ve Nakit Benzerleri", bilancoDonemiColumn)
        alacaklar = getBilancoDegeri("Ticari Alacaklar", bilancoDonemiColumn) + getBilancoDegeri("Diğer Alacaklar",
                                                                                                 bilancoDonemiColumn) + getBilancoDegeri(
            "Ticari Alacaklar1", bilancoDonemiColumn)
        stoklar = getBilancoDegeri("Stoklar", bilancoDonemiColumn)
        digerVarliklar = getBilancoDegeri("Diğer Dönen Varlıklar", bilancoDonemiColumn)
        finansalVarliklar = getBilancoDegeri("Finansal Yatırımlar", bilancoDonemiColumn) + getBilancoDegeri(
            "Finansal Yatırımlar1", bilancoDonemiColumn) + getBilancoDegeri("Özkaynak Yöntemiyle Değerlenen Yatırımlar",
                                                                            bilancoDonemiColumn)
        maddiDuranVarliklar = getBilancoDegeri("Maddi Duran Varlıklar", bilancoDonemiColumn)


        likidasyonDegeri = nakit + (alacaklar * 0.7) + (stoklar * 0.5) + (digerVarliklar * 0.7) + (
                    finansalVarliklar * 0.7) + (maddiDuranVarliklar * 0.2)

        return likidasyonDegeri

    # 1.kriter hesabi
    print("---------------------------------------------------------------------------------")
    print("1.Kriter: Satış gelirleri bir önceki yılın aynı dönemine göre en az %10 artmalı")

    kriter1SatisGelirArtisi = oncekiYilAyniAltiAyDegisimiHesapla(hasilatRow, bilancoDonemi)
    kriter1GecmeDurumu = (kriter1SatisGelirArtisi > 0.1)
    print("Kriter1: Satis Geliri Artisi:", "{:.2%}".format(kriter1SatisGelirArtisi), "> 10%" , kriter1GecmeDurumu)

    # 2.kriter hesabi
    print("---------------------------------------------------------------------------------")
    print("2.Kriter: Son ceyrek faaliyet kari onceki yil ayni ceyrege göre en az %15 fazla olacak")

    if altiAyDegeriHesapla(netKarRow,bilancoDonemiColumn)<0:
        kriter2FaaliyetKariArtisi = oncekiYilAyniAltiAyDegisimiHesapla(faaliyetKariRow, bilancoDonemi)
        kriter2GecmeDurumu = False
        print("Kriter2: Faaliyet Kari Artisi:", kriter2GecmeDurumu, "Son Ceyrek Net Kar Negatif")

    elif altiAyDegeriHesapla(faaliyetKariRow,bilancoDonemiColumn)<0:
        kriter2FaaliyetKariArtisi = oncekiYilAyniAltiAyDegisimiHesapla(faaliyetKariRow, bilancoDonemi)
        kriter2GecmeDurumu = False
        print("Kriter2: Faaliyet Kari Artisi:", kriter2GecmeDurumu, "Son Ceyrek Faaliyet Kari Negatif")

    else:
        kriter2FaaliyetKariArtisi = oncekiYilAyniAltiAyDegisimiHesapla(faaliyetKariRow, bilancoDonemi)
        kriter2GecmeDurumu = (kriter2FaaliyetKariArtisi > 0.15)
        print("Kriter2: Faaliyet Kari Artisi:", "{:.2%}".format(kriter2FaaliyetKariArtisi), "> 15%", kriter2GecmeDurumu)


    # 3.kriter hesabı
    print("---------------------------------------------------------------------------------")
    print("3.Kriter: Bir önceki çeyrekteki satış artış yüzdesi cari dönemden düşük olmalı")


    if kriter1SatisGelirArtisi >= 1:
        kriter3OncekiCeyrekArtisi = oncekiYilAyniAltiAyDegisimiHesapla(hasilatRow, birOncekiBilancoDonemi)
        kriter3GecmeDurumu = True
        print("Kriter3: Onceki Ceyrek Satis Geliri Artisi %100'ün Üzerinde, Karşılaştırma Yapılmayacak!:", "{:.2%}".format(kriter3OncekiCeyrekArtisi), "<",
              "{:.2%}".format(kriter1SatisGelirArtisi), kriter3GecmeDurumu)

    else:
        kriter3OncekiCeyrekArtisi = oncekiYilAyniAltiAyDegisimiHesapla(hasilatRow, birOncekiBilancoDonemi)
        kriter3GecmeDurumu = (kriter3OncekiCeyrekArtisi < kriter1SatisGelirArtisi)
        print("Kriter3: Onceki Ceyrek Satis Geliri Artisi:", "{:.2%}".format(kriter3OncekiCeyrekArtisi),"<","{:.2%}".format(kriter1SatisGelirArtisi), kriter3GecmeDurumu)


    # 4.kriter hesabi
    print("---------------------------------------------------------------------------------")
    print("4.Kriter: Bir önceki çeyrekteki faaliyet karı artış yüzdesi cari dönemden düşük olmalı")

    if kriter2FaaliyetKariArtisi >= 1:
        kriter4OncekiCeyrekFaaliyetKariArtisi = oncekiYilAyniAltiAyDegisimiHesapla(faaliyetKariRow,
                                                                                   birOncekiBilancoDonemi)
        kriter4GecmeDurumu = True
        print("Kriter4: Onceki Ceyrek Faaliyet Kari Artisi %100'ün Üzerinde, Karşılaştırma Yapılmayacak:", "{:.2%}".format(kriter4OncekiCeyrekFaaliyetKariArtisi),
              "<", "{:.2%}".format(kriter2FaaliyetKariArtisi), kriter4GecmeDurumu)

    else:
        kriter4OncekiCeyrekFaaliyetKariArtisi = oncekiYilAyniAltiAyDegisimiHesapla(faaliyetKariRow, birOncekiBilancoDonemi)
        kriter4GecmeDurumu = (kriter4OncekiCeyrekFaaliyetKariArtisi < kriter2FaaliyetKariArtisi)
        print("Kriter4: Onceki Yila Gore Faaliyet Kari Artisi:", "{:.2%}".format(kriter4OncekiCeyrekFaaliyetKariArtisi),
          "<" , "{:.2%}".format(kriter2FaaliyetKariArtisi) , kriter4GecmeDurumu)


    # Gercek Deger Hesapla
    print("----------------Gercek Deger Hesabi-----------------------------------------------------------------")

    sermaye = getBilancoDegeri("Ödenmiş Sermaye", bilancoDonemiColumn)
    print("Sermaye:", sermaye)

    anaOrtaklikPayi = getBilancoDegeri("Ana Ortaklık Payları", bilancoDonemiColumn) / getBilancoDegeri(
        "DÖNEM KARI (ZARARI)", bilancoDonemiColumn)
    print("Ana Ortaklık Payı:", anaOrtaklikPayi)

    sonCeyrekSatisArtisYuzdesi = oncekiYilAyniAltiAyDegisimiHesapla(hasilatRow, bilancoDonemi)
    birOncekiCeyrekSatisArtisYuzdesi = oncekiYilAyniAltiAyDegisimiHesapla(hasilatRow, birOncekiBilancoDonemi)

    birOncekiBilancoDonemiSatis = altiAyDegeriHesapla(hasilatRow, birOncekibilancoDonemiColumn)
    bilancoDonemiSatis = altiAyDegeriHesapla(hasilatRow, bilancoDonemiColumn)

    sonDortCeyrekSatisToplami = birOncekiBilancoDonemiSatis + bilancoDonemiSatis
    print("Son Yıl satış toplamı:", sonDortCeyrekSatisToplami)

    onumuzdekiDortCeyrekSatisTahmini = (
                (((sonCeyrekSatisArtisYuzdesi + birOncekiCeyrekSatisArtisYuzdesi) / 2) + 1) * sonDortCeyrekSatisToplami)
    print("Önümüzdeki Yıl satış tahmini:", onumuzdekiDortCeyrekSatisTahmini)

    birOncekiBilancoDonemiFaaliyetKari = altiAyDegeriHesapla(faaliyetKariRow, birOncekibilancoDonemiColumn)
    bilancoDonemiFaaliyetKari = altiAyDegeriHesapla(faaliyetKariRow, bilancoDonemiColumn)

    onumuzdekiDortCeyrekFaaliyetKarMarjiTahmini = (birOncekiBilancoDonemiFaaliyetKari + bilancoDonemiFaaliyetKari) / (
                bilancoDonemiSatis + birOncekiBilancoDonemiSatis)
    print("Önümüzdeki yıl faaliyet kar marjı tahmini:",
          "{:.2%}".format(onumuzdekiDortCeyrekFaaliyetKarMarjiTahmini))

    faaliyetKariTahmini = onumuzdekiDortCeyrekSatisTahmini * onumuzdekiDortCeyrekFaaliyetKarMarjiTahmini
    print("Faaliyet Kar Tahmini:", faaliyetKariTahmini)

    ortalamaFaaliyetKariTahmini = faaliyetKariTahmini

    print("Ortalama Faaliyet Kari Tahmini:", ortalamaFaaliyetKariTahmini)

    hisseBasinaOrtalamaKarTahmini = (ortalamaFaaliyetKariTahmini * anaOrtaklikPayi) / sermaye
    print("Hisse başına ortalama kar tahmini:", format(hisseBasinaOrtalamaKarTahmini, ".2f"))

    likidasyonDegeri = likidasyonDegeriHesapla(bilancoDonemi)
    print("Likidasyon değeri:", likidasyonDegeri)

    borclar = int(getBilancoDegeri("TOPLAM YÜKÜMLÜLÜKLER", bilancoDonemiColumn))
    print("Borçlar:", format(borclar, ",").replace(',', '.'))

    bilancoEtkisi = (likidasyonDegeri - borclar) / sermaye * anaOrtaklikPayi
    print("Bilanço Etkisi:", format(bilancoEtkisi, ".2f"))

    gercekDeger = (hisseBasinaOrtalamaKarTahmini * 7) + bilancoEtkisi
    print("Gerçek hisse değeri:", format(gercekDeger, ".2f"))

    targetBuy = gercekDeger * 0.66
    print("Target buy:", format(targetBuy, ".2f"))

    print("Bilanço tarihindeki hisse fiyatı:", format(varHisseFiyati, ".2f"))

    gercekFiyataUzaklik = hisseFiyati / targetBuy
    print("Gerçek fiyata uzaklık:", "{:.2%}".format(gercekFiyataUzaklik))

    # Netpro Hesapla
    print("----------------NetPro Kriteri-----------------------------------------------------------------")

    sonDortDonemFaaliyetKariToplami = bilancoDonemiFaaliyetKari + birOncekiBilancoDonemiFaaliyetKari

    birOncekiBilancoDonemiNetKari = altiAyDegeriHesapla(netKarRow, birOncekibilancoDonemiColumn)
    bilancoDonemiNetKari = altiAyDegeriHesapla(netKarRow, bilancoDonemiColumn)
    sonDortDonemNetKar = bilancoDonemiNetKari + birOncekiBilancoDonemiNetKari

    netProEstDegeri = ((
                                   ortalamaFaaliyetKariTahmini / sonDortDonemFaaliyetKariToplami) * sonDortDonemNetKar) * anaOrtaklikPayi
    print("NetPro Est Değeri:", netProEstDegeri)

    piyasaDegeri = (bilancoEtkisi * sermaye * -1) + (hisseFiyati * sermaye)

    netProKriteri = (netProEstDegeri / piyasaDegeri) / bondYield
    netProKriteriGecmeDurumu = (netProKriteri > 2)
    print("NetPro Kriteri:", format(netProKriteri, ".2f"), netProKriteriGecmeDurumu)

    # Forward PE Hesapla
    print("----------------Forward PE Kriteri-----------------------------------------------------------------")

    forwardPeKriteri = (piyasaDegeri) / netProEstDegeri

    forwardPeKriteriGecmeDurumu = (forwardPeKriteri < 4)
    print("Forward PE Kriteri:", format(forwardPeKriteri, ".2f"), forwardPeKriteriGecmeDurumu)

    def exportReportExcel(hisse, b):

        def createTopRow():
            bookSheetWrite.write(0, 0, "Hisse Adı")
            bookSheetWrite.write(0, 1, "Son Çeyrek Hasılat")
            bookSheetWrite.write(0, 2, "Önceki Yıl Aynı Çeyrek Hasılat")
            bookSheetWrite.write(0, 3, "Hasılat Artışı")
            bookSheetWrite.write(0, 4, "Bir Önceki Çeyrek Hasılat Artışı")
            bookSheetWrite.write(0, 5, "Kriter1")
            bookSheetWrite.write(0, 6, "Kriter3")
            bookSheetWrite.write(0, 7, "Son Çeyrek Faaliyet Karı")
            bookSheetWrite.write(0, 8, "Önceki Yıl Aynı Çeyrek Faaliyet Karı")
            bookSheetWrite.write(0, 9, "Faaliyet Karı Artışı")
            bookSheetWrite.write(0, 10, "Bir Önceki Çeyrek Faaliyet Karı Artışı")
            bookSheetWrite.write(0, 11, "Kriter2")
            bookSheetWrite.write(0, 12, "Kriter4")
            bookSheetWrite.write(0, 13, "Sermaye")
            bookSheetWrite.write(0, 14, "Ana Ortaklık Payı")
            bookSheetWrite.write(0, 15, "Son 4 Çeyrek Satış Toplamı")
            bookSheetWrite.write(0, 16, "Önümüzdeki 4 Çeyrek Satış Tahmini")
            bookSheetWrite.write(0, 17, "Önümüzdeki 4 Çeyrek Faaliyet Kar Marjı Tahmini")
            bookSheetWrite.write(0, 18, "Faaliyet Kar Tahmini 1")
            bookSheetWrite.write(0, 19, "Faaliyet Kar Tahmini 2")
            bookSheetWrite.write(0, 20, "Ortalama Faaliyet Kar Tahmini")
            bookSheetWrite.write(0, 21, "Hisse Başına Kar Tahmini")
            bookSheetWrite.write(0, 22, "Bilanço Etkisi")
            bookSheetWrite.write(0, 23, "Bilanço Tarihi Hisse Fiyatı")
            bookSheetWrite.write(0, 24, "Gerçek Hisse Değeri")
            bookSheetWrite.write(0, 25, "Target Buy")
            bookSheetWrite.write(0, 26, "Gerçek Fiyata Uzaklık")
            bookSheetWrite.write(0, 27, "NET Pro")
            bookSheetWrite.write(0, 28, "Forward PE")

        def reportResults(rowNumber):

            bookSheetWrite.write(rowNumber, 0, hisse)
            bookSheetWrite.write(rowNumber, 1, altiAyDegeriHesapla(hasilatRow, bilancoDonemiColumn))
            bookSheetWrite.write(rowNumber, 2, altiAyDegeriHesapla(hasilatRow, ikiOncekibilancoDonemiColumn))
            bookSheetWrite.write(rowNumber, 3, kriter1SatisGelirArtisi)
            bookSheetWrite.write(rowNumber, 4, kriter3OncekiCeyrekArtisi)
            bookSheetWrite.write(rowNumber, 5, kriter1GecmeDurumu)
            bookSheetWrite.write(rowNumber, 6, kriter3GecmeDurumu)
            bookSheetWrite.write(rowNumber, 7, altiAyDegeriHesapla(faaliyetKariRow, bilancoDonemiColumn))
            bookSheetWrite.write(rowNumber, 8, altiAyDegeriHesapla(faaliyetKariRow, ikiOncekibilancoDonemiColumn))
            bookSheetWrite.write(rowNumber, 9, kriter2FaaliyetKariArtisi)
            bookSheetWrite.write(rowNumber, 10, kriter4OncekiCeyrekFaaliyetKariArtisi)
            bookSheetWrite.write(rowNumber, 11, kriter2GecmeDurumu)
            bookSheetWrite.write(rowNumber, 12, kriter4GecmeDurumu)
            bookSheetWrite.write(rowNumber, 13, sermaye)
            bookSheetWrite.write(rowNumber, 14, anaOrtaklikPayi)
            bookSheetWrite.write(rowNumber, 15, sonDortCeyrekSatisToplami)
            bookSheetWrite.write(rowNumber, 16, onumuzdekiDortCeyrekSatisTahmini)
            bookSheetWrite.write(rowNumber, 17, onumuzdekiDortCeyrekFaaliyetKarMarjiTahmini)
            bookSheetWrite.write(rowNumber, 18, faaliyetKariTahmini)
            bookSheetWrite.write(rowNumber, 19, faaliyetKariTahmini)
            bookSheetWrite.write(rowNumber, 20, ortalamaFaaliyetKariTahmini)
            bookSheetWrite.write(rowNumber, 21, hisseBasinaOrtalamaKarTahmini)
            bookSheetWrite.write(rowNumber, 22, bilancoEtkisi)
            bookSheetWrite.write(rowNumber, 23, varHisseFiyati)
            bookSheetWrite.write(rowNumber, 24, gercekDeger)
            bookSheetWrite.write(rowNumber, 25, targetBuy)
            bookSheetWrite.write(rowNumber, 26, gercekFiyataUzaklik)
            bookSheetWrite.write(rowNumber, 27, netProKriteri)
            bookSheetWrite.write(rowNumber, 28, forwardPeKriteri)

        if os.path.isfile(reportFile):
            print("Rapor dosyası var, güncellenecek:", reportFile)
            bookRead = xlrd.open_workbook(reportFile, formatting_info=True)
            sheetRead = bookRead.sheet_by_index(0)
            rowNumber = sheetRead.nrows
            bookWrite = copy(bookRead)
            bookSheetWrite = bookWrite.get_sheet(0)
            reportResults(rowNumber)
            bookWrite.save(reportFile)

        else:
            print("Rapor dosyası yeni oluşturulacak: ", reportFile)
            bookWrite = xlwt.Workbook()
            bookSheetWrite = bookWrite.add_sheet(str(varBilancoDonemi))
            createTopRow()
            reportResults(1)
            bookWrite.save(reportFile)

    hisseAdiTemp = varBilancoDosyasi[19:]
    hisseAdi = hisseAdiTemp[:-5]
    print (hisseAdi)
    exportReportExcel(hisseAdi, reportFile)


runAlgoritma(varBilancoDosyasi, varBilancoDonemi, varBondYield, varHisseFiyati)