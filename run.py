'''
Name       : Download Apk Pure
Author     : Pandas ID
Blog       : https://pandasid.blogspot.com
Deskription: Silahkan kalian pelajari
'''

BANNER = '''
    █▀█ ▄▀█ █▄ █ █▀▄ ▄▀█ █▀
    █▀▀ █▀█ █ ▀█ █▄▀ █▀█ ▄█
    -----------------------
      Apk Pure Downloader
    -----------------------
'''
URL = 'https://m.apkpure.com'
CHUNK = 1024


def get_data(query):
    data = []
    res = rq.get(URL+'/id/search?q='+query).text
    parse = bs(res, 'html.parser')
    name = parse.find_all('p', class_='p1')
    dev = parse.find_all('p', class_='p2')
    href = parse.find_all('a', class_='dd')
    for x,y,z in zip(name, dev, href):
        data.append({'name':x.text, 'dev':y.text, 'url':URL+z.get('href')+'/download?from=details'})
    return data

def download(url, apk_name):
    dat = rq.get(url, stream=True)
    size = int(dat.headers.get('Content-Length'))
    print(f'\n    -! Ukuran File: {str(size)} KB')
    kon = input('    -? Yakin Ingin Mendownload [y/t]: ').lower()
    if kon == 'y':
        print()
        load = tqdm(total=size, unit='KB')
        with open('/sdcard/'+apk_name+'.apk', 'wb') as files:
            for data in dat.iter_content(chunk_size=CHUNK):
                files.write(data)
                load.update(len(data))
        load.close()
        print('    -! File Apk Tesimpan di Internal/'+apk_name)
    elif kon == 't':
        pass
    else:
        print('    -! Mohon masukan pilihan')
        download(url, apk_name)

def get_url(url):
    res = rq.get(url).text
    parse = bs(res, 'html.parser')
    href = parse.find('a', class_='ga')['href']
    return href

def main():
    os.system('clear')
    print(BANNER)
    try:
        query = input('    -? Query: ')
        data = get_data(query)
        if len(data) != 0:
            for show,num in zip(data,range(len(data))):
                print(f"\n{str(num+1)}.)\nNama: {show['name']}\nDeveloper: {show['dev']}")

            sel = int(input('\n    -? Pilih: '))
            try:
                download(get_url(data[sel-1]['url']), data[sel-1]['name'])
            except IndexError:
                input('    -! Index Tidak Ditemukan')
                main()
        else:
            input('    -! Query tidak ditemukan')
            main()
    except KeyboardInterrupt:
        pass
    except IOError:
        pass
    print('    -! Terima kasih telah menggunakan Tools unfaedah kami:v')
    print('    -! Jangan lupa untuk mengunjungi blog kami: https://pandasid.blogspot.com');exit()

if __name__ == '__main__':
    from bs4 import BeautifulSoup as bs
    from tqdm import tqdm
    import requests as rq
    import os
    main()
