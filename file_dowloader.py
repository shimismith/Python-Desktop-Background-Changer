import urllib.request
from datetime import datetime, timedelta
import os

def get_file(num):
    date = datetime.now() - timedelta(days=num)


    url = 'https://apod.nasa.gov/apod/ap' + str(date.year)[2:] + _fix_date(date.month) + _fix_date(date.day) + '.html'

    data = urllib.request.urlopen(url).read()

    check_bytes = bytes('<a href="image', 'utf-8')
    image = ""

    for i in range(len(data)):
        if data[i:i + len(check_bytes)] == check_bytes:
            image = _get_image_name(data, i + len(check_bytes) - len('image'))
            break

    image_url = 'https://apod.nasa.gov/apod/' + image  # the url to the image
    image_name = image.split('/')[-1]  # name of the image

    image_data = urllib.request.urlopen(image_url)

    image_path = "/Users/shimismith/Desktop/" + image_name
    with open(image_path, 'wb') as output:
        output.write(image_data.read())

    change_background_mac(image_path)

def _fix_date(date):
    """adds 0 infront of single digit numbers"""

    return '0' + str(date) if len(str(date)) == 1 else str(date)


def _get_image_name(data, i):
    """gets the name of the image starting at location i"""
    end_byte = bytes('"', 'utf-8')[0]
    end_num = i

    for byte in data[i:]:
        if byte == end_byte:
            break
        end_num += 1

    # the full url of the image
    return str(data[i:end_num])[2:-1]  #[2:-1] removes an unecessary 'b' and quotations


def change_background_mac(path):
    cmd =  """osascript -e 'tell application "Finder" to set desktop picture to POSIX file""" + '"' + path + """"'"""
    os.system(cmd)


if __name__ == '__main__':
    get_file(1)
