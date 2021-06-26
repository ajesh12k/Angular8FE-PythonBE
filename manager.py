import pandas as pd
import pymongo, traceback
from pymongo import MongoClient
from flask import Flask, jsonify, request, json
from datetime import datetime
from datetime import timedelta
import uuid
import urllib
import dateutil.parser as parser
import os, time
import hashlib
import base64
from email.utils import parseaddr
import settings

####################################################################################################
connection_params = settings.configurationReader()
dbconnstr = "mongodb+srv://" + connection_params['APP_DB_USER'] + ":" + connection_params['APP_DB_PWD'] + \
            connection_params['APP_DB_HOST'] + "&ssl=true&ssl_cert_reqs=CERT_NONE"
connection = pymongo.MongoClient(dbconnstr, int(connection_params['APP_DB_PORT']))
# print(connection)
mongo = connection[connection_params['APP_DB_NAME']]

MONGO_PORT = 25058
MONGO_DB = 'finmtee'
os.environ['TZ'] = 'Europe/Helsinki'

######################################################################################################

class DatabaseManager:

  ##############################################################

  def getAllLanguage(self):
    data = mongo.finmtee_app_setting
    query = {'setting_type': 'language'}
    languageInfo = data.find_one(query)
    response = []
    if languageInfo:
      for element in languageInfo['language_list']:
        if element['mtee_language_status'] == 'Active':
          response.append(element['mtee_language_display_name'])
    # print(str(response))
    return response

  #############################################################

  def addLanguage(self, data):
    try:
      collection = mongo.finmtee_app_setting
      query = {'setting_type': 'language'}
      languageInfo = collection.find_one(query)
      response = []
      if languageInfo:
        response = languageInfo['language_list']
      response.append(data)
      newvalues = {"$set": {"language_list": response}}
      # updated = collection.update(query, newvalues)
      self.updateAddLanguage(data['mtee_language_display_name'])
      return 'success'
    except Exception as e:
      print(traceback.format_exc())
      return str(e)

  #############################################################

  def updateAddLanguage(self, data):
    try:
      collection = mongo.finmtee_app_setting
      query = {'setting_type': 'add_language'}
      collectionList = collection.find_one(query)
      for element in collectionList['collection_list']:
        print(element)
        eachColl = mongo[element]
        # eachColl = mongo.element
        eachData = eachColl.find({}, {"_id": False})
        count = 0
        for ele in eachData:
          change = False
          query = {}
          changes = {}
          for key, val in ele.items():
            if type(val) == dict:
              if 'English' in val.keys():
                val[data] = ""
                count += 1
                change = True
                changes[key] = val
            else:
              query[key] = val
          if change:
            print('#################################')
            print(query, changes, count)
            eachColl.update(query, {"$set": changes})
    except Exception as e:
      print(traceback.format_exc())
      return str(e)

  #############################################################

  def getErrorList(self):
    collection = mongo.finmtee_message_list
    output = []
    query = {}
    query["mtee_status"] = "failed"
    # print ("Query for error serach is - " + str(query))
    for q in collection.find(query, {"_id": False}).sort([("mtee_code", pymongo.ASCENDING)]):
      # print(q)
      output.append(q)
    # print(output)
    return output

  #############################################################

  def getSuccessMessageList(self):
    collection = mongo.finmtee_message_list
    output = []
    query = {}
    query["mtee_status"] = "success"
    # print ("Query for success message serach is - " + str(query))
    for q in collection.find(query, {"_id": False}).sort([("mtee_code", pymongo.ASCENDING)]):
      # print(q)
      output.append(q)
    # print(output)
    return output

  #############################################################

  def getAllStaticContent(self):
    data = mongo.finmtee_app_setting
    query = {'setting_type': 'static_content'}
    staticInfo = data.find_one(query)
    response = []
    if staticInfo:
      for element in staticInfo['page_list']:
        response.append(element)
    # print(str(response))
    return response
  #################################################################

  def saveUserAccessDetails(self, mtee_user_access_details, unique_id, mtee_user_access_ip, mtee_user_access_time):
    data = mongo.finmtee_app_access
    unique_id = unique_id
    mtee_user_access_details = mtee_user_access_details
    mtee_user_access_ip = mtee_user_access_ip
    mtee_user_access_time = mtee_user_access_time
    if data.insert({
      'mtee_user_access_unique_id': unique_id,
      'mtee_user_device_details': mtee_user_access_details,
      'mtee_user_access_ip': mtee_user_access_ip,
      'mtee_user_access_time': mtee_user_access_time
    }):
      return 'Inserted'
    else:
      return 'Error in Inserting User Access Details'

  #################################################################

  def getUserAccessDetails(self):
    data = mongo.finmtee_app_access
    output = []
    query = {}
    i = 0
    res = data.find(query, {"_id": False}).sort([("mtee_user_access_time", pymongo.ASCENDING)])
    for eachRow in res:
      i = i + 1
      #print(i)
    return i

  #################################################################

  def registerUser(self,
                   mtee_user_yob,
                   mtee_user_gender,
                   mtee_user_id,
                   mtee_user_pwd,
                   mtee_user_email,
                   mtee_user_lang,
                   mtee_user_role):
    data = mongo.finmtee_users
    # print('inside register user in manager for database :')
    # print(mtee_user_pwd)
    decodedPassword = base64.b64decode(mtee_user_pwd)
    pwd = str(decodedPassword) + mtee_user_id
    encpassword = hashlib.md5(pwd.encode('utf-8')).hexdigest()
    currTime = datetime.now()
    # print("Checking if user id exist -")
    if data.find_one({"mtee_user_id": mtee_user_id}):
      # print("Username already exists")
      errorMap = self.getMessage("101")
      return jsonify({"status": "failed", "result": errorMap})
    elif data.find_one({"mtee_user_email": mtee_user_email}):
      # print("Email Id already exists")
      errorMap = self.getMessage("102")
      return jsonify({"status": "failed", "result": errorMap})
    else:
      if parseaddr(mtee_user_email):
        # print("Creating User in MTEE Database :")
        if data.insert({
          'mtee_user_yob': mtee_user_yob,
          'mtee_user_gender': mtee_user_gender,
          'mtee_user_id': mtee_user_id,
          'mtee_user_pwd': encpassword,
          'mtee_user_email': mtee_user_email,
          'mtee_user_role': mtee_user_role,
          'mtee_user_status': 'initiated',
          'mtee_user_date_created': currTime,
          'mtee_user_date_modified': currTime,
          'mtee_user_lang': mtee_user_lang,
          'mtee_user_type': 'default',
          'mtee_user_group': 'default'
        }):
          # print("User Sucessfully Created")
          responseMap = self.getMessage("900")
          # print(responseMap)
          return jsonify({'status': 'success', 'result': responseMap})
      else:
        # print("Email format incorrect!")
        errorMap = self.getMessage("103")
        return jsonify({'status': 'failed', 'result': errorMap})
    # print("Unable to save user. Please try again!")
    errorMap = self.getMessage("500")
    return jsonify({'status': 'failed', 'result': errorMap})

  ###################################################################

  def getMessage(self, code):
    collection = mongo.finmtee_message_list
    queryMap = {"mtee_code": code}
    # print("Getting Error Code for error " + code)
    result = collection.find_one(queryMap, {"_id": False, "mtee_code": False, "mtee_status": False, "mtee_type": False})
    if result:
      return result
    else:
      return "Error performing request"

  #############################################################

  def getUserMsg(self, reason, lang):
    collection = mongo.finmtee_notification
    query = {}
    query['mtee_notification_reason'] = reason
    query['mtee_notification_type'] = 'email'
    data = collection.find_one(query)
    # print(data['mtee_notification_text'])
    body = data['mtee_notification_text'][lang]
    # print(body)
    return {"status": "success", "body": body}

  ##################################################################

  def validateUser(self,
                   mtee_user_id,
                   mtee_user_pwd,
                   mtee_user_ip,
                   mtee_user_browser):
    data = mongo.finmtee_users
    decodedPassword = base64.b64decode(mtee_user_pwd)
    # print (decodedPassword)
    decodedPasswordStr = str(decodedPassword)
    userinf = data.find_one({'mtee_user_email': mtee_user_id})
    if userinf:
      mtee_user_id = userinf['mtee_user_id']
    pwd = decodedPasswordStr + mtee_user_id
    encpassword = hashlib.md5(pwd.encode('utf-8')).hexdigest()
    output = []
    query = {'$or': [{'mtee_user_id': mtee_user_id}, {'mtee_user_email': mtee_user_id}],
             'mtee_user_pwd': encpassword}
    # print "Query for serach is - " + str(query)
    for q in data.find(query):
      currTime = datetime.now()
      userAgent = str(mtee_user_browser)
      sessionId = str(uuid.uuid4())
      login = {'mtee_user_id': mtee_user_id, 'login_time': currTime, 'user_ip_address': mtee_user_ip,
               'loginInfo': userAgent, 'sessionId': sessionId}
      loginInfo = mongo.eumtee_login_data
      loginInfo.insert(login)
      output.append({"mtee_user_gender": q['mtee_user_gender'], "mtee_user_yob": q['mtee_user_yob'],
                     "mtee_user_role": q['mtee_user_role'], "mtee_user_status": q['mtee_user_status'],
                     "mtee_user_id": q['mtee_user_id'], "mtee_user_lang": q['mtee_user_lang']})
      return jsonify({'status': 'success', 'result': output, 'sessionId': sessionId})
    errorMap = self.getMessage("100")
    return jsonify({'status': 'failed', 'result': errorMap})

  ###################################################################

  def validateAccount(self, mtee_user_id):
    data = mongo.finmtee_users
    userinf = data.find_one({'mtee_user_email': mtee_user_id})
    if userinf:
      mtee_user_id = userinf['mtee_user_id']
    output = []
    query = {'$or': [{'mtee_user_id': mtee_user_id}, {'mtee_user_email': mtee_user_id}]}
    # print "Query for serach is - " + str(query)
    for q in data.find(query):
      output.append({"mtee_user_role": q['mtee_user_role'], "mtee_user_status": q['mtee_user_status'],
                     "mtee_user_id": q['mtee_user_id'], "mtee_user_email": q['mtee_user_email']})
      return jsonify({'status': 'success', 'result': output})
    # print "This account is not registered "
    errorMap = self.getMessage("104")
    return jsonify({'status': 'failed', 'result': errorMap})

  ###################################################################

  #######################################################################

  def forgotPassword(self, user, url, lang):
    collection = mongo.finmtee_forgot_password
    query = {}
    query['mtee_user_id'] = user
    query['mtee_url'] = url
    query['mtee_user_lang'] = lang
    collection.insert(query)
    return "success"

  ######################################################################

  def getForgotPasswordUser(self, url):
    collection = mongo.finmtee_forgot_password
    query = {}
    query['mtee_url'] = url
    userInfo = collection.find_one(query, {"_id": False})
    return userInfo

  #####################################################################

  def updatePassword(self, newPwd, user):
    collection = mongo.finmtee_users
    print(newPwd)
    decodedPassword = base64.b64decode(newPwd)
    decodedPasswordStr = str(decodedPassword)
    pwd = decodedPasswordStr + user
    encpassword = hashlib.md5(pwd.encode('utf-8')).hexdigest()
    # print(user + ' :::::::::::::: ' + encpassword)
    query = {"mtee_user_id": user}
    newvalues = {"$set": {"mtee_user_pwd": encpassword}}
    updated = collection.update(query, newvalues)
    return str(updated)

  #####################################################################
  def activateUser(self, user):
    collection = mongo.finmtee_users
    query = {}
    query['mtee_user_id'] = user
    update = {}
    update['mtee_user_status'] = 'verified'
    user = collection.find_one(query, {"_id": False})
    if user:
      activate = collection.update(query, {'$set': update})
      return {"status": "success", "result": user}
    else:
      return {"status": "failed", "result": "Failed to find user"}

  ######################################################################

  def getQuestions(self):
    data = mongo.finmtee_questions
    output = []
    query = {}
    query["mtee_question_status"] = "Active"
    # print ("Query for question serach is - " + str(query))
    for q in data.find(query, {"_id": False}).sort([("mtee_question_level", pymongo.ASCENDING)]):
      # print(q['mtee_question_type_name'])
      options = self.getOptions(q['mtee_question_type_name'])
      # print(options)
      q['questionType'] = options['questionType']
      q['options'] = options['options']
      q['scaleValue'] = 0
      output.append(q)
    return output

  ###################################################################

  def getCountryList(self):
    data = mongo.finmtee_app_setting
    query = {"type": "municipality"}
    countyInfo = data.find_one(query)
    response = []
    if countyInfo:
      for element in countyInfo['country_details']:
        response.append(element)
    # print(response)
    return response

  ###################################################################

  def getMunicipalityList(self):
    data = mongo.finmtee_app_setting
    query = {'type': 'municipality'}
    municipalityList = data.find_one(query)
    response = []
    if municipalityList:
      for element in municipalityList['country_details']:
        response.append(element)
    print(response)
    return response

  ###################################################################

  def getProvienceList(self):
    data = mongo.finmtee_app_setting
    query = {'type': 'municipality'}
    provienceList = data.find_one(query, {"_id": False})
    response = {}
    if provienceList:
      for element in provienceList['country_details']:
        code = str(element['mtee_county_provience_code'])
        name = element['mtee_county_provience_name_1']
        response[code] = name
    return response

  ###################################################################

  def getQuestionThemeName(self):
    collection = mongo.finmtee_question_theme
    query = {}
    query["mtee_theme_status"] = "Active"
    res = collection.find(query, {'_id': False}).sort([("mtee_sequence_priority", pymongo.ASCENDING)])
    out = []
    for eachColl in res:
      out.append(eachColl)
    return out

  ###################################################################

  def getOptions(self, questionType):
    data = mongo.finmtee_question_sequence
    response = {}
    for sequence in data.find({"mtee_question_type_name": questionType}, {"_id": False}):
      response['questionType'] = sequence['mtee_question_type']
      response['options'] = sequence['mtee_question_options']
    return response

  ###################################################################

  def saveUserResponse(self,
                       mtee_user_response,
                       mtee_user_start_time,
                       mtee_user_end_time,
                       mtee_user_language,
                       mtee_user_yob,
                       mtee_user_gender,
                       mtee_user_id):
    data = mongo.finmtee_responses
    # print('Inside save user response in db')
    saveResponse = mtee_user_response,
    startTime = mtee_user_start_time
    endTime = mtee_user_end_time
    user_language = mtee_user_language
    mtee_user_yob = mtee_user_yob
    mtee_user_gender = mtee_user_gender
    mtee_user_id = mtee_user_id
    # print(mtee_user_end_time)
    if data.insert({
      'mtee_user_response': saveResponse,
      'mtee_user_start_time': startTime,
      'mtee_user_end_time': endTime,
      'mtee_user_language': user_language,
      'mtee_user_yob': mtee_user_yob,
      'mtee_user_gender': mtee_user_gender,
      'mtee_user_id': mtee_user_id
    }):
      # print("Response Sucessfully Saved")
      return jsonify({'status': 'success', 'result': 'success'}), 200, {"Content-Type": "application/json",
                                                                        "Access-Control-Allow-Origin": "*"}
    else:
      # print("Response not saved!")
      return jsonify({'status': 'failed', 'result': 'error'}), 200, {"Content-Type": "application/json",
                                                                     "Access-Control-Allow-Origin": "*"}

  ###################################################################

  def getFeedbackParameters(self):
    data = mongo.finmtee_feedback_parameter
    output = []
    query = {}
    query["mtee_feedback_staus"] = "Active"
    for q in data.find(query, {'_id': False}).sort([("mtee_feedback_sequence", pymongo.ASCENDING)]):
      output.append(
        {"mtee_feedback_parameters": q['mtee_feedback_parameters'], "mtee_feedback_code": q['mtee_feedback_code'],
         "mtee_feedback_question_list": q['mtee_feedback_question_list'],
         "mtee_feedback_description_1": q['mtee_feedback_description_1'],
         "mtee_feedback_sequence": q['mtee_feedback_sequence'], "mtee_feedback_type": q['mtee_feedback_type'],
         "mtee_feedback_manual_average": q['mtee_feedback_manual_average'],
         "mtee_feedback_manual_average_use": q['mtee_feedback_manual_average_use']})
    return json.dumps({'status': 'success', 'result': output})

  ###################################################################

  def getAllResponseOfUser(self, mtee_question_responder_user_id, mtee_question_response_date):
    data = mongo.finmtee_responses
    output = []
    query = {}
    responseList = []
    ansThemeTotal = 0
    feedbackGroupRespAvg = 0
    i = 0
    mainMap = {}
    if mtee_question_responder_user_id != "":
      query["mtee_user_id"] = mtee_question_responder_user_id
    if mtee_question_response_date != "":
      query["mtee_user_end_time"] = mtee_question_response_date
    q = data.find_one(query)
    date = q['mtee_user_end_time']
    # print( 'Response Fetched for date : '+ date)
    responseList = q['mtee_user_response'][0]
    # print('Response Array for selected date : ')
    # print(responseList)
    getfeedBackParameters = json.loads(self.getFeedbackParameters())
    # print('Fetching Feedback Parameter')
    feedBackParameters = getfeedBackParameters['result']
    # print(feedBackParameters)
    for parameter in feedBackParameters:
      params = parameter['mtee_feedback_question_list']
      paramsCode = parameter['mtee_feedback_code']
      paramArr = params.split(";")
      # print(paramArr)
      for question in paramArr:
        # print ('Looking Response For : ' + question)
        # print ('Answer for Question : ' + str(responseList[question]))
        ansThemeTotal = ansThemeTotal + int(responseList[question])
        # print (ansThemeTotal)
        # print ('New ansThemeTotal printed above')
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        i = i + 1
      # print(ansThemeTotal)
      ansAvgVal = float(0)
      # print(i)
      if (paramsCode == 'theme1'):
        ansAvgVal = round(float(ansThemeTotal), 2)
      if (paramsCode == 'theme2'):
        ansAvgVal = round((float(ansThemeTotal) / float(i)), 2)
      if (paramsCode == 'theme3'):
        ansAvgVal = round((float(ansThemeTotal) / float(30)), 2)
      if (paramsCode == 'theme4'):
        ansAvgVal = round((float(ansThemeTotal) / float(i)), 2)
      if (paramsCode == 'theme5'):
        ansAvgVal = round((float(ansThemeTotal) / float(i)), 2)
      if (paramsCode == 'theme6'):
        ansAvgVal = round((float(ansThemeTotal) / float(i)), 2)
      # print ('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
      # print (ansAvgVal)
      # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
      parametersInfo = parameter['mtee_feedback_parameters']
      # print(parametersInfo)
      manualAvg = parameter['mtee_feedback_manual_average']
      for info in parametersInfo:
        if ansAvgVal <= float(info['mtee_feedback_max']) and ansAvgVal >= float(info['mtee_feedback_min']):
          ####################################################################################
          replacedText1FIN = info['mtee_feedback_text']['Finnish'].replace("****", str(ansAvgVal))
          replacedText1ENG = info['mtee_feedback_text']['English'].replace("****", str(ansAvgVal))
          replacedText1SWE = info['mtee_feedback_text']['Swedish'].replace("****", str(ansAvgVal))
          ####################################################################################
          replacedText2FIN = replacedText1FIN.replace("++++", str(manualAvg))
          replacedText2ENG = replacedText1ENG.replace("++++", str(manualAvg))
          replacedText2SWE = replacedText1SWE.replace("++++", str(manualAvg))
          ####################################################################################
          feedbackurl = info['mtee_feedback_url']
          tempMap = {}
          code = paramsCode
          # print('Feedback calculated for :' )
          # print(code)
          tempMap['mtee_feedback_description_ENG'] = replacedText2ENG  # changed
          tempMap['mtee_feedback_description_SWE'] = replacedText2SWE
          tempMap['mtee_feedback_description_FIN'] = replacedText2FIN
          tempMap['mtee_feedback_url'] = feedbackurl
          mainMap[code] = tempMap
          # print('++++++++++++++++++++++++++++++++++++++++++++++')
          # print (mainMap)
          # print('++++++++++++++++++++++++++++++++++++++++++++++')
      # print ansAvg
      # print mainMap
      ansThemeTotal = 0
      i = 0
    mainMap['feedBackDate'] = date
    output.append(mainMap)
    return jsonify({"result": output, "status": "success"})

  ###################################################################

  def getAllDatesForUser(self, mtee_question_responder_user_id):
    data = mongo.finmtee_responses
    query = {}
    if mtee_question_responder_user_id != "":
      query["mtee_user_id"] = mtee_question_responder_user_id
    dateArr = []
    date = datetime.now()
    for q in data.find(query).sort([("mtee_user_end_time", pymongo.DESCENDING)]):
      date = q['mtee_user_end_time']
      dateArr.append(date)
    return jsonify({"result": dateArr, "status": "success"})

  ###################################################################

  def getHeaderSeqKey(self, obj):
    return obj['mtee_report_header_seq']

  ###################################################################

  def getReportHeaders(self, reportName):
    # print('Inside getReportHeaders : ---- ')
    data = mongo.finmtee_report_heading_sequence
    query = {'mtee_report_name': reportName}
    headerDetails = data.find_one(query, {"_id": False})
    headerList = []
    if headerDetails:
      headerList = headerDetails['mtee_report_header_list']
    return headerList

  ###################################################################

  def formatBasicReportDump(self, basicReportDump, headerFormattedResponseData):
    reportName = 'Basic report for Mittaristo'
    reportHeaderList = []
    reportHeaderList = self.getReportHeaders(reportName)
    # print('Printing header list')
    # print(reportHeaderList)
    try:
      reportHeaderList.sort(key=self.getHeaderSeqKey, reverse=False)
      # print('Printing header list after sorting')
      # print(reportHeaderList)
    except:
      print(traceback.format_exc())
    i = 0
    for headers in reportHeaderList:
      # print('Header searching')
      # print(headers['mtee_question_id'])
      for element, val in basicReportDump.items():
        if (str(element) == str(headers['mtee_question_id'])):
          headerFormattedResponseData[headers['mtee_report_header_name']] = val
          # print(headers['mtee_report_header_name'])
          i = i + 1
          # print(i)
    # print(' Returning headerFormattedResponseData')
    return headerFormattedResponseData

  ###################################################################

  def downloadReportBetweenDates(self,
                                 key,
                                 fileNameString,
                                 startDate,
                                 endDate,
                                 # schoolCode,
                                 # municipalityCode,
                                 # provienceCode,
                                 syspath,
                                 dirpath):
    startDate = startDate
    print(startDate)
    endDate = endDate
    print(endDate)
    # schoolCode = schoolCode
    # print(schoolCode)
    # municipalityCode = str(municipalityCode.encode('utf-8'))[2:-1]
    # print(municipalityCode)
    # provienceCode = provienceCode
    # print(provienceCode)
    try:
      data = mongo.finmtee_responses
      query = {
        "mtee_user_start_time": {"$gt": startDate},
        "mtee_user_end_time": {"$lt": endDate}
      }
      # if provienceCode:
      # listOfMunicipality = self.getMunicipalityListFromProvince(provienceCode)
      # print(listOfMunicipality)
      # query["mtee_user_response.SPA"] = {"$or": listOfMunicipality}
      # if municipalityCode:
      # print('Searching for single municipality')
      # query["mtee_user_response.SPA"] = municipalityCode
      print('Search Query below:')
      print(query)
      # provienceList = self.getMunicipalityList()
      mtee_user_language = []
      mtee_user_end_time = []
      mtee_user_start_time = []
      mtee_user_time_taken = []
      mtee_user_id = []
      mtee_user_yob = []
      mtee_user_gender = []
      mtee_fetched_user_response = []

      for q in data.find(query, {'_id': False}).sort([('mtee_user_end_time', pymongo.ASCENDING)]):
        # print(q)
        if (q['mtee_user_language']):
          lang = q['mtee_user_language']
          # print(lang)
          if (lang == 'FIN'):
            mtee_user_language.append("1")
          if (lang == 'Finnish'):
            mtee_user_language.append("1")
          if (lang == 'SWE'):
            mtee_user_language.append("2")
          if (lang == 'Swedish'):
            mtee_user_language.append("2")
          if (lang == 'ENG'):
            mtee_user_language.append("3")
          if (lang == 'English'):
            mtee_user_language.append("3")
        else:
          mtee_user_language.append("1")

        # printing Starting_time
        startTime = datetime.strptime(q['mtee_user_start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # print("Starting_time", startTime)
        # printing Ending_time
        endTime = datetime.strptime(q['mtee_user_end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # print("End_time", endTime)
        diff = endTime - startTime
        timetaken = diff.days * 24 * 60 * 60 + diff.seconds
        mtee_user_time_taken.append(timetaken)
        mtee_user_end_time.append(q['mtee_user_end_time'])
        mtee_user_start_time.append(q['mtee_user_start_time'])
        mtee_user_id.append(q['mtee_user_id'])
        mtee_user_yob.append(q['mtee_user_yob'])
        mtee_user_gender.append(q['mtee_user_gender'])
        mtee_fetched_user_response.append(q['mtee_user_response'])

      responseData = {}
      headerFormattedResponseData = {}
      responseData['Language'] = mtee_user_language
      responseData['StartTime'] = mtee_user_start_time
      responseData['EndTime'] = mtee_user_end_time
      responseData['UsedTime'] = mtee_user_time_taken
      responseData['Userid'] = mtee_user_id
      responseData['Year'] = mtee_user_yob
      responseData['Gender'] = mtee_user_gender
      ############
      for items in mtee_fetched_user_response:
        # This loop traverses all the fetched responses within the search query parameters.
        # All processing below is for each fetched document from user response collection.
        for elem in items:
          # This loop will traverse through each answered question for each fetched document.
          for questionID, val in elem.items():
            answerNew = val
            municipalityName = ''
            provienceName = ''
            provienceCode = ''
            teacherLevelAnswers = []
            if questionID in responseData:
              # If Column is present for questions. This is executed after first response is processed, as column headers are present.
              if questionID == 'MS':
                 isTeacherClass = ''
                 isTeacherLanguages = ''
                 isTeacherMath = ''
                 isTeacherCounselling = ''
                 isTeacherReal = ''
                 isTeacherArt = ''
                 isTeacherSpecial = ''
                 isTeacherOptional = ''
                 isTeacherVocational = ''
                 isTeacherGeneral = ''
                 isNoTeacher = ''
                 teacherLevelAnswers = val
                 # Following code creates new column for a special question based on
                 # the different options selected for multiple select questions.
                 for idx, teacher in enumerate(teacherLevelAnswers):
                   # print(idx, teacher)
                   if teacher == '1':
                     responseData['TeacherClass'].append(1)
                     isTeacherClass = 'Y'
                   if teacher == '2':
                     responseData['TeacherLanguages'].append(1)
                     isTeacherLanguages = 'Y'
                   if teacher == '3':
                     responseData['TeacherMath'].append(1)
                     isTeacherMath = 'Y'
                   if teacher == '4':
                     responseData['TeacherCounselling'].append(1)
                     isTeacherCounselling = 'Y'
                   if teacher == '5':
                     responseData['TeacherReal'].append(1)
                     isTeacherReal = 'Y'
                   if teacher == '6':
                     responseData['TeacherArt'].append(1)
                     isTeacherArt = 'Y'
                   if teacher == '7':
                     responseData['TeacherSpecial'].append(1)
                     isTeacherSpecial = 'Y'
                   if teacher == '8':
                     responseData['TeacherOptional'].append(1)
                     isTeacherOptional = 'Y'
                   if teacher == '9':
                     responseData['TeacherVocational'].append(1)
                     isTeacherVocational = 'Y'
                   if teacher == '10':
                     responseData['TeacherGeneral'].append(1)
                     isTeacherGeneral = 'Y'
                   if teacher == '11':
                     responseData['NoTeacher'].append(1)
                     isNoTeacher = 'Y'
                 #####################################
                 # If certain options are not selected
                 if isTeacherClass == '':
                   responseData['TeacherClass'].append(0)
                 if isTeacherLanguages == '':
                   responseData['TeacherLanguages'].append(0)
                 if isTeacherMath == '':
                   responseData['TeacherMath'].append(0)
                 if isTeacherCounselling == '':
                   responseData['TeacherCounselling'].append(0)
                 if isTeacherReal == '':
                   responseData['TeacherReal'].append(0)
                 if isTeacherArt == '':
                   responseData['TeacherArt'].append(0)
                 if isTeacherSpecial == '':
                   responseData['TeacherSpecial'].append(0)
                 if isTeacherOptional == '':
                   responseData['TeacherOptional'].append(0)
                 if isTeacherVocational == '':
                   responseData['TeacherVocational'].append(0)
                 if isTeacherGeneral == '':
                   responseData['TeacherGeneral'].append(0)
                 if isNoTeacher == '':
                   responseData['NoTeacher'].append(0)
                 val = idx + 1
              # Other special processing being done.
              # If Column is present for Municipality
              if questionID == 'SPA':
                   provienceName = str(answerNew[0].encode('utf-8'))[2:-1]
                   print(provienceName)
                   val = provienceName
                   responseData['CountyCode'].append(answerNew[1])
              # If Column is present for Municipality
              if questionID == 'SPB':
                   municipalityName = str(answerNew[0].encode('utf-8'))[2:-1]
                   print(municipalityName)
                   val = municipalityName
                   responseData['MunicipalityCode'].push(str(answerNew[1]))
              # Normal processing without any extra processing.
              responseData[questionID].append(val)

            else:

              # If Column is not present for questions. This will only execute for the first time.
              if questionID == 'MS':
                isTeacherClass = ''
                isTeacherLanguages = ''
                isTeacherMath = ''
                isTeacherCounselling = ''
                isTeacherReal = ''
                isTeacherArt = ''
                isTeacherSpecial = ''
                isTeacherOptional = ''
                isTeacherVocational = ''
                isTeacherGeneral = ''
                isNoTeacher = ''
                teacherLevelAnswers = val
                # Following code creates new column for a special question based on
                # the different options selected for multiple select questions.
                for idx, teacher in enumerate(teacherLevelAnswers):
                  # print(idx, teacher)
                  if teacher == '1':
                    responseData['TeacherClass'] = [1]
                    isTeacherClass = 'Y'
                  if teacher == '2':
                    responseData['TeacherLanguages'] = [1]
                    isTeacherLanguages = 'Y'
                  if teacher == '3':
                    responseData['TeacherMath'] = [1]
                    isTeacherMath = 'Y'
                  if teacher == '4':
                    responseData['TeacherCounselling'] = [1]
                    isTeacherCounselling = 'Y'
                  if teacher == '5':
                    responseData['TeacherReal'] = [1]
                    isTeacherReal = 'Y'
                  if teacher == '6':
                    responseData['TeacherArt'] = [1]
                    isTeacherArt = 'Y'
                  if teacher == '7':
                    responseData['TeacherSpecial'] = [1]
                    isTeacherSpecial = 'Y'
                  if teacher == '8':
                    responseData['TeacherOptional'] = [1]
                    isTeacherOptional = 'Y'
                  if teacher == '9':
                    responseData['TeacherVocational'] = [1]
                    isTeacherVocational = 'Y'
                  if teacher == '10':
                    responseData['TeacherGeneral'] = [1]
                    isTeacherGeneral = 'Y'
                  if teacher == '11':
                    responseData['NoTeacher'] = [1]
                    isNoTeacher = 'Y'
                #####################################
                # If certain options are not selected
                if isTeacherClass == '':
                  responseData['TeacherClass'] = [0]
                if isTeacherLanguages == '':
                  responseData['TeacherLanguages'] = [0]
                if isTeacherMath == '':
                  responseData['TeacherMath'] = [0]
                if isTeacherCounselling == '':
                  responseData['TeacherCounselling'] = [0]
                if isTeacherReal == '':
                  responseData['TeacherReal'] = [0]
                if isTeacherArt == '':
                  responseData['TeacherArt'] = [0]
                if isTeacherSpecial == '':
                  responseData['TeacherSpecial'] = [0]
                if isTeacherOptional == '':
                  responseData['TeacherOptional'] = [0]
                if isTeacherVocational == '':
                  responseData['TeacherVocational'] = [0]
                if isTeacherGeneral == '':
                  responseData['TeacherGeneral'] = [0]
                if isNoTeacher == '':
                  responseData['NoTeacher'] = [0]
                val = idx + 1
              # Other special processing being done.
              # If Column is present for Municipality
              if questionID == 'SPA':
                provienceName = str(answerNew[0].encode('utf-8'))[2:-1]
                print(provienceName)
                val = provienceName
                responseData['CountyCode'] = str(answerNew[1])
              # If Column is present for Municipality
              if questionID == 'SPB':
                municipalityName = str(answerNew[0].encode('utf-8'))[2:-1]
                print(municipalityName)
                val = municipalityName
                responseData['MunicipalityCode'] = str(answerNew[1])
              responseData[questionID] = [val]

      ##########################################
      # for element, val in responseData.items():
          # print(len(val), element)
      # print('calling report header formatting function')
      res = self.formatBasicReportDump(responseData, headerFormattedResponseData)
      #res = responseData
      print('Report raw data: ')
      print(res)
      print('Response raw data ends')
      # formattedRes = {str(int(k.split(".")[0])) + str(k.split(".")[1]) : v for k, v in res.items()}
      # df = pd.DataFrame({str(int(k.split("+")[0])) + str(k.split("+")[1]) : v for k, v in res.items()})
      df = pd.DataFrame(res)
      # print("############################################################################")
      # print("df", df)
      # print("############################################################################")
      filepath = '{}-{}'.format(key, fileNameString)
      print(filepath)
      df.to_csv('{}{}.csv'.format(dirpath, filepath), index=False)
      return filepath
    except:
      print(traceback.format_exc())
      return "Failed from DB"

  ###################################################################
  def findMunicipalityDetails(self, mtee_municipality_code):
    data = mongo.finmtee_app_setting
    query = {'type': 'municipality'}
    codeToSearch = mtee_municipality_code
    municipalityList = data.find_one(query)
    response = []
    if municipalityList:
      for element in municipalityList['country_details']:
        if codeToSearch == str(element['mtee_municipality_code']):
          print ('Found!!!')
          response.append(element)
    return response

  ###################################################################
  def deleteLocationDetails(self, requestdata):
      data = mongo.finmtee_app_setting
      query = {'type': 'municipality'}
      municipalityToDelete = requestdata.get('mtee_municipality_code', None)
      userDetails = requestdata.get('mtee_user_id', None)
      user_action = ' '
      municipalityList = data.find_one(query)
      response = []
      if municipalityList:
        index = 0
        found = False
        if not municipalityToDelete:
          return 'Code missing'
        for element in municipalityList['country_details']:
          if int(municipalityToDelete) == int(element['mtee_municipality_code']):
            print('Found!!!')
            details = {}
            del municipalityList['country_details'][index]
            print('deleted')
            print(index)
            newvalues = {"country_details": municipalityList['country_details']}
            print(newvalues)
            data.update(query, {"$set": newvalues})
            user_action = 'Deleted'
            self.logLocationHistoryChanges(requestdata, user_action)
            return 'deleted with given code'
          index += 1
      return 'failed'

  ###################################################################
  def changeMunicipality(self, requestdata):
    data = mongo.finmtee_app_setting
    query = {'type': 'municipality'}
    newCode = requestdata.get('mtee_municipality_code_new', None)
    newFinName = requestdata.get('mtee_municipality_name_1_new', None)
    newSweName = requestdata.get('mtee_municipality_name_2_new', None)
    oldCode = requestdata.get('mtee_municipality_code', None)
    finName = requestdata.get('mtee_municipality_name_1', None)
    sweName = requestdata.get('mtee_municipality_name_2', None)
    userDetails = requestdata.get('mtee_user_id', None)
    user_action = ' '
    municipalityList = data.find_one(query)
    response = []
    if municipalityList:
      index = 0
      found = False
      if not newCode:
        return 'Code missing'

      # if not int(oldCode):
      #   print('Create new')
      #   details = {}
      #   details['mtee_county_provience_name_2'] = 'PINGPONG'
      #   details['mtee_county_provience_code'] = 909090
      #   details['mtee_country_name'] = 'FINLAND'
      #   details['mtee_county_provience_name_1'] = 'PING'
      #   details['mtee_municipality_code'] = int(newCode)
      #   details['mtee_country_code'] = 'FIN'
      #   details['mtee_municipality_name_2'] = newSweName
      #   details['mtee_municipality_name_1'] = newFinName
      #   municipalityList['country_details'].append(details)
      #   newvalues = {"country_details": municipalityList['country_details']}
      #   data.update(query, {"$set": newvalues})
      #   user_action = 'Created'
      #   self.logLocationHistoryChanges( requestdata, user_action)
      #   return 'Created'

      for element in municipalityList['country_details']:
        if int(newCode) == int(element['mtee_municipality_code']):
          print ('Found!!!')
          details = {}
          details['mtee_county_provience_name_2'] = element['mtee_municipality_name_1']
          details['mtee_county_provience_code'] = element['mtee_county_provience_code']
          details['mtee_country_name'] = element['mtee_county_provience_name_1']
          details['mtee_county_provience_name_1'] = element['mtee_county_provience_name_1']
          details['mtee_municipality_code'] = int(newCode)
          details['mtee_country_code'] = element['mtee_country_code']
          details['mtee_municipality_name_2'] = newSweName
          details['mtee_municipality_name_1'] = newFinName
          print(details, index)
          del municipalityList['country_details'][index]
          print('deleted')
          municipalityList['country_details'].append(details)
          newvalues = {"country_details": municipalityList['country_details']}
          data.update(query, {"$set": newvalues})
          user_action = 'Updated'
          self.logLocationHistoryChanges(requestdata, user_action)
          return 'Updated with same code'
        index += 1

      print('Create new')
      details = {}
      details['mtee_county_provience_name_2'] = 'PINGPONG'
      details['mtee_county_provience_code'] = 909090
      details['mtee_country_name'] = 'FINLAND'
      details['mtee_county_provience_name_1'] = 'PING'
      details['mtee_municipality_code'] = int(newCode)
      details['mtee_country_code'] = 'FIN'
      details['mtee_municipality_name_2'] = newSweName
      details['mtee_municipality_name_1'] = newFinName
      municipalityList['country_details'].append(details)
      newvalues = {"country_details": municipalityList['country_details']}
      data.update(query, {"$set": newvalues})
      user_action = 'Created New'
      self.logLocationHistoryChanges( requestdata, user_action)
      return 'Created New'

    return 'Failed'

  ###################################################################

  def logLocationHistoryChanges(self, requestdata, action):
    data = mongo.finmtee_location_history
    newCode = requestdata.get('mtee_municipality_code_new', None)
    newFinName = requestdata.get('mtee_municipality_name_1_new', None)
    newSweName = requestdata.get('mtee_municipality_name_2_new', None)
    oldCode = requestdata.get('mtee_municipality_code', None)
    finName = requestdata.get('mtee_municipality_name_1', None)
    sweName = requestdata.get('mtee_municipality_name_2', None)
    userDetails = requestdata.get('mtee_user_id', None)
    user_access_time = datetime.now()
    user_action = action
    if data.insert({
      'mtee_new_code': newCode,
      'mtee_new_fin_name': newFinName,
      'mtee_new_swe_name': newSweName,
      'mtee_old_code': oldCode,
      'mtee_old_fin_name': finName,
      'mtee_old_swe_name': sweName,
      'mtee_user_details': userDetails,
      'mtee_user_action': user_action,
      'mtee_user_access_time': user_access_time
    }):
      print(action)
      return jsonify({'status': 'success', 'result': 'success'}), 200, {"Content-Type": "application/json",
                                                                        "Access-Control-Allow-Origin": "*"}

  #########################################################################################################

  def updateLocationDetails(self, mtee_municipality_code):
    data = mongo.finmtee_app_setting
    query = {'type': 'municipality'}
    codeToSearch = mtee_municipality_code
    municipalityList = data.find_one(query)
    response = []
    if municipalityList:
      for element in municipalityList['country_details']:
        if codeToSearch == str(element['mtee_municipality_code']):
          print ('Found!!!')
          response.append(element)
    return response
  ###################################################################
  def modify(self):
    data = mongo.finmtee_questions
    query = {}
    for q in data.find(query, {'_id': False}):
      stringq = json.dumps(q)
      replaced = stringq.replace("FIN", "Finnish")
      replaced = stringq.replace("SWE", "Swedish")
      replaced = replaced.replace("ENG", "English")
      store = mongo.que_seq
      store.insert(json.loads(replaced))
    return jsonify({"result": "done", "status": "success"})

###################################################################
  def createCampaign(self, mtee_campaign_created_user_id,
                     mtee_campaign_created_date,
                     mtee_campaign_code,
                     mtee_campaign_type,
                     mtee_campaign_description,
                     mtee_campaign_start_date,
                     mtee_campaign_end_date,
                     mtee_campaign_status,
                     mtee_campaign_update_user_id,
                     mtee_campaign_update_date
                     ):
    data = mongo.finmtee_campaign_code
    if data.find_one({"mtee_campaign_code": mtee_campaign_code}):
      return jsonify({"status": "failed", "result": "Campaign code already exists"})
    else:
      if data.insert({
        'mtee_campaign_created_user_id': mtee_campaign_created_user_id,
        'mtee_campaign_created_date': mtee_campaign_created_date,
        'mtee_campaign_code': mtee_campaign_code,
        'mtee_campaign_type': mtee_campaign_type,
        'mtee_campaign_start_date': mtee_campaign_start_date,
        'mtee_campaign_end_date': mtee_campaign_end_date,
        'mtee_campaign_status': mtee_campaign_status,
        'mtee_campaign_update_user_id': mtee_campaign_update_user_id,
        'mtee_campaign_update_date': mtee_campaign_update_date
      }):
        return jsonify({'status': 'success', 'result': mtee_campaign_status})
      else:
        return jsonify({'status': 'failed', 'result': 'Unable to create campaign. Please try again!'})

###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################


###################################################################
