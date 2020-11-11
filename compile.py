import os
import shutil
import json

from jinja2 import Environment, FileSystemLoader
from csscompressor import compress as css_minifier
from jsmin import jsmin as js_minifier
from htmlmin import minify as html_minifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JINJA_ENV = Environment(loader=FileSystemLoader(f'{BASE_DIR}/sources/templates'))


def minify_css(css):
    return css_minifier(css)


def minify_js(js):
    return js_minifier(js, quote_chars="'\"`")


def minify_html(html):
    return html_minifier(html).replace('> <', '><')


def get_minified_css(relative_file_path):
    with open(os.path.join(BASE_DIR, 'sources/css', relative_file_path)) as f:
        raw = f.read()
    return minify_css(raw)


def get_minified_js(relative_file_path):
    with open(os.path.join(BASE_DIR, 'sources/js', relative_file_path)) as f:
        raw = f.read()
    return minify_js(raw)


def get_parameter(relative_file_path):
    with open(os.path.join(BASE_DIR, 'sources/params', relative_file_path)) as f:
        json_data = json.load(f)
    return json_data


def dict_update(*args):
    result = {}
    for arg in args:
        result.update(arg)
    return result


def dump(source, relative_file_path):
    with open(os.path.join(BASE_DIR, 'public', relative_file_path), 'w') as f:
        f.write(source)


if __name__ == '__main__':
    try:
        shutil.rmtree('./public')
    except FileNotFoundError:
        pass

    os.mkdir(os.path.join(BASE_DIR, 'public'))

    source_image_dir = os.path.join(BASE_DIR, 'sources', 'image')
    public_image_dir = os.path.join(BASE_DIR, 'public', 'image')
    os.system(f'cp -a {source_image_dir} {public_image_dir}')

    css = get_minified_css('style.css')
    js = get_minified_js('ga.js')

    profile_parameter = get_parameter('home/profile.json')

    static_soruce = {
        'external_css': css,
        'external_script': js,
    }

    params = dict_update(static_soruce, profile_parameter)

    html = JINJA_ENV.get_template('home/index.html').render(params)
    html = minify_html(html)

    dump(html, 'index.html')
