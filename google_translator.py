# -*- coding: cp950 -*-
from googletrans import Translator

#translator = Translator()
translator = Translator(service_urls=['translate.googleapis.com'])
print(translator.translate('測試').text)