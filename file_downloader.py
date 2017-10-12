import urllib.request
from datetime import datetime, timedelta
import os
import platform
import shutil

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

    return image_name, image_data


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


def download_file(image_path, image_data):
    with open(image_path, 'wb') as output:
        output.write(image_data.read())


def change_background():
    get_file_error = False
    image_name, image_data = "", ""
    try:
        image_name, image_data = get_file(0)
    except:
        get_file_error = True

    if platform.system() == 'Darwin':
        try:
            if get_file_error:
                raise FileNotFoundError  # couldn't find the file online

            image_path = os.path.join(os.path.expanduser('~/Desktop/') + image_name)
            download_file(image_path, image_data)

            #changes the background
            cmd = """osascript -e 'tell application "Finder" to set desktop picture to POSIX file""" + '"' + image_path + """"'"""
            os.system(cmd)
        except:  # use default background
            image_path = "/Users/shimismith/PycharmProjects/DBC/default.png"
            cmd = """osascript -e 'tell application "Finder" to set desktop picture to POSIX file""" + '"' + image_path + """"'"""
            os.system(cmd)

    elif platform.system() == 'Linux':
        print("Sorry we don't do those (for now)")
    elif platform.system() == 'Windows':

        #===================getting the paths to dirs we needed==========================#
        image_path = os.path.join(os.path.expanduser('~\AppData\Roaming\Microsoft\Windows\Themes\ ')).strip()
        cachedFiles_path = image_path + 'CachedFiles\ '.strip()
        #============================================================================#
        download_file(image_path + image_name, image_data)

        if image_name[-3:] is not 'jpg':
            os.rename(image_path + image_name, image_path + image_name[:-3] + 'jpg')
            image_name = image_name[:-3] + 'jpg'

        abs_image_path = image_path + image_name

        cached_file = [f for f in os.listdir(cachedFiles_path) if f.endswith(".jpg")]
        for f in cached_file:
            os.remove(cachedFiles_path + f)

        shutil.copy2(abs_image_path, cachedFiles_path)
        cachedimage_path = cachedFiles_path + image_name

        try:
            os.remove(image_path + 'TranscodedWallpaper')
        except FileNotFoundError:
            pass
        os.rename(image_path + image_name, image_path + 'TranscodedWallpaper')

        reg_background = """reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ  /f /d """ \
                         + cachedimage_path

        os.system(reg_background)
        os.system('RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters SPI_SETDESKWALLPAPER, True' +
                  cachedimage_path + ' SPIF_UPDATEINIFILE')
    else:
        print("OS not supported!")


if __name__ == '__main__':
    change_background()
