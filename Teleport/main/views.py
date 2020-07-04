from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import zipfile
import os
import shutil

@csrf_exempt
def index(request):
    if request.FILES:
        date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        os.mkdir(date)
        for i in range(len(request.FILES)):
            if len(request.FILES) == 1:
                file_name = f'main/static/files/{date} {list(request.FILES)[i]}'
            else:
                file_name = f'{date}/{list(request.FILES)[i]}'
            with open(file_name, 'wb+') as destination:
                for chunk in list(request.FILES.values())[i].chunks():
                    destination.write(chunk)
        if len(request.FILES) != 1:
            with zipfile.ZipFile(f'{date}.zip', 'w') as zip_file:
                for file in request.FILES:
                    zip_file.write(f'{date}/{file}')
            shutil.move(f'{date}.zip', f'main/static/files/{date}.zip')
        shutil.rmtree(date)

    files = []
    file_names = sorted(os.listdir('main/static/files/'))
    file_names.reverse()
    for file_name in file_names:
        try:
            if file_name[19:].find(' ') != -1:
                name = file_name[20:]
            else:
                name = file_name
            date = file_name[:11] + file_name[11:19].replace('-', ':')
            size = os.path.getsize(f'main/static/files/{file_name}')
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1000:
                    size = f'{round(size, 2)} {unit}'
                    break
                else:
                    size /= 1000
            files.append([file_name, name, size, date])
        except:
            pass
    return render(request, 'index.html', {'files': files})
