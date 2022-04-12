import os
import zipfile
import base64
from random import randint
import shutil

# этот класс принимает изображение подписи клиента в base64 и путь к файлу, в котором нужно заменить картинку подписи
class ReplaceImage:
    def __init__(self, imgdata, filename):
        self.__main(imgdata, filename)

    # данная функция архивирует директорию в docx файл
    # принимает директорию для архивации и output директорию (в нашем случае docs/название_файла.docx)
    def __zip_directory(self, folder_path, zip_path):
        with zipfile.ZipFile(zip_path, mode='w') as zipf:
            len_dir_path = len(folder_path)
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, file_path[len_dir_path:])

    # главная функция. Принимает base64 и путь к нужному файлу
    # в ней мы открываем сгенерированный docx как архив, распаковываем его во временную папку temp с рандомным названием
    # с помощью модуля base64 декодируем изображение
    # в распакованном "архиве", который раньше был docx, находим файл image1.png -- шаблонную подпись
    # заменяем image1.png на изображение, полученное после декодинга base64
    # архивируем директорию обратно в docx файл, кидаем его с заменой в директорию docs
    # удаляем временную директорию из папки temp
    def __main(self, imgdata, filename):
        with zipfile.ZipFile(filename, 'a') as zip:
            temp_dirname = 'temp_' + str(randint(100000000000000, 999999999999999)) + '_unzip'
            zip.extractall('temp/' + temp_dirname)

            png_recovered = base64.b64decode(imgdata)

            with open(f"temp/{temp_dirname}/word/media/image1.png", "wb") as f:
                f.write(png_recovered)

            self.__zip_directory('temp/' + temp_dirname, filename)
            shutil.rmtree('temp/' + temp_dirname, ignore_errors=True)