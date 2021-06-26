import traceback
import json
import os, sys, time
import uuid
####################################
def configurationReader():
  try:
    settings = {}
    f = open('config', 'r')
    mode = f.readline().strip()
    print('MITTARISTO BACKEND APPLICATION RUNNING IN MODE: ', mode)
    configuration = json.load(open("app_config.json", "r"))
    for key, value in configuration.items():
      if key == mode:
        settings['APP_DB_USER'] = value['DB_USER']
        settings['APP_DB_PWD'] = value['DB_PWD']
        settings['APP_DB_NAME'] = value['DB_NAME']
        settings['APP_DB_PORT'] = value['DB_PORT']
        settings['APP_DB_HOST'] = value['DB_HOST']
        settings['APP_OS_PWD'] = value['OS_PWD']
        settings['APP_OS_REPORT_DIR'] = value['OS_REPORT_DIR']
        settings['APP_FE_URL'] = value['APP_FE_URL']
        settings['APP_BE_PUBLIC_IP'] = value['APP_BE_PUBLIC_IP']
        settings['APP_BE_LOCAL_IP'] = value['APP_BE_LOCAL_IP']
        settings['APP_BE_PUBLIC_PORT'] = value['APP_BE_PUBLIC_PORT']
        settings['APP_BE_LOCAL_PORT'] = value['APP_BE_LOCAL_PORT']
        settings['MAIL'] = False
        if "prod" in key:
            settings['MAIL'] = True
        # print('APP_FE_URL: ', APP_FE_URL)
        return settings
  except:
    print(traceback.format_exc())
    print("Config file not found. Mode - test")
