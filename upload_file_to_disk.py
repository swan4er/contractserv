import yadisk
from docx2pdf import convert

YADISK_TOKEN = 'AQAAAABa9ubJAAfPJYDqFQjhe08mvBqS8dk8Hb4'

# эта функция используется для загрузки файлов на ядиск
# она принимает путь до docx файла, создает папку для пользователя, создает подпапки под docx и pdf
# грузит docx файл в нужную папку, затем конвертирует docx в pdf и грузит pdf в нужную папку
# в ответе отдает прямую ссылку на папку в яд
class UploadFile:

    # docx_path -- путь до файла docx на диске сервера: doc/file.docx. Нужен для того, чтобы показать ЯД, откуда и какой загрузить файл
    # yadisk_folder -- путь до новой папки на ЯД. Если такой папки нет, то ЯД её создает. doc/рандомный ид_ФИО (дата)
    # docx_name -- название файла. file.docx. Название мы конкатенируем к пути папки, чтобы получился полный путь до файла
    # в этой же функции конвертируем файлы в pdf и грузим на яд
    # для этого берем docx пути и имена, и заменяем их на .pdf, после чего вызываем общую функцию загрузки
    def upload(self, docx_path, docx_name, yadisk_folder):
        y = yadisk.YaDisk(token=YADISK_TOKEN)

        # сначала создеём одну общую папку. Пример: "doc/1234_Иванов Иван Иванович (11.04.2022)"
        # затем создаем подпапки /docx и /pdf и публикуем их
        y.mkdir(yadisk_folder)
        y.mkdir(yadisk_folder + '/docx')
        #y.publish(yadisk_folder + '/docx')

        y.mkdir(yadisk_folder + '/pdf')
        #y.publish(yadisk_folder + '/pdf')
        y.publish(yadisk_folder)

        # загружаем docx в doc/docx
        self.__upload(y, docx_path, yadisk_folder, '/docx', docx_name)

        # в путях к docx меняем все .docx на .pdf, чтобы получились пути для pdf файла
        # после чего конвертируем docx в pdf
        pdf_path = docx_path.replace('.docx', '.pdf')
        pdf_name = docx_name.replace('.docx', '.pdf')
        convert(docx_path, pdf_path)

        # загружаем pdf в doc/pdf
        self.__upload(y, pdf_path, yadisk_folder, '/pdf', pdf_name)

        # возвращаем ссылку на скачивание папки
        # по какой-то причине апи отказывается находить папку по созданному пути, хотя в print все отображается
        # return y.get_public_download_link(yadisk_folder) -- ???
        # поэтому используем всю мощь listdir, получаем список всех доков, и ищем по имени нашу сгенерированную папку
        # если нашли папку, то граббим публичную ссылку и возвращаем её
        download_url = ''
        for i in y.listdir('docs'):
            if i['name'] in yadisk_folder:
                download_url = i['public_url']
        return download_url

    # эта функция загружает нужные файлы на ядиск
    # принимает объект ядиска; путь до нужного файла, который нужно загрузить; путь до папки, куда загрузить; формат файла; название файла;
    def __upload(self, y, path, yadisk_folder, format_dir, doc_name):
        y.upload(path, yadisk_folder + format_dir + '/' + doc_name)