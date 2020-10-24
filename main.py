from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QColorDialog, QMessageBox
from design import Ui_MainWindow
import sys
from discord_webhook import DiscordWebhook, DiscordEmbed
from configparser import ConfigParser

class WebhookSenderApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(WebhookSenderApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        config_file = 'config.ini'
        config = ConfigParser()
        config.read(config_file)
        self.ui.wh_url_ph.setText(config['WebHook']['webhook_url'])
        self.ui.wh_un_ph.setText(config['WebHook']['webhook_username'])
        self.ui.wh_avatar_ph.setText(config['WebHook']['webhook_avatar_url'])

        def show_error():
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("An error occurred while sending.")
            msg.setInformativeText("Check your data.")
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)

            x = msg.exec_()

        def btn_wh_clear():
            self.ui.wh_url_ph.setText('')
            self.ui.wh_un_ph.setText('')
            self.ui.wh_avatar_ph.setText('')

        def btn_send_clear():
            self.ui.send_title_ph.setText('')
            self.ui.send_author_ph.setText('')
            self.ui.send_author_icon_ph.setText('')
            self.ui.send_image_ph.setText('')
            self.ui.send_thumbnail_ph.setText('')
            self.ui.send_footer_ph.setText('')
            self.ui.send_color_ph.setText('')
            self.ui.send_desc_ph.setText('')

        def btn_send_color():
            sel_col = QColorDialog.getColor()
            color = sel_col.name().replace('#', '')
            self.ui.send_color_ph.setText(color)
            self.ui.send_color_ph.setStyleSheet("QWidget {color: %s}" % sel_col.name())

        def btn_send():
            embed_title = self.ui.send_title_ph.text()
            embed_author = self.ui.send_author_ph.text()
            embed_author_icon = self.ui.send_author_icon_ph.text()
            embed_image = self.ui.send_image_ph.text()
            embed_thumbnail = self.ui.send_thumbnail_ph.text()
            embed_footer = self.ui.send_footer_ph.text()
            embed_timestamp = self.ui.send_timestamp_cb.isChecked()
            embed_color = self.ui.send_color_ph.text()
            if embed_color != "":
                e_color = int(embed_color, 16)
            else:
                e_color = 000000
            embed_desc = self.ui.send_desc_ph.toPlainText()
            wh_u = self.ui.wh_url_ph.text()
            wh_n = self.ui.wh_un_ph.text()
            wh_a = self.ui.wh_avatar_ph.text()
            try:
                webhook = DiscordWebhook(url=wh_u, username=wh_n, avatar_url=wh_a)
                embed = DiscordEmbed(title=embed_title, description=embed_desc, color=e_color)
                embed.set_author(name=embed_author, icon_url=embed_author_icon)
                embed.set_image(url=embed_image)
                embed.set_thumbnail(url=embed_thumbnail)
                embed.set_footer(text=embed_footer)
                if embed_timestamp == True:
                    embed.set_timestamp()
                webhook.add_embed(embed)
                response = webhook.execute()
            except:
                show_error()

        def btn_save():
            config['WebHook']['webhook_url'] = self.ui.wh_url_ph.text()
            config['WebHook']['webhook_username'] = self.ui.wh_un_ph.text()
            config['WebHook']['webhook_avatar_url'] = self.ui.wh_avatar_ph.text()

            with open('config.ini', 'w') as config_file:
        	       config.write(config_file)

        self.ui.wh_clear.clicked.connect(btn_wh_clear)
        self.ui.send_clear.clicked.connect(btn_send_clear)
        self.ui.send_send.clicked.connect(btn_send)
        self.ui.send_color_btn.clicked.connect(btn_send_color)
        self.ui.wh_save.clicked.connect(btn_save)


app = QtWidgets.QApplication([])
application = WebhookSenderApp()
application.show()

sys.exit(app.exec())