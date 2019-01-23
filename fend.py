#!/usr/bin/env python
import os
import sys
import errno
import shutil
import ctypes
import urllib
import argparse
import requests
import urllib.request
from io import BytesIO
from zipfile import ZipFile
from django.conf import settings
from urllib.request import urlopen

# GLOBAL SETTINGS
cwd = os.getcwd()
path_setting = str((os.path.basename(cwd)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', path_setting+'.settings')
Base_temp = os.path.join(settings.BASE_DIR, '.fend')
BASE_URL = "https://s3.amazonaws.com/dangofend/"

# module_global_variable
templates = "templates"
static_clone = os.path.join(settings.BASE_DIR, '.fend\static')
templates_clone = os.path.join(settings.BASE_DIR, '.fend\\templates')

# REQUEST CALL TO TEMPLATE OPTIONS SERVER
response = requests.get("https://s3.amazonaws.com/dangofend/templates.txt")
template_options = response.text
##@@ arrparser@@@###
parser = argparse.ArgumentParser(description='Choose your template')
parser.add_argument('template_name', type=str,
                    help='Type in the name of the template you would like to use, currently available Options are:  {}'.format(
                        template_options))
args = parser.parse_args()

print(args.template_name)

# URL TO TEMPLATE SERVER
resp = urlopen(BASE_URL + args.template_name + ".zip")

# Downloader
try:
    with ZipFile(BytesIO(resp.read())) as template_file:
        # create folder .fend and download the desired template
        # For windows set file attribute.
        print("Creating Template folder............................")
        if os.path.exists(Base_temp):
            print(Base_temp + " already exists, deleting .fend folder")
            shutil.rmtree(Base_temp)

        if not os.path.exists(Base_temp):
            os.makedirs(Base_temp)
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ret = ctypes.windll.kernel32.SetFileAttributesW(Base_temp, FILE_ATTRIBUTE_HIDDEN)
            print("Template Folder Creation Successful............................")
            os.chdir(Base_temp)

            template_file.extractall(Base_temp)
            print("Template Downloading and Creation Complete............................")

except Exception as errors:
    print(errors)

# # File or folder Finder


def getSubdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


st_dir = getSubdirectories(settings.BASE_DIR)


# 
# # Path_finder and creator
def find(name, path):
    try:
        for obj in name:
            for root, dirs, files in os.walk(path):
                if obj in dirs:
                    dir = os.path.join(root, obj)
                    if not os.path.isdir(os.path.join(dir, obj)):
                        path_off = str((os.path.basename(dir)))
                        path_off1 = str(settings.ROOT_URLCONF.split(".")[0])
                        if path_off == ".fend" or path_off ==".git" or path_off == path_off1:
                            pass

                        else:
                            try:
                                os.chdir(dir)
                                os.makedirs('static')
                                os.makedirs('templates')
                                print("static and template folder created to " + dir + " successfully")

                            except OSError as errors:
                                if errors.errno != errno.EEXIST:
                                    print (errors)
                    else:
                        print(os.path.join(dir, obj) + " already exist")

    except Exception as error:
        print(error)


find(getSubdirectories(settings.BASE_DIR), settings.BASE_DIR)


# static_cloner
def staticCopy(src, dst, symlinks=False, ignore=None):
    for obj in dst:
        target = os.path.join(settings.BASE_DIR, obj + '\\static')

        try:
            path_off = str((os.path.basename(obj)))
            path_off1 = str(settings.ROOT_URLCONF.split(".")[0])

            if path_off == ".fend" or path_off ==".git" or path_off == path_off1:
                pass
            elif not len(os.listdir(target)) == 0:
                print("Static Files found in {}".format(path_off))

            else:
                for item in os.listdir(src):
                    s = os.path.join(src, item)
                    d = os.path.join(target, item)
                    if os.path.isdir(s):
                        print ("Copying file: %s" % s)
                        shutil.copytree(s, d, symlinks, ignore)
                    else:
                        print ("Copying file: %s" % s)
                        shutil.copy2(s, d)
        except Exception as error:
            print(error)


staticCopy(static_clone, st_dir)


# Template_cloner
def templatesCopy(src, dst):
    for obj in dst:
        target = os.path.join(settings.BASE_DIR, obj + '\\templates')
        print(target)

        try:
            path_off = str((os.path.basename(obj)))
            path_off1 = str(settings.ROOT_URLCONF.split(".")[0])

            if path_off == ".fend" or path_off ==".git" or path_off == path_off1:
                pass
            elif not len(os.listdir(target)) == 0:
                print("Template Files found in {}".format(path_off))

            else:
                for item in os.listdir(src):
                    s = os.path.join(src, item)
                    d = os.path.join(target, item)
                    if os.path.isdir(s):
                        print ("Copying file: %s" % s)
                        shutil.copytree(s, d)
                    else:
                        print ("Copying file: %s" % s)
                        shutil.copy2(s, d)
        except Exception as error:
            print(error)


templatesCopy(templates_clone, st_dir)
