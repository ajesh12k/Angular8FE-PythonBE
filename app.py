# coding=utf-8
import base64
import hashlib

from flask import Flask, render_template, session, escape, request, Response
from flask import url_for, redirect, send_from_directory
from flask import send_file, make_response, abort
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import json
import os, time
import glob
import urllib
import logging
from logging.handlers import RotatingFileHandler
import codecs
import uuid
import os, sys, time

# Needs installation on server
# ---------------------------------------------------------------------

# from flask_socketio import SocketIO
import xlsxwriter
# import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from openpyxl import load_workbook
from flask_mail import Mail
from flask_mail import Message
import traceback
##################################################

import settings

##################################################

os.environ['TZ'] = 'Europe/Helsinki'
parentdir = os.path.join(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
syspath = sys.path

from manager import DatabaseManager

app = Flask(__name__)

mail = Mail(app)
app.secret_key = "mtee_app"
#######################################
allLanguageList = {}
allStaticContent = {}
allQuestions = {}
allThemeNames = {}
allCountryList = {}
allErrorList = {}
allSuccessMessageList = {}
setting = {}

##################################

db = DatabaseManager()


def cacheAllData():
  global allLanguageList
  allLanguageList = db.getAllLanguage()
  # print(allLanguageList)
  # print('All language list cached .....')
  global allStaticContent
  allStaticContent = db.getAllStaticContent()
  # print(allStaticContent)
  # print('All static content cached .....')
  global allThemeNames
  allThemeNames = db.getQuestionThemeName()
  # print(allThemeNames)
  # print('All theme names catched ...')
  global allCountryList
  allCountryList = db.getCountryList()
  # print(allCountryList)
  # print('All country list cached .....')
  global allQuestions
  allQuestions = db.getQuestions()
  # print(allQuestions)
  # print('All Questions cached')
  global allErrorList
  allErrorList = db.getErrorList()
  # print('All Error list cached .....', str(allErrorList))
  global getSuccessMessageList
  allSuccessMessageList = db.getSuccessMessageList()
  # print('All Success message list cached .....', str(allSuccessMessageList))
  global setting
  setting = settings.configurationReader()


#######################################################
cacheAllData()
baseurl = setting['APP_BE_PUBLIC_IP']


#######################################################

@app.route('/')
def welcome():
  return redirect(baseurl, code=302)


#############################################

@app.route('/getAllLanguage', methods=['GET'])
def getAllLanguage():
  global allLanguageList
  reloadCheck = request.args.get('reload', False)
  if allLanguageList == {} or reloadCheck:
    # print("Getting all languages ............ ")
    allLanguageList = db.getAllLanguage()
  else:
    print("languages already available - {}".format(allLanguageList))
  return jsonify({'status': 'success', 'result': allLanguageList}), 200, {'Content-Type': 'application/json',
                                                                          'Access-Control-Allow-Origin': '*'}


#############################################

@app.route('/addLanguage', methods=['POST'])
def addLanguage():
  data = request.get_json(silent=True)
  mtee_country_code = data.get('mtee_country_code', None)
  mtee_country_display_name = data.get('mtee_country_display_name', None)
  mtee_language_code = data.get('mtee_language_code', None)
  mtee_language_display_name = data.get('mtee_language_display_name', None)
  mtee_language_display_seq = data.get('mtee_language_display_seq', None)
  mtee_language_status = data.get('mtee_language_status', None)
  if not mtee_country_code or not mtee_country_display_name or not mtee_language_code or not mtee_language_display_name or not mtee_language_display_seq or not mtee_language_status:
    return json.dumps({'status': 'failed', 'result': 'Incomplete details'})
  status = db.addLanguage(data)
  return jsonify({'status': 'success', 'result': status}), 200, {'Content-Type': 'application/json',
                                                                 'Access-Control-Allow-Origin': '*'}


#################################################

@app.route('/getSuccessMessageList', methods=['GET'])
def getSuccessMessageList():
  global allSuccessMessageList
  reloadCheck = request.args.get('reload', False)
  if allSuccessMessageList == {} or reloadCheck:
    # print("Getting all Success message List ............ ")
    allSuccessMessageList = db.getSuccessMessageList()
  # else:
  # print("Success message list already available - {}".format(allSuccessMessageList))
  return jsonify({'status': 'success', 'result': allSuccessMessageList}), 200, {'Content-Type': 'application/json',
                                                                                'Access-Control-Allow-Origin': '*'}


#############################################

@app.route('/getErrorList', methods=['GET'])
def getErrorList():
  global allErrorList
  reloadCheck = request.args.get('reload', False)
  if allErrorList == {} or reloadCheck:
    # print("Getting all Error List ............ ")
    allErrorList = db.getErrorList()
  # else:
  # print("Error list already available - {}".format(allErrorList))
  return jsonify({'status': 'success', 'result': allErrorList}), 200, {'Content-Type': 'application/json',
                                                                       'Access-Control-Allow-Origin': '*'}


#################################################
@app.route('/getAllStaticContent', methods=['GET'])
def getAllStaticContent():
  global allStaticContent
  reloadCheck = request.args.get('reload', False)
  if allStaticContent == {} or reloadCheck:
    # print("Getting all static content ............. ")
    allStaticContent = db.getAllStaticContent()
  else:
    print("Static content already available!")
  return jsonify({'status': 'success', 'result': allStaticContent}), 200, {'Content-Type': 'application/json',
                                                                           'Access-Control-Allow-Origin': '*'}


###############################################################

@app.route('/saveUserAccessDetails', methods=['POST', 'OPTIONS'])
def saveUserAccessDetails():
  requestData = json.loads(request.data)
  # print(requestData)
  mtee_user_access_details = requestData
  # print(mtee_user_access_details)
  uuidStatus = uuid.uuid1()
  unique_id = str(uuidStatus).replace("-", "")
  if request.headers.getlist("X-Forwarded-For"):
    mtee_user_access_ip = request.headers.getlist("X-Forwarded-For")[0]
  else:
    mtee_user_access_ip = request.remote_addr
  mtee_user_access_time = int(time.time())
  result = jsonify({'status': 'success',
                    'result': db.saveUserAccessDetails(mtee_user_access_details, unique_id, mtee_user_access_ip,
                                                       mtee_user_access_time)}), 200, {
             'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
  return result


##################################################

@app.route('/getUserAccessDetails', methods=['GET'])
def getUserAccessDetails():
  result = jsonify({'status': 'success', 'result': db.getUserAccessDetails()}), 200, {
    'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
  print(str(result))
  return result


##################################################


@app.route('/registerUser', methods=['OPTIONS', 'POST'])
def registerUser():
  # print('Inside registerUser -----'.format(request.data))
  requestData = json.loads(request.data)
  mtee_user_yob = requestData['mtee_user_yob']
  # print(mtee_user_yob)
  mtee_user_gender = requestData['mtee_user_gender']
  mtee_user_id = requestData['mtee_user_id']
  mtee_user_pwd = requestData['mtee_user_pwd']
  mtee_user_email = requestData['mtee_user_email']
  mtee_user_lang = requestData['mtee_user_lang']
  mtee_user_role = 'T'
  if mtee_user_id != None and mtee_user_pwd != None:
    url = baseurl + "/activate?user=" + mtee_user_id
    # print(url)
    # print(mtee_user_pwd)
    response = db.registerUser(mtee_user_yob, mtee_user_gender, mtee_user_id, mtee_user_pwd, mtee_user_email,
                               mtee_user_lang, mtee_user_role)
    responseDetails = response.json
    # print(responseDetails['status'])
    if responseDetails['status'] == 'success':
      recieverEmail = mtee_user_email
      recieverName = mtee_user_id
      msgContent = db.getUserMsg('userCreation', mtee_user_lang)
      body = msgContent['body']
      body = body.replace('recieverName', recieverName)
      body = body.replace('url', url)
      body = body.replace('base', baseurl)
      # print(body)
      msg = Message("Activate Your Account", sender="mittaristo@lut.fi", recipients=[recieverEmail])
      msg.body = body + "\n\n"
      # print msg
      if setting['MAIL'] == True:
        mail.send(msg)
    # print(responseDetails)
    return response, 200, {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}
  else:
    return {"status": "Failed to save user as data is incomplete!"}, 200, {'Content-Type': 'application/json',
                                                                           "Access-Control-Allow-Origin": "*"}


##################################################################################

@app.route('/validateUser', methods=['POST'])
def validateUser():
  # print('Inside registerUser -----'.format(request.data))
  requestData = json.loads(request.data)
  mtee_user_id = requestData['mtee_user_id']
  mtee_user_pwd = requestData['mtee_user_pwd']
  mtee_user_ip = request.remote_addr
  mtee_user_browser = request.user_agent
  if mtee_user_id != None and mtee_user_pwd != None:
    Response = db.validateUser(mtee_user_id, mtee_user_pwd, mtee_user_ip, mtee_user_browser)
    # print(Response.json)
    validate_user_res = Response.json
    if validate_user_res['status'] == 'success':
      session['mtee_user_id'] = mtee_user_id
      session['mtee_user_session_id'] = validate_user_res['sessionId']
      session['mtee_user_role'] = validate_user_res['result'][0]['mtee_user_role']
      session['mtee_user_lang'] = validate_user_res['result'][0]['mtee_user_lang']
      # print(validate_user_res)
      # print(session)
      return jsonify({'status': 'success', 'result': validate_user_res['result']}), 200, {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"}
    else:
      error = db.getMessage("100")
      return jsonify({'status': 'failed', 'result': error}), 200, {"Content-Type": "application/json",
                                                                   "Access-Control-Allow-Origin": "*"}
  else:
    error = db.getMessage("500")
    return jsonify({'status': 'failed', 'result': error}), 200, {"Content-Type": "application/json",
                                                                 "Access-Control-Allow-Origin": "*"}


#######################################################

@app.route('/activateUser', methods=['POST'])
def activateUser():
  user = request.json['user']
  print ('Activating ' + user)
  activate = db.activateUser(user)
  if activate['status'] == 'success':
    print(activate)
    return jsonify({"status": "success", "result": activate['result']}), 200, {'Content-Type': 'application/json',
                                                                               'Access-Control-Allow-Origin': '*'}
  else:
    return jsonify({"status": "failed", "result": "failed to activate"}), 200, {'Content-Type': 'application/json',
                                                                                'Access-Control-Allow-Origin': '*'}


#######################################################

@app.route('/resetPassword', methods=['POST'])
def forgotPassword():
  # print('Inside resetPassword -----'.format(request.data))
  requestData = json.loads(request.data)
  url = requestData['resettoken']
  print('URL : ' + url)
  userInfo = db.getForgotPasswordUser(url)
  print(userInfo)
  #    session['mtee_user_id'] = userInfo['user']
  return jsonify({"status": "success", "result": userInfo}), 200, {'Content-Type': 'application/json',
                                                                   'Access-Control-Allow-Origin': '*'}


#######################################################

@app.route('/updatepassword', methods=['POST'])
def updatepassword():
  # print('Inside updatepassword -----'.format(request.data))
  requestData = json.loads(request.data)
  resetToken = requestData['resettoken']
  password = requestData['password']
  print(resetToken)
  print(password)
  if not password:
    return jsonify({"status": "failed", "result": "Password empty"}), 200, {'Content-Type': 'application/json',
                                                                            'Access-Control-Allow-Origin': '*'}
  if not resetToken:
    return jsonify({"status": "failed", "result": "User info not found"}), 200, {'Content-Type': 'application/json',
                                                                                 'Access-Control-Allow-Origin': '*'}
  tokeninfo = db.getForgotPasswordUser(resetToken)
  print(tokeninfo)
  if not tokeninfo:
    return jsonify({"status": "failed", "result": "User not found"}), 200, {'Content-Type': 'application/json',
                                                                            'Access-Control-Allow-Origin': '*'}
  user = tokeninfo['mtee_user_id']
  print(user)
  if not user:
    return jsonify({"status": "failed", "result": "User not found"}), 200, {'Content-Type': 'application/json',
                                                                            'Access-Control-Allow-Origin': '*'}
  if user:
    updateResponse = db.updatePassword(password, user)
    print('update Response: ' + updateResponse)
    return jsonify({"status": "success", "result": updateResponse}), 200, {'Content-Type': 'application/json',
                                                                           'Access-Control-Allow-Origin': '*'}


#######################################################

@app.route('/validateAccount', methods=['POST', 'OPTIONS'])
# This is used in case user forgets password.
# The user provides email which is validated to see if the email is registered in the system or not.
# If email is registered, a password reset link is sent to user's registered email.
def validateAccount():
  # print(request.data)
  # print('Printed request data above .......')
  requestData = json.loads(request.data)
  mtee_user_id = requestData['mtee_user_id']
  mtee_user_lang = requestData['mtee_user_lang']
  if mtee_user_id:
    Response = db.validateAccount(mtee_user_id)
    validate_user_details = Response.json
    result = validate_user_details['result']
    status = validate_user_details['status']
    if status == 'failed':
      return jsonify({'status': 'failed', 'result': result}), 200, {'Content-Type': 'application/json',
                                                                    'Access-Control-Allow-Origin': '*'}
    if result[0]['mtee_user_status'] == 'verified' or result[0]['mtee_user_status'] == 'initiated':
      userDetails = validate_user_details['result']
      # print userDetails
      recieverEmail = userDetails[0]['mtee_user_email']
      recieverRole = userDetails[0]['mtee_user_role']
      recieverStatus = userDetails[0]['mtee_user_status']
      recieverName = userDetails[0]['mtee_user_id']
      if recieverRole == 'T' or recieverRole == 'A':
        if recieverStatus == 'initiated' or recieverStatus == 'verified':
          uuidStatus = uuid.uuid1()
          url = str(uuidStatus).replace("-", "")
          db.forgotPassword(recieverName, url, mtee_user_lang)
          urlToSend = baseurl + "/resetPassword?reset=" + url
          # print(urlToSend)
          msgContent = db.getUserMsg('forgotPassword', mtee_user_lang)
          body = msgContent['body']
          body = body.replace('recieverName', recieverName)
          body = body.replace('urlToSend', urlToSend)
          # print(body + " ---- ")
          msg = Message("Password Reset", sender="mittaristo@lut.fi", recipients=[recieverEmail])
          msg.body = body + "\n"
          print(msg)
          if setting['MAIL']:
            mail.send(msg)
          return jsonify({'status': 'success', 'result': 'Please Check Your Email'}), 200, {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'}
    else:
      error = db.getMessage("100")
      return jsonify({'status': 'failed', 'result': error}), 200, {'Content-Type': 'application/json',
                                                                   'Access-Control-Allow-Origin': '*'}
  else:
    # print("Failed to validate user as data is incomplete!")
    error = db.getMessage("106")
    return jsonify({'status': 'failed', 'result': error}), 200, {'Content-Type': 'application/json',
                                                                 'Access-Control-Allow-Origin': '*'}


#######################################################


@app.route('/getQuestions', methods=['GET'])
def getQuestions():
  global allQuestions
  reloadCheck = request.args.get('reload', False)
  if allQuestions == {} or reloadCheck:
    # print("Getting all Questions ............ ")
    allQuestions = db.getQuestions()
  else:
    print("Questions already available - {}".format(allQuestions))
  return jsonify({'status': 'success', 'result': allQuestions}), 200, {'Content-Type': 'application/json',
                                                                       'Access-Control-Allow-Origin': '*'}


#######################################################

@app.route('/getCountryList', methods=['GET'])
def getCountryList():
  global allCountryList
  reloadCheck = request.args.get('reload', False)
  if allCountryList == {} or reloadCheck:
    # print("Getting all Country List ............ ")
    allCountryList = db.getCountryList()
  else:
    print("Country list already available - {}".format(allCountryList))
  return jsonify({'status': 'success', 'result': allCountryList}), 200, {'Content-Type': 'application/json',
                                                                         'Access-Control-Allow-Origin': '*'}


########################################################

@app.route('/getMunicipalityList', methods=['GET'])
def getMunicipalityList():
  getMunicipalityList = jsonify({'status': 'success', 'result': db.getMunicipalityList()}), 200, {
    'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
  return getMunicipalityList


########################################################

@app.route('/getProvienceList', methods=['GET'])
def getProvienceList():
  # print('Inside getProvienceList')
  provienceList = jsonify({'status': 'success', 'result': db.getProvienceList()}), 200, {
    'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
  return provienceList


#######################################################

@app.route('/getQuestionThemeName', methods=['GET'])
def getQuestionThemeName():
  global allThemeNames
  reloadCheck = request.args.get('reload', False)
  if allThemeNames == {} or reloadCheck:
    # print("Getting all Theme Name ............ ")
    allThemeNames = db.getQuestionThemeName()
  else:
    print("Theme names already available - {}".format(allThemeNames))
  return jsonify({'status': 'success', 'result': allThemeNames}), 200, {'Content-Type': 'application/json',
                                                                        'Access-Control-Allow-Origin': '*'}


#######################################################

@app.route('/saveUserResponse', methods=['OPTIONS', 'POST'])
def saveUserResponse():
  # print('Inside save user response {}'.format(request.data) )
  requestData = json.loads(request.data)
  mtee_user_start_time = requestData['start_time']
  # print(mtee_user_start_time)
  mtee_user_response = requestData['mtee_user_response']
  mtee_user_end_time = requestData['end_time']
  mtee_user_language = requestData['mtee_user_language']
  mtee_user_yob = requestData['mtee_user_yob']
  mtee_user_gender = requestData['mtee_user_gender']
  mtee_user_id = requestData['mtee_user_id']
  responseSaved = db.saveUserResponse(mtee_user_response, mtee_user_start_time, mtee_user_end_time, mtee_user_language,
                                      mtee_user_yob, mtee_user_gender, mtee_user_id)
  return responseSaved


#######################################################

@app.route('/getFeedbackParameters', methods=['GET'])
def getFeedbackParameters():
  # mtee_feedback_code = request.json['mtee_feedback_code']
  # mtee_feedback_question_list = request.json['mtee_feedback_question_list']
  return db.getFeedbackParameters(), 200, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}


#######################################################

@app.route('/getAllResponseOfUser', methods=['GET'])
def getAllResponseOfUser():
  mtee_question_responder_user_id = request.args.get('user')
  # print(mtee_question_responder_user_id)
  # if mtee_question_responder_user_id != session.get('mtee_user_id'):
  # return jsonify({"status":"failed", "result":"User login Expired"}), 200, {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}
  mtee_question_response_date = request.args.get('selectedDate')
  return db.getAllResponseOfUser(mtee_question_responder_user_id, mtee_question_response_date), 200, {
    'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}


#######################################################

@app.route('/modify', methods=['GET'])
def modify():
  return db.modify()


#######################################################

@app.route('/getAllDatesForUser', methods=['GET'])
def getAllDatesForUser():
  mtee_question_responder_user_id = request.args.get('user')
  # print('Inside getAllDatesForUser')
  # print(mtee_question_responder_user_id)
  # print('Session UserId')
  # print(session.get('mtee_user_id'))
  # if mtee_question_responder_user_id != session.get('mtee_user_id'):
  # return jsonify({"status":"failed", "result":"User login Expired"}), 200, {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}
  return db.getAllDatesForUser(mtee_question_responder_user_id), 200, {'Content-Type': 'application/json',
                                                                       'Access-Control-Allow-Origin': '*'}


#######################################################
#######################################################

@app.route('/verifyReportKey', methods=['GET', 'OPTIONS'])
def verifyReportKey():
  key = request.args.get('reportKey')
  if key == 'Mittaristo@2021':
    return jsonify({"status": "success", "result": key}), 200, {"Content-Type": "application/json",
                                                                "Access-Control-Allow-Origin": "*"}
  else:
    return jsonify({"status": "Invalid Key", "result": ""}), 200, {"Content-Type": "application/json",
                                                                   "Access-Control-Allow-Origin": "*"}


#######################################################
@app.route('/downloadReportBetweenDates', methods=['GET', 'OPTIONS'])
def downloadReportBetweenDates():
  global setting
  try:
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    # schoolCode = request.args.get('schoolCode')
    # municipalityCode = request.args.get('municipalityCode')
    # provienceCode = request.args.get('provienceCode')
    key = request.args.get('report_key')
    # print('Inside downloadDump {}'.format(request.data))
    # requestData = json.loads(request.data)
    # key = requestData['report_key']
    fileNameString = str(uuid.uuid4())
    if key == 'Mittaristo@2021':
      response = db.downloadReportBetweenDates(
        key,
        fileNameString,
        startDate,
        endDate,
        # schoolCode,
        # municipalityCode,
        # provienceCode,
        syspath,
        setting['APP_OS_REPORT_DIR'])
      # print(response)
      if response == 'Failed':
        return jsonify({"status": "failed"}), 200, {"Content-Type": "application/json",
                                                    "Access-Control-Allow-Origin": "*"}
      return send_from_directory('{}'.format(setting['APP_OS_REPORT_DIR']), filename=response + '.csv',
                                 as_attachment=True)
      # return jsonify({'status': 'success', 'result': response}), 200, {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
    else:
      return jsonify({"status": "Invalid Key"}), 200, {"Content-Type": "application/json",
                                                       "Access-Control-Allow-Origin": "*"}
  except:
    print(traceback.format_exc())
    return jsonify({"status": "failed"}), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


#############################################################

@app.route('/searchByMunicipalityCode', methods=['POST', 'OPTIONS'])
def searchByMunicipalityCode():
  requestData = json.loads(request.data)
  mtee_municipality_code = requestData['mtee_municipality_code']
  municipalityDetails = jsonify(
    {'status': 'success', 'result': db.findMunicipalityDetails(mtee_municipality_code)}), 200, {
                          'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
  print(str(municipalityDetails))
  return municipalityDetails


#############################################################
@app.route('/updateLocationDetails', methods=['POST', 'OPTIONS'])
def updateLocationDetails():
  requestData = json.loads(request.data)
  municipalityChange = requestData.get('change_municipality', None)
  provienceChange = requestData.get('change_province', None)
  if not municipalityChange and not provienceChange:
    return jsonify({'status': 'success', 'result': 'UPDATE ERROR OR SUCCESS CODE HERE'}), 200, {
      'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
  if municipalityChange:
    municipalityDetails = db.changeMunicipality(requestData)
  if provienceChange:
    municipalityDetails = db.changeProvience(requestData)
  print(str(municipalityDetails))
  return jsonify({'status': 'success', 'result': municipalityDetails}), 200, {
    'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}


#############################################################
@app.route('/deleteLocationDetails', methods=['POST', 'OPTIONS'])
def deleteLocationDetails():
  requestData = json.loads(request.data)
  municipalityToDelete = db.deleteLocationDetails(requestData)
  return jsonify({'status': 'success', 'result': municipalityToDelete}), 200, {
    'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}


###############################################################

@app.route('/searchByMunicipalityName', methods=['POST', 'OPTIONS'])
def searchByMunicipalityName():
  requestData = json.loads(request.data)
  mtee_municipality_name = requestData['mtee_municipality_name']
  municipalityDetails = jsonify(
    {'status': 'success', 'result': db.searchByMunicipalityName(mtee_municipality_name)}), 200, {
                          'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
  print(str(municipalityDetails))
  return municipalityDetails


##############################################################

@app.route('/createCampaign', methods=['POST', 'OPTIONS'])
def createcampaign():
    requestData = json.loads(request.data)
    mtee_user_id = requestData['mtee_user_id']
    mtee_campaign_created_user_id = mtee_user_id
    mtee_campaign_created_date = datetime.now()
    mtee_campaign_code = requestData['mtee_campaign_code']
    mtee_campaign_type = requestData['mtee_campaign_type']
    mtee_campaign_description = requestData['mtee_campaign_description']
    mtee_campaign_start_date = requestData['mtee_campaign_start_date']
    mtee_campaign_end_date = requestData['mtee_campaign_end_date']
    mtee_campaign_status = 'Created'
    mtee_campaign_update_user_id = mtee_user_id
    mtee_campaign_update_date = datetime.now()
    return db.createCampaign(mtee_campaign_created_user_id,
                             mtee_campaign_created_date,
                             mtee_campaign_code,
                             mtee_campaign_type,
                             mtee_campaign_description,
                             mtee_campaign_start_date,
                             mtee_campaign_end_date,
                             mtee_campaign_status,
                             mtee_campaign_update_user_id,
                             mtee_campaign_update_date
                             ), 200, {'Content-Type':'application/json', 'Access-Control-Allow-Origin': '*'}

##############################################################




##############################################################
##############################################################




##############################################################
##############################################################




##############################################################
##############################################################




##############################################################
##############################################################




##############################################################

if __name__ == '__main__':
  app.run(host=os.getenv('IP', setting['APP_BE_LOCAL_IP']), port=int(os.getenv('PORT', setting['APP_BE_PUBLIC_PORT'])))
##########################################################################################################################################################
