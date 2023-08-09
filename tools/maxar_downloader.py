import os
import shutil
from urllib import request, error
import progressbar
import sys

links_files = []

image_type = 'ms'

pbar = None

def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

for links_file in links_files:
    event = links_file.split('-')[1].split('.')[0]
    print(('Fetch {} Data of Event {} from MAXAR Open Data Program (Powered by Amazon Web Services)').format(image_type, event))
    # Create Event Folder
    event_folder = './maxar_data/' + event
    if os.path.exists(event_folder):
        shutil.rmtree(event_folder)
    os.mkdir(event_folder)

    # Download Data
    f = open('./maxar_data/'+links_file)
    lines = f.readlines()
    f.close()
    for line in lines:
        # Interpret Origin Link
        link = line.strip()
        quadkey = link.split('/')[7]
        time = link.split('/')[8]
        category_id = link.split('/')[9].split('-')[0]

        # Link to be Downloaded
        image_link = link.replace(category_id+'-visual', category_id+'-ms')
        meta_link = link.replace(category_id+'-visual.tif', category_id+'.json')

        # Download File Name
        image_name = event_folder + '/' + time + '_' + quadkey + '_' + category_id + '-ms.tif'
        meta_name = event_folder + '/' + time + '_' + quadkey + '_' + category_id + '-ms.json'

        print('downloading: {} and corresponding meta file'.format(image_link))
        # Down Image
        try:
            request.urlretrieve(image_link, image_name, show_progress)
        except error.HTTPError as e:
            print(e)
            print('\r\n' + image_link + 'Download Failed!' + '\r\n')
        # Down Meta
        try:
            request.urlretrieve(meta_link, meta_name, show_progress)
        except error.HTTPError as e:
            print(e)
            print('\r\n' + meta_link + 'Download Failed!' + '\r\n')


