import os
from Ulog import ULog
import csv


try:
    os.mkdir('Csv')
    os.mkdir('Maps')
except:
    pass
path = r"5 (2). Глушение GPS\10.08.2023 (2)"


def new_files(i_type, i_dir, o_type, o_dir):
    inp_files = [i.split('\\')[-1].split('.')[0] for i in os.listdir(f'{i_dir}') if i.endswith(f'{i_type}')]
    out_files = [i.split('\\')[-1].split('.')[0] for i in os.listdir(f'{o_dir}') if i.endswith(f'{o_type}')]
    files = []
    for i in inp_files:
        if i in out_files:
            inp_files.remove(i)
        else:
            files.append(f'{i_dir}\\{i}{i_type}')
    return files

            
def ulg_unpack(path, out):
    source = ['lat', 'lon', 'rssi', 'noise', 'remote_noise', 'rxerrors', 'fix']
    ulog = ULog(path, None, False)
    data = ulog.data_list
    header = []
    result = {}
    data.sort(key=lambda x: x.name)
    maxlen = 0
    for d in data:
        names = [f.field_name for f in d.field_data]
        names.remove('timestamp')
        names.insert(0, 'timestamp')
        for head in names:
            if head in source:
                if (d.name + '.' + head) not in header: header.append(d.name + '.' + head)
        if len(d.data['timestamp']) > maxlen:
            maxlen = len(d.data['timestamp'])

    for d in data:
        d_keys = [f.field_name for f in d.field_data]
        d_keys.remove('timestamp')
        d_keys.insert(0, 'timestamp')
        for key in d_keys:
            result[d.name + '.' + key] = d.data[key]
    
    
    with open(f'Csv\\{out}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for i in range(maxlen):
            row = []
            for head in header:
                if i < len(result[head]):
                    row.append(result[head][i])
                else:
                    row.append('')
            writer.writerow(row)


files = new_files('.ulg', path, '.csv', 'Csv')

n = 0
for path in files:
    print(path, n)
    ulg_unpack(path, path.split('\\')[-1].split('.')[0])
    n+=1
    print(f'{path} unpacked')
else:
    print('New log files not found')