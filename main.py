# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_cors import CORS
from tinydb import TinyDB, Query
import json
import re
from werkzeug.utils import secure_filename

from generate import CreateDocx
from upload_file_to_disk import UploadFile

# UPLOAD IMAGES
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


'''db = TinyDB('db/shift.json')
db.insert({'name': 'Сквозь время', 'description':'Рассмотрим любопытные исторические закономерности и эффекты общеизвестных событий, на которые не обращают внимания в школьном курсе. Сделаем это интересно и наглядно на моделях государств, которые ребята сами будут строить в течение смены. Научимся вести переговоры, строить доверительные деловые и личные отношения, работать в группах, лидировать и подчиняться в соответствующих ситуациях, мыслить стратегически, строить логические цепочки, принимать различные решения и отвечать за их последствия', 'isActive':True, 'thumbnail':'https://static.tildacdn.com/tild6137-3530-4261-a232-656433646537/image.png', 'dates': '4-10 июля', 'price':19900})
db.insert({'name': 'Мир после 3.0', 'description':'Научимся работать в команде и взаимодействовать в коллективе, освоим навыки планирования и тактического мышления, освоим навык ответственности за принятие сложных и неоднозначных решений. В рамках созданной нами вселенной, смоделируем сложные ситуации, каждая из которых будет испытанием, которое можно преодолеть только с опорой на себя и других, важно чтобы испытание прошло, как можно больше участников, ведь мир полон непредсказуемости.', 'isActive':True, 'thumbnail':'https://static.tildacdn.com/tild3463-6134-4133-b766-643531633435/Frame_45.png', 'dates': '11-17 июля', 'price':19400})
db.insert({'name': 'ЗакуЛесье 2022', 'description':'В игровой форме узнаем о тонкостях съёмочных процессов. Будем развивать коммуникативные навыки, учиться работать в команде, расширять кругозор, поймем на практике в чем заключается ответственность за себя, других и все что находится вокруг.', 'isActive':True, 'thumbnail':'https://static.tildacdn.com/tild3866-6431-4637-a161-333264356266/s3.png', 'dates': '18-24 июля', 'price':18900})
db.insert({'name': '7 дней сплава по реке', 'description':'Любимая часть похода для юных туристов — это сплав! Теперь у нас есть отличная возможность провести 7 дней в настоящем водном путешествии.', 'isActive':True, 'thumbnail':'https://static.tildacdn.com/tild3934-6534-4631-b237-313764393534/image_5.png', 'dates': '3-10 августа', 'price':17900})
db.insert({'name': 'Тайны следствия 2022', 'description':'Каждый день дети будем знакомиться с теорией методов научного познания, а далее использовать свои знания на практике. Узнаем основы юриспруденции, правоведения и психологии. Научимся некоторым методам шифрования.', 'isActive':True, 'thumbnail':'https://static.tildacdn.com/tild3461-3064-4934-b864-656439616666/image_4.png', 'dates': '25-31 августа', 'price':18400})
db.insert({'name': None, 'description':None, 'isActive':False, 'thumbnail':None, 'start': None, 'end': None, 'price':None})

db = TinyDB('db/sale.json')
db.insert({'name': 'Оплачу 100% при заключении договора', 'isActive': False, 'sale': 500})
db.insert({'name': 'Поедут двое друзей', 'isActive': True, 'sale': 500})
db.insert({'name': 'Уже есть страховка', 'isActive': True, 'sale': 400})
db.insert({'name': 'Ребенок участвует во второй раз', 'isActive': True, 'sale': 500})
db.insert({'name': 'Ребенок участвует в третий раз', 'isActive': False, 'sale': 1000})
db.insert({'name': 'Ребенок участвует в четвертый раз', 'isActive': False, 'sale': 1500})
#print(db.all())'''

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/getinfo", methods=['GET'])
def getinfo():
    shift_db = TinyDB('db/shift.json')
    sale_db = TinyDB('db/sale.json')
    return {'shifts': shift_db.all(), 'sales':sale_db.all()}

@app.route("/save", methods=['POST'])
def save():
    req = request.form  # берем данные из запроса

    shift_db = TinyDB('db/shift.json')
    sale_db = TinyDB('db/sale.json')
    shift_db.truncate()
    sale_db.truncate()

    with open('db/shift.json', 'w') as shift_db, open('db/sale.json', 'w') as sale_db:
        new_shifts = str(req['shifts'])
        new_sales = str(req['sales'])

        new_shifts = re.sub('"true"', 'true', new_shifts)
        new_sales = re.sub('"true"', 'true', new_sales)
        new_shifts = re.sub('"false"', 'false', new_shifts)
        new_sales = re.sub('"false"', 'false', new_sales)

        shift_db.write(new_shifts)
        sale_db.write(new_sales)

    return 'Удачно'

# обработчик запроса о генерации документов
# принимает json объект от браузера со страницы калькулятора
@app.route("/generate", methods=['POST'])
def generate():
    req = request.form # берем данные из запроса

    # print(req)
    # print(req['child_phone'])

    #try:
    # вызываем класс/модуль CreateDocx(), который генерирует док файл, и передаем в его метод create наш json
    # в ответе получаем путь до созданного файла
    docx_path, docx_name, yadisk_folder = CreateDocx().create(req)
    # вызываем класс/модуль UploadFile(), который загружает файл на ядиск, и передаем в его метод upload путь до файла
    # в ответ получаем ссылку на скачивание файла
    #print(UploadFile().upload(doc_path, doc_name, yadisk_folder))
    #except:
    #    print('Ошибка загрузки файла')
    #else:
    #    print('Файл успешно загружен')
    download_link = UploadFile().upload(docx_path, docx_name, yadisk_folder)
    return download_link

# файл на сервере будет находиться по адресу http://flask-contract/uploads/img.jpg
@app.route("/upload", methods=['POST'])
def upload():
    f = request.files['file']
    f.save(secure_filename(f.filename))
    print('http://flask-contract/uploads/' + secure_filename(f.filename))
    return 'file uploaded successfully'


app.run(port=8080)