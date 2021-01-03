import numpy as np, pandas as pd
import os, re, requests, demjson,urllib, argparse
from bs4 import BeautifulSoup


def main(f_url_list='url_list.txt', dir_out=None):
    if dir_out is None: 
        import time
        dir_out=f'metadata_{int(time.time())}'
    try:
        os.mkdir(dir_out)
    except FileExistsError:
        pass
    f_meta_out=os.path.join(dir_out, 'metadata.txt')
    f_meta=open(f_meta_out,'w+')
    # douban format: 
    fields=['album', 'barcode', 'album', 'album-alt', 'artist', 'genre', 'release-type', 'media', 'date', 'label', 'number_of_disc', 'isrc', 'tracks', 'description']
    sep='='*50 + '\n'
    f_meta.write(f"# {','.join(fields)} \n")
    f_meta.write(sep)
    
    with open(f_url_list,'r') as f_url:
        for url in f_url:
            print(f'Processing {url}')
            try:
                meta=get_metadata(url.strip())
            except Exception as e:
                print(f"Get metadata failed.")
                continue
            # Save metadata line by line
            f_meta.write(url+'\n')
            for field in fields:
                try:
                    content=meta[field]
                    if field=='tracks':
                        content='\n'.join([f'{i+1}. {track}' for i, track in enumerate(content)])
                        content='*** TRACKLIST ***\n'+content
                    elif field=='description':
                        content='*** DESCRIPTION ***\n'+content
                except KeyError:
                    content=f"*{field} MISSING*"
                f_meta.write(content+'\n')
            f_meta.write(sep)

            # Save cover image
            try:
                f_cover=os.path.join(dir_out, f"{meta['album']} - {meta['artist']}.{meta['img_url'].split('.')[-1]}")
                save_image(meta['img_url'],f_cover)
            except:
                print(f"Download cover failed")
    f_meta.close()        


def save_image(url, fout):
    # Save image
    with open(fout,'wb') as f:
        f.write(requests.get(url).content)

def get_metadata(url):
    site=re.findall(r'\.(.+)\.com',url)[0]
    if site=='bandcamp':
        return get_bandcamp_metadata(url)
    elif site=='discogs':
        return get_discogs_metadata(url)
    elif site=='apple':
        return get_apple_metadata(url)
    elif site=='amazon':
        return get_amazon_metatdata(url)

def get_bandcamp_metadata(url):
    req=requests.get(url)
    soup=BeautifulSoup(req.text,'html.parser')

    out={}
    out['album']=soup.find(id='name-section').find('h2').text.strip()
    out['artist']=soup.find(id='name-section').find('h3').text[2:].strip()
    out['img_url']=soup.find(id='tralbumArt').find('img').attrs['src']
    out['tracks']=pd.read_html(str(soup.find(id='track_table')))[0][2].to_list()
    out['description']=soup.find(class_='tralbumData tralbum-about').text.strip()
    out['date']=soup.find(class_='tralbumData tralbum-credits').text.strip().split('\n')[0].replace('released ','') # TODO: format this
    # spl=re.split(r'[, ]',out['_date'])
    # spl.remove('')
    # out['month'],out['day'],out['year']=spl
    out['label']='Self-Released' # bandcamp album page generally don't have label info

    return out


def get_discogs_metadata(url):
    url_types=['master','release']
    ps=[r'/master/(\d+)',r'/release/(\d+)']
    api_urls=['https://api.discogs.com/masters/%s', 'https://api.discogs.com/releases/%s']
    for url_type,p, api_url in zip(url_types,ps, api_urls):
        _id=re.findall(p,url)
        if len(_id)!=0:
            js=requests.get(api_url % _id[0]).json()
            if url_type=='master':
                js=requests.get(js['main_release_url']).json()
            break
    req=requests.get(url)
    soup=BeautifulSoup(req.text,'html.parser') # Get image link from this

    out={}
    out['album']=js['title']
    out['artist']=js['artists'][0]['name'] # TODO: multiple artists
    out['img_url']= soup.find(class_='thumbnail_center').find('img').attrs['src'] # TODO: this is a shrinked thumbnail image
    out['tracks']=[tk['title']+' '+tk['duration'] for tk in js['tracklist']] #  TODO: custum track # (A1, A2...)
    try:
        out['description']=js['notes']
    except KeyError:
        out['description']=''
    out['date']=js['released']   
    # out['month'],out['day'],out['year']=out['_date'].split('-')
    out['label']=js['labels'][0]['name'] 

    return out

def get_apple_metadata(url):
    # TODO
    pass


if __name__=='__main__':
    parser=argparse.ArgumentParser(description="Fetching album metadata")
    parser.add_argument("-i","--input", action='store',dest='f_url_list',default='url_list.txt',help="Input file path")
    parser.add_argument('-o','--output',action='store',dest='dir_out',default=None )

    result=parser.parse_args()
    main(result.f_url_list, result.dir_out)
