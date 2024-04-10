import datetime
import sys
import threading
import keyboard
import pyautogui
import time

import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from arayüz import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.exit_event = threading.Event()
        self.current_thread = None
        self.timer = QTimer(self)

        # Push button'a tıklanma olayını bağlayalım
        self.ui.basla.clicked.connect(self.start_execution)
        self.ui.durdur.clicked.connect(self.stop)
        self.ui.cikis.clicked.connect(self.close)
        self.ui.tum_kaldir.clicked.connect(self.tumu_kaldir)
        self.ui.tum_sec.clicked.connect(self.tumu_sec)

        # Timer'ın timeout olayını bağlayalım
        self.timer.timeout.connect(self.update_remaining_time)

        keyboard.add_hotkey("F1", self.start_execution)
        keyboard.add_hotkey("F2", self.stop)
        # QLineEdit için doğrulayıcı oluştur
        self.ui.lineEdit.textChanged.connect(self.add_colon)

        self.ui.guncelle.clicked.connect(self.download_files)

    def download_files(self):
        url = "https://github.com/kullanici_adi/proje_adı/archive/main.zip"
        save_path = "update.zip"

        self.progress_bar.setValue(0)  # İndirme başlamadan önce ilerleme çubuğunu sıfırla

        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            with open(save_path, 'wb') as file, \
                 QtWidgets.QProgressDialog("İndiriliyor...", "İptal", 0, total_size, self) as progress:
                progress.setWindowModality(QtCore.Qt.WindowModal)

                for data in response.iter_content(chunk_size=4096):
                    file.write(data)
                    progress.setValue(progress.value() + len(data))

                    if progress.wasCanceled():
                        break

            if not progress.wasCanceled():
                QtWidgets.QMessageBox.information(self, "Bilgi", "Güncelleme tamamlandı.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Hata oluştu: {str(e)}")

    def add_colon(self):
        text = self.ui.lineEdit.text()
        if len(text) == 2:  # İkinci basamakta
            if text[-1] != ':':  # Eğer son karakter : değilse
                self.ui.lineEdit.setText(text + ':')
        elif len(text) > 2:  # İkinci basamaktan sonra gelen karakterlerde
            if text[2] != ':':  # Eğer 3. karakter : değilse
                self.ui.lineEdit.setText(text[:2] + ':' + text[2:4])
        if len(text) > 5:
            self.ui.lineEdit.setText(text[:5])
    def update_remaining_time(self):
        saat_str = self.ui.lineEdit.text()

        current_time = datetime.datetime.now().time()
        current_hour = current_time.hour
        current_minute = current_time.minute

        if not saat_str:  # Eğer lineEdit boşsa devam et
            self.start_task()  # Botu başlat
            return

        saat_list = saat_str.split(":")
        if len(saat_list) == 2:
            try:
                saat = int(saat_list[0])
                dakika = int(saat_list[1])
                if 0 <= saat <= 23 and 0 <= dakika <= 59:
                    if saat < current_hour or (saat == current_hour and dakika <= current_minute):
                        self.show_warning_message("Hata",
                                                  "Geçmiş bir saat dilimi girdiniz. Lütfen ileri bir saat girin.")
                    else:
                        target_time = datetime.time(saat, dakika)
                        delta = datetime.datetime.combine(datetime.date.today(),
                                                          target_time) - datetime.datetime.combine(
                            datetime.date.today(), current_time)
                        remaining_time = delta.total_seconds()
                        hours, remainder = divmod(remaining_time, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        # Kalan süreyi saat, dakika ve saniye olarak göster
                        self.statusBar().showMessage(
                            f"Bot saat {saat:02d}:{dakika:02d}'de başlayacak. Kalan süre: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
                else:
                    self.show_warning_message("Hata", "Lütfen geçerli bir saat ve dakika girin.")
            except ValueError:
                self.show_warning_message("Hata", "Lütfen sayısal değerler girin.")
        else:
            self.show_warning_message("Hata", "Lütfen saat ve dakikayı 'saat:dakika' formatında girin.")
    def show_warning_message(self, title, message):
        self.stop()
        warning_box = QMessageBox(self)
        warning_box.setWindowTitle(title)
        warning_box.setText(message)
        QTimer.singleShot(2000, warning_box.close)  # QMessageBox 2 saniye sonra kapanacak
        warning_box.exec_()
        self.ui.lineEdit.clear()
    def start_execution(self):
        # Checkboxların seçilip seçilmediğini kontrol et
        if not self.ui.zafer_yolu.isChecked() and \
                not self.ui.koruma_arama.isChecked() and \
                not self.ui.koruma_devriye.isChecked() and \
                not self.ui.koruma_muhru.isChecked() and \
                not self.ui.sonsuz_ucurum.isChecked() and \
                not self.ui.titan_tapinagi.isChecked() and \
                not self.ui.seytan_kitasi.isChecked() and \
                not self.ui.deneme_gecidi.isChecked() and \
                not self.ui.kutsal_saray.isChecked() and \
                not self.ui.zaman_kapisi.isChecked() and \
                not self.ui.kurtulus_yolu.isChecked() and \
                not self.ui.intikam_yolu.isChecked() and \
                not self.ui.bolge_kesif.isChecked() and \
                not self.ui.peri_turnuvasi.isChecked() and \
                not self.ui.peri_seferi.isChecked() and \
                not self.ui.gokyuzu_yolu.isChecked() and \
                not self.ui.amfi_tiyatro.isChecked() and \
                not self.ui.birlik_katkisi.isChecked() and \
                not self.ui.birlik_bereketi.isChecked() and \
                not self.ui.birlik_sirri.isChecked() and \
                not self.ui.birlik_hazinesi.isChecked() and \
                not self.ui.peri_adasi.isChecked() and \
                not self.ui.sihirli_konak.isChecked() and \
                not self.ui.yuzey_savasi.isChecked() and \
                not self.ui.ciftlik.isChecked() and \
                not self.ui.labavatuar.isChecked() and \
                not self.ui.ahir.isChecked() and \
                not self.ui.kedi_evi.isChecked() and \
                not self.ui.iskele.isChecked() and \
                not self.ui.cevre_kesif.isChecked() and \
                not self.ui.deneme_kulesi.isChecked() and \
                not self.ui.kara_magarasi.isChecked() and \
                not self.ui.yeralti_labirenti.isChecked():

            self.show_warning_message("Hata", "En az bir görev seçmelisiniz.")
            return

        self.update_remaining_time()
        self.timer.start(1000)
        self.ui.basla.setEnabled(False)
    def start_task(self):
        self.exit_event.clear()
        self.reset_checkbox_background_color()
        self.ui.cikis.setEnabled(False)
        if self.current_thread is None or not self.current_thread.is_alive():
            self.current_thread = threading.Thread(target=self.execute_tasks)
            self.current_thread.start()
    def stop(self):
        self.timer.stop()
        self.statusBar().showMessage("Bot Durduruldu.")
        self.exit_event.set()
        self.reset_checkbox_background_color()
        self.ui.cikis.setEnabled(True)
        self.ui.basla.setEnabled(True)
        if self.current_thread is not None and self.current_thread.is_alive():
            self.current_thread.join()
            self.statusBar().showMessage("Bot Durduruldu.")
    def dur(self):
        self.timer.stop()
        self.exit_event.set()
        self.exit_event.clear()
        self.ui.basla.setEnabled(True)
        self.ui.cikis.setEnabled(True)
        self.statusBar().showMessage("İşlem Bitti.")
    def execute_tasks(self):
        if self.ui.zafer_yolu.isChecked():
            self.statusBar().showMessage("Zafer Yolu Başladı")
            self.zafer_yolu()
            self.set_checkbox_background_color(self.ui.zafer_yolu)

        if self.ui.koruma_arama.isChecked():
            self.statusBar().showMessage("Koruma Arama Başladı")
            self.koruma_arama()
            self.set_checkbox_background_color(self.ui.koruma_arama)

        if self.ui.koruma_devriye.isChecked():
            self.statusBar().showMessage("Koruma Devriye Başladı")
            self.koruma_devriye()
            self.set_checkbox_background_color(self.ui.koruma_devriye)

        if self.ui.koruma_muhru.isChecked():
            self.statusBar().showMessage("Koruma Mührü Başladı")
            self.koruma_muhru()
            self.set_checkbox_background_color(self.ui.koruma_muhru)

        if self.ui.sonsuz_ucurum.isChecked():
            self.statusBar().showMessage("Sonsuz Uçurum Başladı.")
            self.sonsuz_ucurum()
            self.set_checkbox_background_color(self.ui.sonsuz_ucurum)

        if self.ui.titan_tapinagi.isChecked():
            self.statusBar().showMessage("Titan Tapınağı Başladı")
            self.titan_tapinagi()
            self.set_checkbox_background_color(self.ui.titan_tapinagi)

        if self.ui.seytan_kitasi.isChecked():
            self.statusBar().showMessage("Şeytan Kıtası Başladı")
            self.seytan_kitasi()
            self.set_checkbox_background_color(self.ui.seytan_kitasi)

        if self.ui.deneme_gecidi.isChecked():
            self.statusBar().showMessage("Deneme Geçidi Başladı")
            self.deneme_gecidi()
            self.set_checkbox_background_color(self.ui.deneme_gecidi)

        if self.ui.kutsal_saray.isChecked():
            self.statusBar().showMessage("Kutsal Saray Başladı")
            self.kutsal_saray()
            self.set_checkbox_background_color(self.ui.kutsal_saray)

        if self.ui.zaman_kapisi.isChecked():
            self.statusBar().showMessage("Zaman Kapısı Başladı")
            self.zaman_kapisi()
            self.set_checkbox_background_color(self.ui.zaman_kapisi)

        if self.ui.kurtulus_yolu.isChecked():
            self.statusBar().showMessage("Kurtuluş Yolu Başladı")
            self.kurtulus_yolu()
            self.set_checkbox_background_color(self.ui.kurtulus_yolu)

        if self.ui.intikam_yolu.isChecked():
            self.statusBar().showMessage("İntikam Yolu Başladı")
            self.intikam_yolu()
            self.set_checkbox_background_color(self.ui.intikam_yolu)

        if self.ui.bolge_kesif.isChecked():
            self.statusBar().showMessage("Bölge Keşif Başladı")
            self.bolge_kesif()
            self.set_checkbox_background_color(self.ui.bolge_kesif)

        if self.ui.peri_turnuvasi.isChecked():
            self.statusBar().showMessage("Peri Turnuvası Başladı")
            self.peri_turnuvasi()
            self.set_checkbox_background_color(self.ui.peri_turnuvasi)

        if self.ui.gokyuzu_yolu.isChecked():
            self.statusBar().showMessage("Gökyüzü Yolu Başladı")
            self.gokyuzu_yolu()
            self.set_checkbox_background_color(self.ui.gokyuzu_yolu)

        if self.ui.peri_seferi.isChecked():
            self.statusBar().showMessage("Peri Seferi Başladı")
            self.peri_seferi()
            self.set_checkbox_background_color(self.ui.peri_seferi)

        if self.ui.peri_adasi.isChecked():
            self.statusBar().showMessage("Peri Adası Başladı")
            self.peri_adasi()
            self.set_checkbox_background_color(self.ui.peri_adasi)

        if self.ui.birlik_katkisi.isChecked():
            self.statusBar().showMessage("Birlik Katkısı Başladı")
            self.birlik_katkisi()
            self.set_checkbox_background_color(self.ui.birlik_katkisi)

        if self.ui.birlik_bereketi.isChecked():
            self.statusBar().showMessage("Birlik Bereketi Başladı")
            self.birlik_bereketi()
            self.set_checkbox_background_color(self.ui.birlik_bereketi)

        if self.ui.birlik_sirri.isChecked():
            self.statusBar().showMessage("Birlik Sırrı Başladı")
            self.birlik_sirri()
            self.set_checkbox_background_color(self.ui.birlik_bereketi)

        if self.ui.birlik_hazinesi.isChecked():
            self.statusBar().showMessage("Birlik Hazinesi Başladı")
            self.birlik_hazinesi()
            self.set_checkbox_background_color(self.ui.birlik_hazinesi)

        if self.ui.labavatuar.isChecked():
            self.statusBar().showMessage("Laboravatuar Toplama Başladı.")
            self.labavatuar()
            self.set_checkbox_background_color(self.ui.labavatuar)

        if self.ui.yeralti_labirenti.isChecked():
            self.statusBar().showMessage("Yeraltı Labirenti Başladı.")
            self.yeralti_labirenti()
            self.set_checkbox_background_color(self.ui.yeralti_labirenti)

        if self.ui.sihirli_konak.isChecked():
            self.statusBar().showMessage("Sihirli Konak Toplama Başladı.")
            self.sihirli_lokal()
            self.set_checkbox_background_color(self.ui.sihirli_konak)

        if self.ui.yuzey_savasi.isChecked():
            self.statusBar().showMessage("Yüzey Savaşı Başladı.")
            self.yuzey_savasi()
            self.set_checkbox_background_color(self.ui.yuzey_savasi)

        if self.ui.ciftlik.isChecked():
            self.statusBar().showMessage("Çiftlik Toplama Başladı")
            self.ciftlik()
            self.set_checkbox_background_color(self.ui.ciftlik)

        if self.ui.ahir.isChecked():
            self.statusBar().showMessage("Ahır Toplama Başladı.")
            self.ahir()
            self.set_checkbox_background_color(self.ui.ahir)

        if self.ui.kedi_evi.isChecked():
            self.statusBar().showMessage("Kedi Evi Toplama Başladı.")
            self.kedi_evi()
            self.set_checkbox_background_color(self.ui.kedi_evi)

        if self.ui.iskele.isChecked():
            self.statusBar().showMessage("İskele Başladı")
            self.iskele()
            self.set_checkbox_background_color(self.ui.iskele)

        if self.ui.cevre_kesif.isChecked():
            self.statusBar().showMessage("Çevre Keşif Başladı")
            self.cevre_kesif()
            self.set_checkbox_background_color(self.ui.cevre_kesif)

        if self.ui.kara_magarasi.isChecked():
            self.statusBar().showMessage("Kara Mağarası Başladı")
            self.kara_magarasi()
            self.set_checkbox_background_color(self.ui.kara_magarasi)

        if self.ui.amfi_tiyatro.isChecked():
            self.statusBar().showMessage("Amfi Tiyatro Başladı")
            self.amfi_tiyatro()
            self.set_checkbox_background_color(self.ui.amfi_tiyatro)

        tasks_completed = True

        if tasks_completed:
            self.dur()

    def download_files(self):
        url = "https://github.com/kullanici_adi/proje_adı/archive/main.zip"
        save_path = "update.zip"

        self.progress_bar.setValue(0)  # İndirme başlamadan önce ilerleme çubuğunu sıfırla

        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            with open(save_path, 'wb') as file, \
                    QtWidgets.QProgressDialog("İndiriliyor...", "İptal", 0, total_size, self) as progress:
                progress.setWindowModality(QtCore.Qt.WindowModal)

                for data in response.iter_content(chunk_size=4096):
                    file.write(data)
                    progress.setValue(progress.value() + len(data))

                    if progress.wasCanceled():
                        break

            if not progress.wasCanceled():
                QtWidgets.QMessageBox.information(self, "Bilgi", "Güncelleme tamamlandı.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Hata oluştu: {str(e)}")
    def tumu_sec(self):
        for checkbox in self.findChildren(QtWidgets.QCheckBox):
            if not checkbox.isChecked():
                checkbox.setChecked(True)
    def tumu_kaldir(self):
        for checkbox in self.findChildren(QtWidgets.QCheckBox):
            if checkbox.isChecked():
                checkbox.setChecked(False)
                self.reset_checkbox_background_color()
    def set_checkbox_background_color(self, checkbox):
        checkbox.setStyleSheet("QCheckBox { background-color: red; }")
    def reset_checkbox_background_color(self):
        self.ui.deneme_gecidi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.kutsal_saray.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.titan_tapinagi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.seytan_kitasi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.sonsuz_ucurum.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.intikam_yolu.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.zafer_yolu.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.bolge_kesif.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.zaman_kapisi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.peri_turnuvasi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.peri_seferi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.gokyuzu_yolu.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.peri_adasi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.labavatuar.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.yeralti_labirenti.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.sihirli_konak.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.yuzey_savasi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.ciftlik.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.amfi_tiyatro.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.ahir.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.kedi_evi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.cevre_kesif.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.koruma_arama.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.koruma_devriye.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.koruma_muhru.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.kurtulus_yolu.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.birlik_sirri.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.birlik_katkisi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.birlik_bereketi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.birlik_hazinesi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.deneme_kulesi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.kara_magarasi.setStyleSheet("QCheckBox { background-color:; }")
        self.ui.iskele.setStyleSheet("QCheckBox { background-color:; }")
    def click_image(self, image_path, retry=1, confidence=0.9):
        found_any = False  # Herhangi bir konum bulundu mu?
        for _ in range(retry):
            try:
                # Görüntüyü ekranda bul
                location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
                if location is not None:
                    found_any = True
                    # Önceki mouse konumunu al
                    original_position = pyautogui.position()
                    # Görüntünün ortasına tıkla
                    pyautogui.moveTo(location)
                    time.sleep(0.1)
                    pyautogui.click(location)
                    print(f"Tıklanan resim: {image_path}")
                    # Önceki konuma geri dön
                    pyautogui.moveTo(original_position)
            except pyautogui.ImageNotFoundException:
                pass
        return found_any
    def tasima(self,image_path, retry=3, confidence=0.9):
        for _ in range(retry):
            try:
                # Görüntüyü ekranda bul
                location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
                if location[0] != -1:
                    pyautogui.moveTo(location)
                    time.sleep(0.5)
                    print(f"Tıklanan resim: {image_path}")  # Resmin adını yazdır
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            # Görüntü bulunamadıysa belirli bir süre bekleyerek tekrar dene
        return False
    def kara_magarasi(self):
        zaman_hazinesi = False
        grup_sahne = False
        sehir = False
        kurma = False
        ek_sahne = False
        ikinci = False
        kara_magarasi = False
        hemen_basla = False
        ileri1 = False
        ileri2 = False
        ileri3 = False
        geri = False
        geri1 = False
        geri2 = False
        geri3 = False
        geri4 = False
        geri5 = False
        boss = False
        geri_cik = False

        while not self.exit_event.is_set():
            if not sehir:
                if self.click_image("resimler/zafer_yolu/gokyuzu.png"):
                    sehir = True
                    time.sleep(5)
            if not zaman_hazinesi:
                if self.click_image("resimler/kara_magarasi/zaman_hazinesi.png"):
                    zaman_hazinesi = True
                else:
                    if self.click_image("resimler/kara_magarasi/else.png"):
                        pass
            elif not grup_sahne:
                if self.click_image("resimler/kara_magarasi/grup_sahne.png"):
                    grup_sahne = True
            elif not kurma:
                if self.click_image("resimler/kara_magarasi/kurma.png"):
                    kurma = True
            elif not ek_sahne:
                if self.click_image("resimler/kara_magarasi/ek_sahne.png"):
                    ek_sahne = True
            elif not ikinci:
                if self.click_image("resimler/kara_magarasi/ikinci.png"):
                    ikinci = True
            elif not kara_magarasi:
                if self.click_image("resimler/kara_magarasi/kara_magarasi.png"):
                    kara_magarasi = True
                    time.sleep(1)
                if self.click_image("resimler/kara_magarasi/onay.png"):
                    pass
            elif not hemen_basla:
                if self.click_image("resimler/kara_magarasi/hemen_basla.png"):
                    hemen_basla = True
                    time.sleep(2)
                if self.click_image("resimler/birlik_sirri/onay.png"):
                    time.sleep(5)
            elif not ileri1:
                if self.click_image("resimler/kara_magarasi/ileri1.png"):
                    time.sleep(2)
                    self.click_image("resimler/kara_magarasi/else2.png")
                    time.sleep(1)
                    ileri1 = True
            elif not ileri2:
                if self.click_image("resimler/kara_magarasi/ileri2.png"):
                    ileri2 = True
            elif not ileri3:
                if self.click_image("resimler/kara_magarasi/ileri3.png"):
                    ileri3 = True
                    time.sleep(3)
            elif not geri:
                if self.click_image("resimler/kara_magarasi/geri.png"):
                    geri = True
                    time.sleep(3)
            elif not geri1:
                if self.click_image("resimler/kara_magarasi/geri1.png"):
                    geri1 = True
                    time.sleep(3)
            elif not geri2:
                if self.click_image("resimler/kara_magarasi/geri2.png"):
                    geri2 = True
                    time.sleep(3)
            elif not geri3:
                if self.click_image("resimler/kara_magarasi/geri3.png"):
                    geri3 = True
                    time.sleep(3)
            elif not geri4:
                if self.click_image("resimler/kara_magarasi/geri4.png"):
                    geri4 = True
                    time.sleep(3)
            elif not geri5:
                if self.click_image("resimler/kara_magarasi/geri5.png"):
                    geri5 = True
                    time.sleep(3)
            elif not boss:
                if self.click_image("resimler/kara_magarasi/bos.png"):
                    boss = True
                    time.sleep(10)
            elif not geri_cik:
                if self.click_image("resimler/kara_magarasi/geri_cik.png"):
                    self.statusBar().showMessage("Kara Mağarası Bitti")
                    break
    def birlik_hazinesi(self):
        pass
    def deneme_gecidi(self):
        harita_tikla = False
        deneme_gecidi1 = False
        deneme_gecidi2 = False
        dilek = False
        meydan_tiklama = 0
        tiklama_sayisi = 0
        dilek1 = 0
        if self.ui.deneme_ayar.currentIndex() == 0:
            tiklama_sayisi = 1
        elif self.ui.deneme_ayar.currentIndex() == 1:
            tiklama_sayisi = 5
        elif self.ui.deneme_ayar.currentIndex() == 2:
            tiklama_sayisi = 10
        elif self.ui.deneme_ayar.currentIndex() == 3:
            tiklama_sayisi = 15
        time.sleep(2)
        self.statusBar().showMessage(f"Deneme Geçidi Meydan Okuma Sayısı {tiklama_sayisi}")
        while not self.exit_event.is_set():
            if self.click_image("resimler/deneme_gecidi/gokyuzu.png"):
                pass
            if not harita_tikla:
                if self.click_image("resimler/deneme_gecidi/harita.png"):
                    harita_tikla = True
            elif not deneme_gecidi1:
                if self.click_image("resimler/deneme_gecidi/deneme_gecidi_1.png"):
                    deneme_gecidi1 = True
            elif not deneme_gecidi2:
                if self.click_image("resimler/deneme_gecidi/deneme_gecidi_2.png"):
                    deneme_gecidi2 = True
            elif not dilek:
                for i in range(3):
                    if self.click_image("resimler/deneme_gecidi/dilek.png"):
                        pass
                    elif self.click_image("resimler/deneme_gecidi/dilek_basla.png"):
                        dilek1 += 1
                        pass
                    elif self.click_image("resimler/deneme_gecidi/bereket.png"):
                        pass
                        if self.click_image("resimler/deneme_gecidi/sonlandir.png"):
                            pass
                    if dilek1 == 3:
                        self.click_image("resimler/deneme_gecidi/kapat2.png")
                        dilek = True
            elif self.click_image("resimler/deneme_gecidi/deneme_meydan_oku.png"):
                self.statusBar().showMessage(
                    f"Deneme Geçidi Meydan Okuma Sayısı {meydan_tiklama} kez tıklandı. Kalan {tiklama_sayisi - meydan_tiklama}")
                meydan_tiklama += 1
                # Eğer kullanıcı belirlediği tıklama sayısına ulaşmışsa döngüden çık
            elif meydan_tiklama >= tiklama_sayisi:
                self.statusBar().showMessage("Deneme Geçidi Bitti.")
                if self.click_image("resimler/deneme_gecidi/kapat.png"):
                    print(self.click_image)
                    break
            if self.click_image("resimler/deneme_gecidi/oto_savas.png"):
                pass
    def kutsal_saray(self):
        harita_tikla = False
        kutsal_saray1 = False
        kutsal_saray2 = False
        gokyuzu_tikla = False
        saray_tiklama = 0
        tiklama_sayisi = 0
        # Kullanıcının seçtiği değere göre tıklama sayısını belirle
        if self.ui.kutsal_ayar.currentIndex() == 0:
            tiklama_sayisi = 1
        elif self.ui.kutsal_ayar.currentIndex() == 1:
            tiklama_sayisi = 5
        elif self.ui.kutsal_ayar.currentIndex() == 2:
            tiklama_sayisi = 10
        time.sleep(2)
        self.statusBar().showMessage(f"Kutsal Saray Meydan Okuma Sayısı {tiklama_sayisi}")
        while not self.exit_event.is_set():
            if not gokyuzu_tikla:
                if self.click_image("resimler/kutsal_saray/gokyuzu.png"):
                    gokyuzu_tikla = True
            if not harita_tikla:
                if self.click_image("resimler/kutsal_saray/harita.png"):
                    harita_tikla = True
            elif not kutsal_saray1:
                if self.click_image("resimler/kutsal_saray/kutsal_saray1.png"):
                    kutsal_saray1 = True
            elif not kutsal_saray2:
                if self.click_image("resimler/kutsal_saray/kutsal_saray2.png"):
                    kutsal_saray2 = True
            if self.click_image("resimler/kutsal_saray/iptal.png"):
                pass
            elif self.click_image("resimler/kutsal_saray/savas.png"):
                self.statusBar().showMessage(f"Kutsal Saray {saray_tiklama} kez tıklandı. Kalan {tiklama_sayisi - saray_tiklama}")
                saray_tiklama += 1
            elif self.click_image("resimler/deneme_gecidi/oto_savas.png"):
                pass
            if self.click_image("resimler/kutsal_saray/son.png"):
                time.sleep(2)
                if self.click_image("resimler/kutsal_saray/iptal.png"):
                    time.sleep(1)
                if self.click_image("resimler/kutsal_saray/kapat.png"):
                    self.statusBar().showMessage("kutsal saray bitti...")
                    time.sleep(2)
                    break
            elif saray_tiklama == tiklama_sayisi:
                self.statusBar().showMessage("kutsal saray bitti...")
                if self.click_image("resimler/kutsal_saray/kapat.png"):
                    break
    def titan_tapinagi(self):
        harita_tikla = False
        titan_tapinagi1 = False
        titan_tapinagi2 = False
        titan_tiklama = 0
        tiklama_sayisi = 0

        if self.ui.titan_ayar.currentIndex() == 0:
            tiklama_sayisi = 1
        elif self.ui.titan_ayar.currentIndex() == 1:
            tiklama_sayisi = 5
        elif self.ui.titan_ayar.currentIndex() == 2:
            tiklama_sayisi = 8

        while not self.exit_event.is_set():
            if self.click_image("resimler/titan_tapinagi/gokyuzu.png"):
                time.sleep(3)
            if not harita_tikla:
                if self.click_image("resimler/titan_tapinagi/harita.png"):
                    harita_tikla = True
                    time.sleep(2)  # Her resim aramasından sonra 2 saniye bekle
            elif not titan_tapinagi1:
                if self.click_image("resimler/titan_tapinagi/titan_tapinagi1.png"):
                    titan_tapinagi1 = True
                    time.sleep(2)  # Her resim aramasından sonra 2 saniye bekle
            elif not titan_tapinagi2:
                if self.click_image("resimler/titan_tapinagi/titan_tapinagi2.png"):
                    titan_tapinagi2 = True
                    time.sleep(2)  # Her resim aramasından sonra 2 saniye bekle
            elif self.click_image("resimler/titan_tapinagi/meydan_oku.png"):
                self.statusBar().showMessage(f"Titan tapınağı {titan_tiklama} kez tıklandı. Kalan {tiklama_sayisi - titan_tiklama}")
                titan_tiklama += 1
                time.sleep(5)
            elif titan_tiklama == tiklama_sayisi:
                self.statusBar().showMessage("Titan Tapınağı bitti...")
                time.sleep(2)
                if self.click_image("resimler/titan_tapinagi/kapat.png"):
                    break
    def seytan_kitasi(self):
        harita_tikla = False
        seytan_kitasi = False
        seytan_kitasi1 = False
        yenilik = False
        yenilik1 = False
        baskin_basla = False
        hizlandir = False
        gokyuzu = False
        baskin = False
        while not self.exit_event.is_set():
            if self.click_image("resimler/peri_turnuvasi/gokyuzu.png"):
                time.sleep(1)
            if not harita_tikla:
                if self.click_image("resimler/seytan_kitasi/harita.png"):
                    time.sleep(1)
                    harita_tikla = True
            elif not seytan_kitasi:
                if self.click_image("resimler/seytan_kitasi/seytan_kitasi.png"):
                    seytan_kitasi = True
            elif not seytan_kitasi1:
                if self.click_image("resimler/seytan_kitasi/seytan_kitasi1.png"):
                    seytan_kitasi1 = True
            elif not yenilik:
                if self.click_image("resimler/seytan_kitasi/yenilik.png"):
                    yenilik = True
            elif not yenilik1:
                if self.click_image("resimler/seytan_kitasi/yenilik1.png"):
                    time.sleep(1)
                    yenilik1 = True
            elif not baskin:
                if self.click_image("resimler/seytan_kitasi/baskin.png"):
                    time.sleep(3)
                    baskin = True
                    if self.click_image("resimler/seytan_kitasi/baskin1.png"):
                        keyboard.press("1")
                        keyboard.release("1")
                        time.sleep(0.2)
                        keyboard.press("1")
                        keyboard.release("1")
            elif not baskin_basla:
                if self.click_image("resimler/seytan_kitasi/baskin_basla.png"):
                    time.sleep(1)
                    baskin_basla = True
            if not hizlandir:
                if self.click_image("resimler/seytan_kitasi/hizlandir.png"):
                    time.sleep(1)
                    hizlandir = True
            elif self.click_image("resimler/seytan_kitasi/baskin_bitir.png"):
                time.sleep(2)
                if self.click_image("resimler/seytan_kitasi/kapat1.png"):
                    time.sleep(1)
                if self.click_image("resimler/seytan_kitasi/kapat2.png"):
                    time.sleep(1)
                if self.click_image("resimler/seytan_kitasi/kapat3.png"):
                    time.sleep(1)
                    self.statusBar().showMessage("Şeytan Kıtası Bitti.")
                    time.sleep(1)
                    break
    def sonsuz_ucurum(self):
        harita_tikla = False
        sonsuz_ucurum = False
        sonsuz_ucurum1 = False
        sehir = False
        meydan_oku = 0
        tiklama_sayisi = 0
        hizlandir = False
        if self.ui.sonsuz_ayar.currentIndex() == 0:
            tiklama_sayisi = 1
        elif self.ui.sonsuz_ayar.currentIndex() == 1:
            tiklama_sayisi = 5
        elif self.ui.sonsuz_ayar.currentIndex() == 2:
            tiklama_sayisi = 10
        if self.ui.sonsuz_ayar.currentIndex() == 3:
            tiklama_sayisi = 15
        self.statusBar().showMessage(f"Sonsuz Uçurum Meydan Okuma Sayısı {tiklama_sayisi}")
        time.sleep(2)
        while not self.exit_event.is_set():
            if not sehir:
                if self.click_image("resimler/zafer_yolu/gokyuzu.png"):
                    sehir = True
            if not harita_tikla:
                if self.click_image("resimler/zafer_yolu/harita.png"):
                    harita_tikla = True
            elif not sonsuz_ucurum:
                if self.click_image("resimler/sonsuz_ucurum/sonsuz_ucurum1.png"):
                    sonsuz_ucurum = True
            elif not sonsuz_ucurum1:
                if self.click_image("resimler/sonsuz_ucurum/sonsuz_ucurum2.png"):
                    sonsuz_ucurum1 = True
            elif self.click_image("resimler/sonsuz_ucurum/meydan_oku.png"):
                time.sleep(3)
                meydan_oku = + 1
                self.statusBar().showMessage(
                    f"Sonsuz Uçurum Meydan Okuma Sayısı {meydan_oku} Kalan {tiklama_sayisi - meydan_oku}")
            if not hizlandir:
                if self.click_image("resimler/sonsuz_ucurum/baskin.png"):
                    time.sleep(1)
                    self.click_image("resimler/sonsuz_ucurum/hizlandir.png")
                    hizlandir = True
                    time.sleep(5)
                if self.click_image("resimler/sonsuz_ucurum/bitir.png"):
                    time.sleep(1)
            if meydan_oku == tiklama_sayisi:
                time.sleep(5)
                if self.click_image("resimler/sonsuz_ucurum/kapat.png"):
                    self.statusBar().showMessage("Sonsuz Uçurum Bitti.")
                    time.sleep(2)
                    break
    def intikan_yolu(self):
        if self.click_image("resimler/deneme_gecidi/gokyuzu.png"):
            pass
        pass
    def zafer_yolu(self):
        harita_tikla = False
        kutsal_saray1 = False
        kutsal_saray2 = False
        sehir = False
        ilk_kat = False
        while not self.exit_event.is_set():
            if not sehir:
                if self.click_image("resimler/zafer_yolu/gokyuzu.png"):
                    sehir = True
            if not harita_tikla:
                if self.click_image("resimler/zafer_yolu/harita.png"):
                    harita_tikla = True
            elif not kutsal_saray1:
                if self.click_image("resimler/zafer_yolu/zafer_yolu1.png"):
                    kutsal_saray1 = True
            elif not kutsal_saray2:
                if self.click_image("resimler/zafer_yolu/zafer_yolu2.png"):
                    kutsal_saray2 = True
            elif not ilk_kat:
                if self.click_image("resimler/zafer_yolu/ilk_kat.png"):
                    ilk_kat = True
            elif self.click_image("resimler/zafer_yolu/kabus.png"):
                if self.click_image("resimler/zafer_yolu/onay.png"):
                    time.sleep(5)
            elif self.click_image("resimler/zafer_yolu/kapat.png"):
                self.statusBar().showMessage("Zafer yolu Bitti.")
                time.sleep(3)
                break
    def zaman_kapisi(self):
        if self.click_image("resimler/deneme_gecidi/gokyuzu.png"):
            pass
    def peri_turnuvasi(self):
        harita_tikla = False
        peri_turnuvasi1 = False
        peri_turnuvasi2 = False
        sonlandir = False
        peri_tikla = 0
        while not self.exit_event.is_set():
            if self.click_image("resimler/peri_turnuvasi/gokyuzu.png"):
                pass
            if not harita_tikla:
                if self.click_image("resimler/peri_turnuvasi/harita.png"):
                    harita_tikla = True
            elif not peri_turnuvasi1:
                if self.click_image("resimler/peri_turnuvasi/peri_turnuvasi1.png"):
                    peri_turnuvasi1 = True
            elif not peri_turnuvasi2:
                if self.click_image("resimler/peri_turnuvasi/peri_turnuvasi2.png"):
                    peri_turnuvasi2 = True
            elif self.click_image("resimler/peri_turnuvasi/meydan_oku.png"):
                self.statusBar().showMessage(f"Peri meydan okuma sayısı {peri_tikla} kalan sayı {10 - peri_tikla}.")
                peri_tikla += 1
                time.sleep(4)
            elif peri_tikla == 10:
                    self.statusBar().showMessage("Peri Turnuvası bitti...")
                    if self.click_image("resimler/peri_turnuvasi/kapat.png"):
                        break
            if not sonlandir:
                if self.click_image("resimler/peri_turnuvasi/hemen_sonlandir.png"):
                    sonlandir = False
    def peri_seferi(self):
        harita_tikla = False
        peri_seferi1 = False
        peri_seferi2 = False
        gokyuzu_yolu = False
        sefere_basla = False
        hizlandir = False
        basla = False
        baskin = False
        while not self.exit_event.is_set():
            if not gokyuzu_yolu:
                if self.click_image("resimler/peri_seferi/gokyuzu.png"):
                    gokyuzu_yolu = True
            if not harita_tikla:
                if self.click_image("resimler/peri_seferi/harita.png"):
                    harita_tikla = True
            elif not peri_seferi1:
                if self.click_image("resimler/peri_seferi/peri_seperi1.png"):
                    peri_seferi1 = True
            elif not peri_seferi2:
                if self.click_image("resimler/peri_seferi/peri_seperi2.png"):
                    peri_seferi2 = True
            elif not sefere_basla:
                if self.click_image("resimler/peri_seferi/sefer_basla.png"):
                    sefere_basla = True
            elif not basla:
                if self.click_image("resimler/peri_seferi/basla.png"):
                    basla = True
            elif not baskin:
                if self.click_image("resimler/peri_seferi/baskin.png"):
                    baskin = True
            elif not hizlandir:
                if self.click_image("resimler/peri_seferi/hizlandir.png"):
                    hizlandir = True
            elif self.click_image("resimler/peri_seferi/bitir.png"):
                self.statusBar().showMessage("Peri Seferi Bitti")
                break
    def peri_adasi(self):
        liris_resimler = ["resimler/peri_adasi/liris.png",
                          "resimler/peri_adasi/liris2.png",
                          "resimler/peri_adasi/liris3.png",
                          "resimler/peri_adasi/liris4.png"]
        gokyuzu_yolu = False
        tiklama = 0
        while not self.exit_event.is_set():
            for resim in liris_resimler:
                if not gokyuzu_yolu:
                    if self.click_image("resimler/peri_adasi/gokyuzu.png"):
                        gokyuzu_yolu = True
                if self.click_image(resim):
                    time.sleep(5)
                    tiklama = + 1
                elif tiklama >= 30:
                    self.statusBar().showMessage("Peri Adası Bitti")
                elif self.click_image("resimler/gokyuzu_yolu/geri.png"):
                    break
    def gokyuzu_yolu(self):
        harita_tikla = False
        gokyuzu_yolu1 = False
        gokyuzu_yolu2 = False
        gokyuzu_yolu = False
        sandik = False
        kesif_tikla = 0
        while not self.exit_event.is_set():
            if not gokyuzu_yolu:
                if self.click_image("resimler/gokyuzu_yolu/gokyuzu.png"):
                    gokyuzu_yolu = True
            if not harita_tikla:
                if self.click_image("resimler/gokyuzu_yolu/harita.png"):
                    harita_tikla = True
            elif not gokyuzu_yolu1:
                if self.click_image("resimler/gokyuzu_yolu/gokyuzu1.png"):
                    gokyuzu_yolu1 = True
            elif not gokyuzu_yolu2:
                if self.click_image("resimler/gokyuzu_yolu/gokyuzu2.png"):
                    gokyuzu_yolu2 = True
            elif not sandik:
                if self.tasima("resimler/gokyuzu_yolu/sandik.png"):
                    sandik = True
            if self.click_image("resimler/gokyuzu_yolu/kesif.png"):
                self.statusBar().showMessage(f"Keşif {kesif_tikla} kez tıklandı. Kalan {30 - kesif_tikla}")
                kesif_tikla += 1
                time.sleep(4)
                if self.click_image("resimler/gokyuzu_yolu/oto_savas.png"):
                    time.sleep(1)
            elif kesif_tikla == 30:
                self.statusBar().showMessage("Gökyüzü Yolu bitti...")
                if self.click_image("resimler/zafer_yolu/kapat.png"):
                    time.sleep(1)
            elif self.click_image("resimler/gokyuzu_yolu/geri.png"):
                time.sleep(1)
                break
    def ciftlik(self):
        ev_clicked = False
        ciflik_clicked = False
        sehir_tikla = False
        ileri_tikla = 0
        tiklama_sayisi = 0

        if self.ui.ciftlik_ayar.currentIndex() == 0:
            tiklama_sayisi = 1
        elif self.ui.ciftlik_ayar.currentIndex() == 1:
            tiklama_sayisi = 5
        elif self.ui.ciftlik_ayar.currentIndex() == 2:
            tiklama_sayisi = 10
        if self.ui.ciftlik_ayar.currentIndex() == 3:
            tiklama_sayisi = 15
        elif self.ui.ciftlik_ayar.currentIndex() == 4:
            tiklama_sayisi = 20
        elif self.ui.ciftlik_ayar.currentIndex() == 5:
            tiklama_sayisi = 25

        while not self.exit_event.is_set():
            if not sehir_tikla:
                if self.click_image("resimler/ciftlik/sehir.png"):
                    sehir_tikla = True
            if not ev_clicked:
                if self.click_image("resimler/ciftlik/ev.png"):
                    ev_clicked = True
            elif not ciflik_clicked:
                if self.click_image("resimler/ciftlik/ciftlik.png"):
                    ciflik_clicked = True
                if self.click_image("resimler/ciftlik/topla.png"):
                    time.sleep(1)
            if self.click_image("resimler/ciftlik/elmas.png"):
                self.click_image("resimler/ciftlik/topla.png")
            elif self.click_image("resimler/ciftlik/elmas1.png"):
                self.click_image("resimler/ciftlik/topla.png")
            elif self.click_image("resimler/ciftlik/elmas2.png"):
                self.click_image("resimler/ciftlik/topla.png")
            elif self.click_image("resimler/ciftlik/elmas3.png"):
                self.click_image("resimler/ciftlik/topla.png")
            else:
                if self.click_image("resimler/ciftlik/ileri.png"):
                    ileri_tikla += 1
                    self.statusBar().showMessage(
                        f"Tıklanan Sayfa Sayısı {ileri_tikla} Kalan Sayfa Sayısı {tiklama_sayisi - ileri_tikla}")
                if ileri_tikla == tiklama_sayisi:
                    self.statusBar().showMessage("Çiftlik bitti...")
                    time.sleep(1)
                    self.click_image("resimler/ciftlik/kapat.png")
                    time.sleep(1)
                    self.click_image("resimler/ciftlik/kapat.png")
                    break
    def ahir(self):
        ev_clicked = False
        ciflik_clicked = False
        sehir_tikla = False
        ileri_tikla = 0
        tiklama_sayisi = 0

        if self.ui.ciftlik_ayar.currentIndex() == 0:
            tiklama_sayisi = 1
        elif self.ui.ciftlik_ayar.currentIndex() == 1:
            tiklama_sayisi = 5
        elif self.ui.ciftlik_ayar.currentIndex() == 2:
            tiklama_sayisi = 10
        if self.ui.ciftlik_ayar.currentIndex() == 3:
            tiklama_sayisi = 15
        elif self.ui.ciftlik_ayar.currentIndex() == 4:
            tiklama_sayisi = 20
        elif self.ui.ciftlik_ayar.currentIndex() == 5:
            tiklama_sayisi = 25

        while not self.exit_event.is_set():
            if not sehir_tikla:
                if self.click_image("resimler/ahir/sehir.png"):
                    sehir_tikla = True
            if not ev_clicked:
                if self.click_image("resimler/ahir/ev.png"):
                    ev_clicked = True
                    time.sleep(1)  # Her resim aramasından sonra 2 saniye bekle
            elif not ciflik_clicked:
                if self.click_image("resimler/ahir/ahir.png"):
                    ciflik_clicked = True
                if self.click_image("resimler/ciftlik/topla.png"):
                    time.sleep(1)
            elif self.click_image("resimler/ahir/hap.png"):
                self.click_image("resimler/ahir/topla.png")
            elif self.click_image("resimler/ahir/hap1.png"):
                self.click_image("resimler/ahir/topla.png")
            else:
                if self.click_image("resimler/ahir/ileri.png"):
                    ileri_tikla += 1
                    self.statusBar().showMessage(
                        f"Tıklanan Sayfa Sayısı {ileri_tikla} Kalan Sayfa Sayısı {tiklama_sayisi - ileri_tikla}")
                if ileri_tikla == tiklama_sayisi:
                    self.statusBar().showMessage("Ahır bitti...")
                    time.sleep(1)
                    self.click_image("resimler/ahir/kapat.png")
                    time.sleep(1)
                    self.click_image("resimler/ahir/kapat.png")
                    break
    def kedi_evi(self):
        ev_clicked = False
        sehir_tikla = False
        kedi_evi = False
        while not self.exit_event.is_set():
            if not sehir_tikla:
                if self.click_image("resimler/ciftlik/sehir.png"):
                    sehir_tikla = True
            if not ev_clicked:
                if self.click_image("resimler/ciftlik/ev.png"):
                    ev_clicked = True
            elif not kedi_evi:
                if self.click_image("resimler/kedi_evi/kedi_evi.png"):
                    kedi_evi = True
                    time.sleep(5)
            elif self.click_image("resimler/kedi_evi/teslim.png"):
                pass
            elif self.click_image("resimler/kedi_evi/kazanc.png"):
                pass
            elif self.click_image("resimler/kedi_evi/konum.png"):
                pass
            else:
                if self.click_image("resimler/kedi_evi/kapat.png"):
                    self.statusBar().showMessage("Kedi Evi bitti...")
                    time.sleep(1)
                    self.click_image("resimler/kedi_evi/kapat.png")
                    time.sleep(1)
                    self.click_image("resimler/kedi_evi/kapat.png")
                    break
    def cevre_kesif(self):
        cevre_tikla = False
        kazi_tikla = 0
        tiklama_sayisi = 0

        if self.ui.cevre_ayar.currentIndex() == 0:
            tiklama_sayisi = 1
        elif self.ui.cevre_ayar.currentIndex() == 1:
            tiklama_sayisi = 5
        elif self.ui.cevre_ayar.currentIndex() == 2:
            tiklama_sayisi = 10
        if self.ui.cevre_ayar.currentIndex() == 3:
            tiklama_sayisi = 15
        elif self.ui.cevre_ayar.currentIndex() == 4:
            tiklama_sayisi = 20
        elif self.ui.cevre_ayar.currentIndex() == 5:
            tiklama_sayisi = 30

        while not self.exit_event.is_set():
            if not cevre_tikla:
                if self.click_image("resimler/cevre/cevre.png"):
                    cevre_tikla = True
            elif self.click_image("resimler/cevre/kesif.png"):
                pass
            else:
                self.click_image("resimler/cevre/kapat.png")
                time.sleep(1)
            if self.click_image("resimler/cevre/kazi.png"):
                self.statusBar().showMessage(f"Kazı {kazi_tikla} kez tıklandı. Kalan sayı {tiklama_sayisi - kazi_tikla}")
                kazi_tikla += 1
                time.sleep(1)
            if kazi_tikla == tiklama_sayisi:
                self.statusBar().showMessage("Çevfe keşif bitti...")
                time.sleep(1)
                self.click_image("resimler/cevre/sehir.png")
                break
    def amfi_tiyatro(self):
        zaman_hazinesi = False
        amfi_ = False
        kurma = False
        hazir_tikla = 0
        while not self.exit_event.is_set():
            if self.click_image("resimler/amfi_tiyatro/gokyuzu.png"):
                pass
            if not zaman_hazinesi:
                if self.click_image("resimler/amfi_tiyatro/zaman_hazinesi.png"):
                    zaman_hazinesi = True
                else:
                    self.click_image("resimler/kara_magarasi/else.png")
            elif not amfi_:
                if self.click_image("resimler/amfi_tiyatro/amfi_tiyatro.png"):
                    amfi_ = True
            elif not kurma:
                if self.click_image("resimler/amfi_tiyatro/kurma.png"):
                    kurma = True
            if self.click_image("resimler/amfi_tiyatro/hazir.png"):
                self.statusBar().showMessage(f"Hazır {hazir_tikla} kez tıklandı. Kalan sayı {15 - hazir_tikla}")
                hazir_tikla += 1
            elif hazir_tikla == 15:
                self.statusBar().showMessage("Amfi Tiyatro bitti...")
                time.sleep(2)
                self.click_image("resimler/amfi_tiyatro/geri.png")
                break
            if self.click_image("resimler/amfi_tiyatro/basla.png"):
                self.statusBar().showMessage(f"Başlat {hazir_tikla} kez tıklandı. Kalan sayı {15 - hazir_tikla}")
                hazir_tikla += 1
            elif hazir_tikla >= 15:
                self.statusBar().showMessage("Amfi Tiyatro bitti...")
                time.sleep(2)
                self.click_image("resimler/amfi_tiyatro/geri.png")
                break
    def labavatuar(self):
        labavatuar = False
        hazir_tikla = 0
        while not self.exit_event.is_set():
            if self.click_image("resimler/labavatuar/sehir.png"):
                pass
            if not labavatuar:
                if self.click_image("resimler/labavatuar/laboratuvar.png"):
                    labavatuar = True
                    time.sleep(6)  # Her resim aramasından sonra 2 saniye bekle
            elif self.click_image("resimler/labavatuar/tatto.png"):
                self.statusBar().showMessage(f"tatto {hazir_tikla} kez tıklandı. Kalan sayı {3 - hazir_tikla}")
                hazir_tikla += 1
            elif hazir_tikla >= 3:
                self.statusBar().showMessage("Tatto toplama bitti...")
                time.sleep(2)
                self.click_image("resimler/labavatuar/kapat.png")
                break
            else:
                if self.click_image("resimler/labavatuar/geri.png"):
                    self.statusBar().showMessage(f"Toplanacak Tatto yok diğer işleme geçiliyor...")
                    time.sleep(2)
                    self.click_image("resimler/labavatuar/kapat.png")
                    break
    def sihirli_lokal(self):
        sehir = False
        labavatuar = False
        sihirli_lokal = False
        demirci = False
        badin = False
        phina = False
        sandy = False
        brad = False
        while not self.exit_event.is_set():
            if not sehir:
                if self.click_image("resimler/sihirli_lokal/sehir.png"):
                    sehir = True
            if not labavatuar:
                if self.click_image("resimler/sihirli_lokal/sihirli_konak.png"):
                    labavatuar = True
            elif not sihirli_lokal:
                if self.click_image("resimler/sihirli_lokal/sihirli_lokal.png"):
                    sihirli_lokal = True
            elif not demirci:
                if self.click_image("resimler/sihirli_lokal/demirci.png"):
                    demirci = True
                    time.sleep(1)  # Her resim aramasından sonra 2 saniye bekle
                    if self.click_image("resimler/sihirli_lokal/metin.png"):
                        if self.click_image("resimler/sihirli_lokal/metin2.png"):
                            time.sleep(0.2)
                            self.click_image("resimler/sihirli_lokal/geri.png")
                    else:
                        self.click_image("resimler/sihirli_lokal/geri.png")
                        time.sleep(1)
            elif not badin:
                if self.click_image("resimler/sihirli_lokal/badin.png"):
                    badin = True
                    time.sleep(1)  # Her resim aramasından sonra 2 saniye bekle
                    if self.click_image("resimler/sihirli_lokal/metin.png"):
                        time.sleep(0.2)
                        if self.click_image("resimler/sihirli_lokal/metin2.png"):
                            time.sleep(1)
                            self.click_image("resimler/sihirli_lokal/geri.png")
                    else:
                        self.click_image("resimler/sihirli_lokal/geri.png")
                        time.sleep(1)
            elif not phina:
                if self.click_image("resimler/sihirli_lokal/phina.png"):
                    phina = True
                    time.sleep(1)
                    if self.click_image("resimler/sihirli_lokal/metin.png"):
                        time.sleep(0.2)
                        if self.click_image("resimler/sihirli_lokal/metin2.png"):
                            time.sleep(1)
                            self.click_image("resimler/sihirli_lokal/geri.png")
                    else:
                        self.click_image("resimler/sihirli_lokal/geri.png")
                        time.sleep(1)
            elif not sandy:
                if self.click_image("resimler/sihirli_lokal/sandy.png"):
                    sandy = True
                    time.sleep(1)
                    if self.click_image("resimler/sihirli_lokal/metin.png"):
                        time.sleep(0.2)
                        if self.click_image("resimler/sihirli_lokal/metin2.png"):
                            time.sleep(1)
                            self.click_image("resimler/sihirli_lokal/geri.png")
                    else:
                        self.click_image("resimler/sihirli_lokal/geri.png")
                        time.sleep(1)
            elif not brad:
                if self.click_image("resimler/sihirli_lokal/brad.png"):
                    brad = True
                    time.sleep(1)
                    if self.click_image("resimler/sihirli_lokal/metin.png"):
                        time.sleep(1)
                        if self.click_image("resimler/sihirli_lokal/metin2.png"):
                            time.sleep(1)
                            self.click_image("resimler/sihirli_lokal/kapat.png")
                            time.sleep(1)
                            self.click_image("resimler/sihirli_lokal/kapat.png")
                            self.statusBar().showMessage("Sihirli Konak Bitti.")
                            break
                    else:
                        self.click_image("resimler/sihirli_lokal/kapat.png")
                        time.sleep(1)
                        self.click_image("resimler/sihirli_lokal/kapat.png")
                        break
    def yeralti_labirenti(self):
        sehir = False
        yeralti_labirant = False
        yeralti_labirant1 = False
        yeralti_labirant2 = False
        baskin1 = False
        baskin2 = False
        baskin3 = False
        yeralti = False
        ucurum = False
        araf = False
        while not self.exit_event.is_set():
            if not sehir:
                if self.click_image("resimler/sihirli_lokal/sehir.png"):
                    sehir = True
            if not yeralti_labirant:
                if self.click_image("resimler/yerali_labirenti/yeralti_labirenti.png"):
                    yeralti_labirant = True
            elif not yeralti:
                if self.click_image("resimler/yerali_labirenti/yeralti.png"):
                    yeralti = True
            if self.click_image("resimler/yerali_labirenti/devam.png"):
                time.sleep(5)
                self.click_image("resimler/yerali_labirenti/oto_savas.png")
            elif not baskin1:
                if self.click_image("resimler/yerali_labirenti/baskin.png"):
                    time.sleep(3)
                    baskin1 = True
                if self.click_image("resimler/yerali_labirenti/baskin_basla.png"):
                    time.sleep(2)
                if self.click_image("resimler/yerali_labirenti/hizlandir.png"):
                    time.sleep(6)
                    if self.click_image("resimler/yerali_labirenti/baskin_bitir.png"):
                        time.sleep(1)
                    if self.click_image("resimler/yerali_labirenti/kapat.png"):
                        time.sleep(1)
            elif not yeralti_labirant1:
                if self.click_image("resimler/yerali_labirenti/yeralti_labirenti.png"):
                    yeralti_labirant1 = True
            elif not ucurum:
                if self.click_image("resimler/yerali_labirenti/ucurum.png"):
                    ucurum = True
                    time.sleep(1)  # Her resim aramasından sonra 2 saniye bekle
                if self.click_image("resimler/yerali_labirenti/devam.png"):
                    time.sleep(5)
                    self.click_image("resimler/yerali_labirenti/oto_savas.png")

                if self.click_image("resimler/yerali_labirenti/baskin.png"):
                    time.sleep(3)
                if self.click_image("resimler/yerali_labirenti/baskin_basla.png"):
                    time.sleep(2)
                if self.click_image("resimler/yerali_labirenti/hizlandir.png"):
                    time.sleep(6)
                    if self.click_image("resimler/yerali_labirenti/baskin_bitir.png"):
                        time.sleep(1)
            elif not yeralti_labirant2:
                if self.click_image("resimler/yerali_labirenti/yeralti_labirenti.png"):
                    yeralti_labirant2 = True
            elif not araf:
                if self.click_image("resimler/yerali_labirenti/araf.png"):
                    araf = True
                    time.sleep(1)  # Her resim aramasından sonra 2 saniye bekle
                if self.click_image("resimler/yerali_labirenti/devam.png"):
                    time.sleep(5)
                    self.click_image("resimler/yerali_labirenti/oto_savas.png")
                if self.click_image("resimler/yerali_labirenti/baskin.png"):
                    time.sleep(3)
                elif self.click_image("resimler/yerali_labirenti/baskin_basla.png"):
                    time.sleep(2)
                elif self.click_image("resimler/yerali_labirenti/hizlandir.png"):
                    time.sleep(6)
                    if self.click_image("resimler/yerali_labirenti/baskin_bitir.png"):
                        time.sleep(1)
                        self.click_image("resimler/yerali_labirenti/kapat.png")
                        self.statusBar().showMessage("Yeraltı Labirenti Bitti.")
                        time.sleep(2)
                        break
    def yuzey_savasi(self):
        transfer_kampi = False
        transfer = False
        geri = False
        sehir = False
        while not self.exit_event.is_set():
            if not sehir:
                self.click_image("resimler/ciftlik/sehir.png")
                sehir = True
                time.sleep(3)
            if not transfer_kampi:
                if self.click_image("resimler/yuzey_savasi/transfer_kampi.png"):
                    transfer_kampi = True
                    time.sleep(1)  # Her resim aramasından sonra 2 saniye bekle
            elif not transfer:
                if self.click_image("resimler/yuzey_savasi/transfer.png"):
                    transfer = True
            elif self.click_image("resimler/yuzey_savasi/mevcut.png"):
                if self.click_image("resimler/yuzey_savasi/geri.png"):
                    time.sleep(1)  # Her resim aramasından sonra 2 saniye bekle
                    self.click_image("resimler/yuzey_savasi/onay.png")
                    time.sleep(1)  # Her resim aramasından sonra 2 saniye bekle
                    self.statusBar().showMessage("Yüzey Savaşı Bitti.")
                    time.sleep(2)
                    break
    def bolge_kesif(self):
        transfer_kampi = False
        transfer = False
        heidrun = False
        heidrun1 = False
        onay = False
        time.sleep(2)
        while not self.exit_event.is_set():
            if self.click_image("resimler/bolge_kesif/gokyuzu.png"):
                time.sleep(3)
            if not transfer_kampi:
                if self.click_image("resimler/bolge_kesif/harita.png"):
                    transfer_kampi = True
            elif not transfer:
                if self.click_image("resimler/bolge_kesif/bolge.png"):
                    transfer = True
            elif not heidrun:
                if self.click_image("resimler/bolge_kesif/heidrun.png"):
                    heidrun = True
                    time.sleep(2)  # Her resim aramasından sonra 2 saniye bekle
                if self.click_image("resimler/bolge_kesif/kesif.png"):
                    time.sleep(1)
                    self.click_image("resimler/bolge_kesif/onay.png")
            elif not onay:
                self.click_image("resimler/bolge_kesif/geri.png")
                onay = True
                time.sleep(1)
                self.click_image("resimler/bolge_kesif/onay.png")
                time.sleep(5)
            elif not heidrun1:
                if self.click_image("resimler/bolge_kesif/heidrun.png"):
                    heidrun1 = True
                if self.click_image("resimler/bolge_kesif/kesif.png"):
                    time.sleep(1)
                    self.click_image("resimler/bolge_kesif/onay.png")
            elif self.click_image("resimler/bolge_kesif/geri.png"):
                time.sleep(1)
                self.click_image("resimler/bolge_kesif/onay.png")
                time.sleep(1)
                self.click_image("resimler/bolge_kesif/geri.png")
                time.sleep(1)
                self.statusBar().showMessage("Bölge Keşif Bitti.")
                break
    def koruma_arama(self):
        gokyuzu = False
        harita = False
        koruma1 = False
        koruma2 = False
        while not self.exit_event.is_set():
            if not gokyuzu:
                self.click_image("resimler/zafer_yolu/gokyuzu.png")
                gokyuzu = True
            if not harita:
                if self.click_image("resimler/koruma_arama/harita.png"):
                    harita = True
            elif not koruma1:
                if self.click_image("resimler/koruma_arama/koruma1.png"):
                    koruma1 = True
            elif not koruma2:
                if self.click_image("resimler/koruma_arama/koruma2.png"):
                    koruma2 = True
                    time.sleep(5)
            if self.click_image("resimler/koruma_arama/arama_1.png"):
                self.click_image("resimler/koruma_arama/meydan_oku.png")
            elif self.click_image("resimler/koruma_arama/arama_2.png"):
                self.click_image("resimler/koruma_arama/meydan_oku.png")
            elif self.click_image("resimler/koruma_arama/arama_3.png"):
                self.click_image("resimler/koruma_arama/meydan_oku.png")
            elif self.click_image("resimler/koruma_arama/arama_4.png"):
                self.click_image("resimler/koruma_arama/meydan_oku.png")
            else:
                if self.click_image("resimler/koruma_arama/kapat.png"):
                    time.sleep(1)
                    self.click_image("resimler/koruma_arama/kapat.png")
                    self.statusBar().showMessage("Koruma Arama Bitti")
                    break
    def intikam_yolu(self):
        gokyuzu = False
        harita = False
        intikan1 = False
        intikan2 = False
        sonsuz = False
        sonsuz1 = False
        baskin = False
        baskin1 = False
        while not self.exit_event.is_set():
            if not gokyuzu:
                self.click_image("resimler/zafer_yolu/gokyuzu.png")
                gokyuzu = True
            if not harita:
                if self.click_image("resimler/intikam_yolu/harita.png"):
                    harita = True
            elif not intikan1:
                if self.click_image("resimler/intikam_yolu/intikam_yolu1.png"):
                    intikan1 = True
            elif not intikan2:
                if self.click_image("resimler/intikam_yolu/intikam_yolu2.png"):
                    intikan2 = True
            elif not sonsuz:
                if self.click_image("resimler/intikam_yolu/sonsuz.png"):
                    sonsuz = True
            elif not sonsuz1:
                if self.click_image("resimler/intikam_yolu/sonsuz1.png"):
                    sonsuz1 = True
            elif self.click_image("resimler/intikam_yolu/baskin.png"):
                time.sleep(1)
                self.click_image("resimler/intikam_yolu/baskin1.png")
                time.sleep(1)
                keyboard.press("1")
                keyboard.release("1")
            elif self.click_image("resimler/intikam_yolu/baskin_basla.png"):
                time.sleep(1)
            elif self.click_image("resimler/intikam_yolu/hizlandir.png"):
                time.sleep(1)
            elif self.click_image("resimler/intikam_yolu/baskin_bitir.png"):
                time.sleep(1)
            elif self.click_image("resimler/intikam_yolu/kapat.png"):
                time.sleep(1)
                if self.click_image("resimler/intikam_yolu/kapat.png"):
                    break
    def kurtulus_yolu(self):
        gokyuzu = False
        harita = False
        kurtulus1 = False
        kurtulus2 = False
        meydan_oku = False
        basla = 0
        while not self.exit_event.is_set():
            if not gokyuzu:
                self.click_image("resimler/zafer_yolu/gokyuzu.png")
                gokyuzu = True
            if not harita:
                if self.click_image("resimler/kurtulus_yolu/harita.png"):
                    harita = True
            elif not kurtulus1:
                if self.click_image("resimler/kurtulus_yolu/kurtulus1.png"):
                    kurtulus1 = True
            elif not kurtulus2:
                if self.click_image("resimler/kurtulus_yolu/kurtulus2.png"):
                    kurtulus2 = True
            elif not meydan_oku:
                if self.click_image("resimler/kurtulus_yolu/meydan_oku.png"):
                    meydan_oku = True
            elif self.click_image("resimler/kurtulus_yolu/basla.png"):
                self.statusBar().showMessage(f"Kazı {basla} kez tıklandı. Kalan sayı {10 - basla}")
                basla += 1
            else:
                break
            if basla >= 10:
                self.statusBar().showMessage("Kurtuluş Yolı bitti...")
                if self.click_image("resimler/kurtulus_yolu/kapat.png"):
                    time.sleep(1)
                    break
            if self.click_image("resimler/kurtulus_yolu/oto_savas.png"):
                time.sleep(1)
    def birlik_sirri(self):
        birlik = False
        birlik_oyun = False
        ilerle = False
        while not self.exit_event.is_set():
            if not birlik:
                self.click_image("resimler/birlik_sirri/birlik.png")
                birlik = True
            if not birlik_oyun:
                if self.click_image("resimler/birlik_sirri/birlik_oyunlari.png"):
                    birlik_oyun = True
            elif not ilerle:
                if self.click_image("resimler/birlik_sirri/ilerle.png"):
                    ilerle = True
            elif self.click_image("resimler/birlik_sirri/kutsal_agac.png"):
                if self.click_image("resimler/birlik_sirri/geri.png"):
                    time.sleep(1)
                    self.click_image("resimler/birlik_sirri/onay.png")
                    self.statusBar().showMessage("Birlik Sırrı Bitti.")
                    time.sleep(2)
                    break
    def birlik_katkisi(self):
        birlik = False
        birlik_katki = False
        ilerle = False
        while not self.exit_event.is_set():
            if not birlik:
                self.click_image("resimler/birlik_katkisi/birlik.png")
                birlik = True
            if not birlik_katki:
                if self.click_image("resimler/birlik_katkisi/birlik_katki.png"):
                    birlik_katki = True
                    time.sleep(3)
                    keyboard.press("5")
                    keyboard.release("5")
                for i in range(7):
                    keyboard.press("0")
                    keyboard.release("0")

            elif not ilerle:
                if self.click_image("resimler/birlik_katkisi/katki_yap.png"):
                    ilerle = True
                if self.click_image("resimler/birlik_katkisi/kapat.png"):
                    self.statusBar().showMessage("Birlik Katkısı Bitti")
                    time.sleep(2)
                    self.click_image("resimler/birlik_katkisi/kapat.png")
                    break
    def birlik_bereketi(self):
        birlik = False
        birlik_katki = False
        ilerle = False
        while not self.exit_event.is_set():
            if not birlik:
                self.click_image("resimler/birlik_katkisi/birlik.png")
                birlik = True
            if not birlik_katki:
                if self.click_image("resimler/birlik_bereketi/birlik_bereketi.png"):
                    birlik_katki = True
                    time.sleep(3)
            elif not ilerle:
                if self.click_image("resimler/birlik_bereketi/ibadethane.png"):
                    ilerle = True
                    for i in range(2):
                        self.click_image("resimler/birlik_bereketi/bereket.png")
                        time.sleep(1)
                    if self.click_image("resimler/birlik_katkisi/kapat.png"):
                        self.statusBar().showMessage("Birlik Katkısı Bitti")
                        time.sleep(1)
                        self.click_image("resimler/birlik_katkisi/kapat.png")
                        break
    def iskele(self):
        ev_clicked = False
        ciflik_clicked = False
        sehir_tikla = False
        liman = False
        kabul_et = False
        gemi = False
        ticaret = False
        tiklama_sayisi = 0  # Kabul tıklama sayısını saymak için
        while not self.exit_event.is_set():
            if not sehir_tikla:
                if self.click_image("resimler/ciftlik/sehir.png"):
                    sehir_tikla = True
            if not ev_clicked:
                if self.click_image("resimler/ciftlik/ev.png"):
                    ev_clicked = True
            elif not ciflik_clicked:
                if self.click_image("resimler/iskele/iskele.png"):
                    ciflik_clicked = True
            elif not liman:
                if self.click_image("resimler/iskele/liman.png"):
                    liman = True
            elif not kabul_et and tiklama_sayisi < 3:  # Üç kez kabul.png tıklamak için kontrol
                if self.click_image("resimler/iskele/kabul.png"):
                    tiklama_sayisi += 1
            elif not ticaret:
                if tiklama_sayisi == 3:  # Üç kez kabul.png tıklandığında
                    if self.click_image("resimler/iskele/ticaret.png"):
                        time.sleep(1)
                        ticaret = True
            elif not gemi:
                if self.click_image("resimler/iskele/gemi.png"):
                    time.sleep(1)
                    gemi = True
            elif self.click_image("resimler/iskele/onay.png"):
                time.sleep(1)
                self.statusBar().showMessage("İskele Bitti")
                if self.click_image("resimler/iskele/kapat.png"):
                    time.sleep(1)
                if self.click_image("resimler/iskele/kapat.png"):
                    break

    def exp_script(self):
        expFirst = None
        i = 0
        while not self.exit_event.is_set():
            exp = pyautogui.locateCenterOnScreen("exp.png")
            reload = pyautogui.locateCenterOnScreen("reload.png")
            open = pyautogui.locateCenterOnScreen("open.png")

            if exp[0] == -1:
                self.perform_click(reload)
                time.sleep(0.5)
            elif exp[0] != -1:
                if expFirst == exp[0] or expFirst is None and i != 4:
                    self.perform_click(open)
                    expFirst = exp[0]
                    i += 1
                else:
                    self.perform_click(reload)
                    expFirst = None
                    i = 0
                    time.sleep(0.5)

    def sefer_script(self):
        seferFirst = None
        i = 0
        while not self.exit_event.is_set():
            sefer = pyautogui.locateCenterOnScreen("sefer.png")
            reload = pyautogui.locateCenterOnScreen("reload.png")
            open = pyautogui.locateCenterOnScreen("open.png")

            if sefer[0] == -1:
                self.perform_click(reload)
                time.sleep(0.5)
            elif sefer[0] != -1:
                if seferFirst == sefer[0] or seferFirst is None and i != 4:
                    self.perform_click(open)
                    seferFirst = sefer[0]
                    i += 1
                else:
                    self.perform_click(reload)
                    seferFirst = None
                    i = 0
                    time.sleep(0.5)

# Ana uygulamayı başlatma
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
