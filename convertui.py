import os
from pathlib import Path


def convertui(path_to_start_file, output_name='sceleton'):
    '''Конвертирует все .ui файлы в папке, в которой был запущен в sceleton.py файлы'''
    my_folder = Path(path_to_start_file).resolve().parent
    files = os.listdir(str(my_folder))

    for filename in files:
        if filename.split('.')[-1] == 'ui':
            path_to_file = my_folder / filename

            errors = os.system(f'pyuic5 {str(path_to_file)} -o {str(my_folder / f"{output_name}.py")}')
            if errors == 0:
                
                # Дальше из конвертированного файла вырезаются комментарии. 
                # Дело в том, что комментарии в начале включают в себя путь к файлу, из которого было сделано преобразование
                # Так что если просто перезапускать проект на разных устройствах, комментарии немного меняются и git отмечает файл как изменённый, хотя суть файла вообще не изменилась

                with open(str(str(my_folder / f"{output_name}.py")), 'r', encoding='utf-8') as pyfile:
                    data = pyfile.read()
                
                data = data.split('\n')
                for i in range(len(data)-1, 0-1, -1):
                    if data[i].startswith('#'):
                        data.pop(i)
                
                for _ in range(0, len(data)):
                    if data[0] == '':
                        data.pop(0)
                    else:
                        break
                
                data = '\n'.join(data)

                with open(str(str(my_folder / f"{output_name}.py")), 'w', encoding='utf-8') as pyfile:
                    data = pyfile.write(data)
                
                print(f'Конвертировано {filename}')

            else:
                print(f'Не удалось сконвертировать {filename}, ошибка: ', errors)