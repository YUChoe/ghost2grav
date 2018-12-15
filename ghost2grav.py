import json
import os
import datetime
import jinja2 
import re
import sys

__version__ = '3'

slug_regex = re.compile('[^A-Za-z0-9_-]')

def slug_filter(id, title):
    rval = slug_regex.sub('', title)
    rval = rval.replace('--', '-').replace('__', '_') 
    if len(rval) > 0 and rval[0] in ['-', '_']:
        rval = rval[1:]
    if len(rval) > 0 and rval[-1] in ['-', '_']:
        rval = rval[:-1]
    if rval:
        return '--'.join([str(id), rval])
    else:
        return str(id)

url_regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
def urlify2(value):
    return value
    # buggy !!!
    # return url_regex.sub(r"[\g<0>](\g<0>)", value)
    
def get_tag_index_from_json_data(json_data):
    tag_temp = {}
    tag_index = {}        
    for tag in json_data['data']['tags']:
        tag_temp[int(tag['id'])] = tag['name']
        # print(tag['id'], tag['name'])
    
    for tag in json_data['data']['posts_tags']:
        if 'tag_id' not in tag:
            continue
        if tag['post_id'] in tag_index: 
            old_list = tag_index[tag['post_id']]
            tag_id = int(tag['tag_id'])
            old_list.append(tag_temp[tag_id])
            tag_index[tag['post_id']] = old_list
        else:
            tag_id = int(tag['tag_id'])
            tag_index[tag['post_id']] = [tag_temp[tag_id]]
    return tag_index
            
def main(fname, template_fname):
    if os.path.isfile(fname) and os.path.isfile(template_fname):

        with open(template_fname) as fp:
            template = jinja2.Template(fp.read())

        with open(fname, encoding="utf-8") as fp:
            json_data = json.load(fp) 
            # { 'meta': ... , 
            #   'data': {
            #     'posts': ..., 
            #     'tags': ..., 
            #     'posts_tags', ... 
            #   }
            # }
            tag_index = get_tag_index_from_json_data(json_data)
            
            for post in json_data['data']['posts']:
                # updated_by, id, created_at, status, slug, language, meta_title, updated_at, meta_description, page, published_at, created_by, markdown, html, featured, image, title, published_by
                rpost = {}
                rpost['title'] = post['title']
                rpost['created_at'] = datetime.datetime.fromtimestamp(post['created_at'] / 1000).strftime("%H:%M %m/%d/%Y")
                rpost['published'] = 'false' if post['status'] == 'draft' else 'true'
                # updated_at = datetime.datetime.fromtimestamp(post['updated_at'] / 1000)
                rpost['tags'] = tag_index[post['id']] if post['id'] in tag_index else []
                # print(post['status'], created_at, updated_at, post['title'], tags)
                rpost['markdown'] = urlify2(post['markdown'])
                # print(rpost['markdown'])
                
                _dist_dir = os.path.join('.', 'dist')
                os.makedirs(_dist_dir, exist_ok=True)

                os.makedirs(os.path.join(_dist_dir, slug_filter(post['id'], post['title'])), exist_ok=True)
                with open(os.path.join(_dist_dir, slug_filter(post['id'], post['title']), 'item.md'), 'w') as wf:
                    content = template.render(rpost)
                    wf.write(content)
    else:
        print('Error:', 'File not found.', fname)  # , 'or', template_fname)

def print_usage():
    print('Usage:', sys.argv[0], '<ghost.json>')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(fname=sys.argv[1], template_fname='templates/blog_post.md')
    else:
        print_usage()
    