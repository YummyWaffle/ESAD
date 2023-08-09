import os
import shutil
from tqdm import tqdm

proc_events = ['emilia_romagna_flooding', 'tonga_volcano']

for event in proc_events:
    event_dir = './maxar_data/' + event
    event_times = []
    filenames = os.listdir(event_dir)
    filenames = list(filter(lambda x: '.tif' in x, filenames))

    for filename in filenames:
        time = filename.split('_')[0]
        if time not in event_times:
            event_times.append(time)

    for time in event_times:
        if os.path.exists(event_dir + '/' + time):
            shutil.rmtree(event_dir + '/' + time)
        os.mkdir(event_dir + '/' + time)

    for filename in tqdm(filenames):
        time = filename.split('_')[0]
        ori_img = event_dir + '/' + filename
        ori_meta = event_dir + '/' + filename.split('.')[0] + '.json'
        dst_img = event_dir + '/' + time + '/' + filename
        dst_meta =event_dir + '/' + time + '/' + filename.split('.')[0] + '.json'
        shutil.move(ori_img, dst_img)
        shutil.move(ori_meta, dst_meta)