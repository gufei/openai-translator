import json
import time

from ui.mainwindow import Ui_Translator
from PyQt5.QtWidgets import QMessageBox
import openai


class UI(Ui_Translator):
    def __init__(self):
        super(UI, self).__init__()

    def init_connect(self):
        self.translator_button.clicked.connect(self.translator)

    def translator(self):
        openai.api_key = self.ApiKey_lineEdit.text()
        openai.api_base = self.BaseURL_lineEdit.text()

        if openai.api_key == "":
            QMessageBox.critical(self.centralwidget, "错误", "apikey 必须设置", QMessageBox.Ok)
            self.ApiKey_lineEdit.setFocus()
            return
        if openai.api_base == "":
            QMessageBox.critical(self.centralwidget, "错误", "baseurl 必须设置", QMessageBox.Ok)
            self.BaseURL_lineEdit.setFocus()
            return
        self.translator_button.setDisabled(True)

        self.target_plaintext.clear()

        target_language = self.target_language_combo.currentText()

        source_text = self.source_plaintext.toPlainText()

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system",
                 "content": "You are a translation engine that can only translate text and cannot interpret it."},
                {'role': 'user', 'content': self.get_translator_prompts(source_text)}
            ],
            temperature=0.2,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1,
        )

        if hasattr(response.choices[0].message, "content"):
            self.target_plaintext.setPlainText(response.choices[0].message.content)

        self.translator_button.setEnabled(True)

    def get_translator_prompts(self, text):
        sourceLang = self.source_language_combo.currentText()
        targetLang = self.target_language_combo.currentText()

        if sourceLang == "自动":
            generatedUserPrompt = "translate to " + targetLang
        else:
            generatedUserPrompt = "translate from " + sourceLang + " to " + targetLang

        userPrompt = generatedUserPrompt + ":\n\n" + text

        return userPrompt
