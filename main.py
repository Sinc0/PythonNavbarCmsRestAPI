#------ IMPORTS ------#
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from deta import Deta
import json
import datetime
import uuid
# from fastapi.responses import ORJSONResponse
# from pprint import pprint
# import requests
#from fastapi.responses import JSONResponse



#------ GLOBALS ------#
PROJECT_DATA_KEY = ""
DEFAULT_DOMAIN = ""
DEFAULT_SETTINGS = ""
DEFAULT_SECTIONS = ""
DEFAULT_CATEGORIES = ""
DEFAULT_DATA = ""
dbUsers = ""



#------ START ------#
with open('configs.json') as data: PROJECT_DATA_KEY = json.load(data)["PROJECT_DATA_KEY"]
with open('configs.json') as data: PROJECT_DATA_KEY = json.load(data)["DEFAULT_DOMAIN"]
with open('defaultSettings.json') as data: DEFAULT_SETTINGS = json.load(data)
with open('defaultSections.json') as data: DEFAULT_SECTIONS = json.load(data)
with open('defaultCategories.json') as data: DEFAULT_CATEGORIES = json.load(data)
with open('defaultData.json') as data: DEFAULT_DATA = json.load(data)
dbRoot = Deta(PROJECT_DATA_KEY)
dbUsers = dbRoot.Base("users")
app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_credentials=True, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)



#------ QUICK NAV ------#
def _():
    #routes
    root
    user_all
    user_add
    user_sign_in
    user_specific
    user_update_data
    user_update_categories
    user_update_sections
    user_update_settings
    user_reset
    user_delete
    domain_specific
    domain_protected

    #functions
    forbiddenCharacterCheck
    forbiddenNameCheck
    cleanObjects



#------ ROUTES ------#
@app.get("/", tags=['root']) #response_class=JSONResponse
async def root(): return { "data": "there is nothing here" }



#route: user all
@app.get("/user-all", tags=['users']) 
async def user_all():
    #fetch all users
    usersFromDb = dbUsers.fetch()
    
    #return value
    return { "users": usersFromDb }



#route: add user
@app.post("/user-add", tags=['users'])
async def user_add(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json
    # json.dumps(dataObj) # convert to json

    #debugging
    # print(dataObj)

    #set user obj
    dataObj["createdAt"] = str(datetime.datetime.now())[:-7]
    dataObj["id"] = str(uuid.uuid4()).replace("-", "")
    dataObj["sections"] = DEFAULT_SECTIONS
    dataObj["categories"] = DEFAULT_CATEGORIES
    dataObj["data"] = DEFAULT_DATA
    dataObj["settings"] = DEFAULT_SETTINGS
    dataObj["token"] = ""
    dataObj["domain"] = str(uuid.uuid4()).replace("-", "")[:20]
    dataObj["email"] = "example@email.com"
    dataObj["name"] = "name"
    dataObj["phone"] = "+123456789"
    dataObj["country"] = "country"
    dataObj["accountStatus"] = "active"
    
    #check total users
    dbUsersObj = dbUsers._fetch() 
    totalUsers = dbUsersObj[1]["paging"]["size"]
    
    #log
    print("Accounts = " + str(totalUsers))

    #check forbidden name 
    if(forbiddenNameCheck(dataObj["username"]) == False): return { "status": "username is unavailable" }

    #check forbidden character
    if(forbiddenCharacterCheck(dataObj["username"]) == False): return { "status": "username is unavailable" }

    #check if registration is closed
    if(totalUsers > 100): return { "status": "user registration is closed"}

    #check if username is taken
    for user in dbUsersObj[1]["items"]:
        if(dataObj["username"] == user["username"]): return { "status": "username is taken"}

    #update db
    dbUsers.insert(dataObj); return { "status": "user added successfully" }



#route: sign in user
@app.post("/user-sign-in", tags=['users'])
async def user_sign_in(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj)
    
    username = dataObj["username"]
    password = dataObj["password"]
    correctUserObj = ""

    #log
    print("sign-in-user: " + username)

    #fetch all users
    dbUsersObj = dbUsers._fetch()
    allUsers = dbUsersObj[1]["items"]

    #check if username and password match
    for item in allUsers:
        if(username == item["username"] and password == item["password"]): 
            print(item)
            correctUserObj = item
            correctUserObj["token"] = str(uuid.uuid4()).replace("-", "")
            correctUserObj["lastLogin"] = str(datetime.datetime.now())
            break
    
    #update DB
    if(correctUserObj != ""): 
        dbUsers.put(correctUserObj)
        return { "status": "user login successful", 
                 "account": correctUserObj["username"], 
                 "lastLogin": correctUserObj["lastLogin"],
                 "token": correctUserObj["token"] }

    #login error
    elif(correctUserObj == ""): 
        return {"status": "user login failed"}



#route: get specific user
@app.post("/user-specific", tags=['users'])
async def user_specific(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj)

    #debugging
    # print(dataObj)

    #variables
    username = dataObj["username"]
    token = dataObj["token"]
    lastLogin = dataObj["lastLogin"]

    #log
    print("user-specific: " + username)

    #fetch user data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountUsername = accountObj["username"]
    accountCreatedAt = accountObj["createdAt"]
    accountLastLogin = accountObj["lastLogin"]
    accountSections = accountObj["sections"]
    accountCategories = accountObj["categories"]
    accountData = accountObj["data"]
    accountSetttings = accountObj["settings"]
    accountDomain = accountObj["domain"]
    accountEmail = accountObj["email"]
    accountName = accountObj["name"]
    accountCountry = accountObj["country"]
    accountPhone = accountObj["phone"]
    accountStatus = accountObj["accountStatus"]
    accountInfo = { "lastLogin": accountLastLogin, "createdAt": accountCreatedAt, "accountStatus": accountStatus }
    accountCredentials = { "username": accountUsername,"domain": accountDomain,"email": accountEmail,"name": accountName,"country": accountCountry,"phone": accountPhone }

    #return value
    return { "status": "fetch specific user successful",
             "sections": accountSections, 
             "categories": accountCategories, 
             "data": accountData,
             "settings": accountSetttings,
             "credentials": accountCredentials,
             "info": accountInfo }



#route: update user data
@app.post("/user-update-data", tags=['users'])
async def user_update_data(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj)

    #variables
    userInfo = dataObj[0]
    newData = json.loads(dataObj[1])
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]

    #debugging
    # print(userInfo)
    # print(newData)

    #log
    print("user-update-data: " + username)

    #fetch user data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    
    #update user data
    try: dbUsers.update({"data": newData}, accountKey); return { "status": "update user data successful" }

    #update error
    except: return { "status": "update user data failed" }



#route: update user categories
@app.post("/user-update-categories", tags=['users'])
async def user_update_categories(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj)
    
    #variables
    userInfo = dataObj[0]
    newCategories = json.loads(dataObj[1])
    newData = json.loads(dataObj[2])
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]

    #debugging
    # print(userInfo)
    # print(newCategories)
    # print(newData)

    #log
    print("user-update-categories: " + username)

    #fetch user data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    
    #update user categories & data
    try: 
        dbUsers.update({"categories": newCategories}, accountKey); 
        dbUsers.update({"data": newData}, accountKey); 
        return { "status": "update user categories successful" }
    
    #update error
    except: 
        return { "status": "update user categories failed" }



#route: update user sections
@app.post("/user-update-sections", tags=['users'])
async def user_update_sections(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) 
    
    #variables
    userInfo = dataObj[0]
    newSections = json.loads(dataObj[1])
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]
    # print(userInfo)
    # print(newSections)

    #log
    print("user-update-sections: " + username)

    #fetch user data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    # accountSectionsOld = accountObj["sections"]
        
    #update user sections & data
    try: 
        dbUsers.update({"sections": newSections}, accountKey)
        dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
        cleanObjects(dbRequestAccountData, accountKey, "updateSections") #remove associated categories and data
        return { "status": "update user sections successful" }
    
    #update error
    except:
        return { "status": "update user sections failed" }



#route: update user settings
@app.post("/user-update-settings", tags=['users'])
async def user_update_settings(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) 
    
    #variables
    newCredentials = dataObj['credentials']
    newSettings = dataObj['settings']
    userInfo = dataObj['userInfo']
    newUsername = newCredentials['usernameNew']
    newDomain = newCredentials['domain']
    newEmail = newCredentials['email']
    newName = newCredentials['name']
    newPhone = newCredentials['phone']
    newCountry = newCredentials['country']
    newPassword = newCredentials['passwordNew']
    oldPassword = newCredentials['passwordOld']
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]
    newSettingsPassedCheck = False
    newPasswordPassedCheck = False
    newEmailPassedCheck = False
    newNamePassedCheck = False
    newPhonePassedCheck = False
    newCountryPassedCheck = False
    usernameIsAvailable = False
    domainIsAvailable = False

    print(newCredentials)
    # print(newSettings)
    # print(userInfo)

    #convert to lower case
    newUsername = newUsername.lower()
    newDomain = newDomain.lower()
    newEmail = newEmail.lower()

    #log
    print("user-update-settings: " + username)

    #fetch user data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    # print(accountObj)
    # print("username:" + accountObj['username'])
    # print("password:" + accountObj['password'])
    # print("newPassword: " + newPassword)
    # print("oldPassword: " + oldPassword)
    
    #check new settings
    if(newSettings != ''): newSettingsPassedCheck = True
        
    #check new credentials
    if(newEmail != accountObj['email']): newEmailPassedCheck = True
    if(newName != accountObj['name']): newNamePassedCheck = True
    if(newPhone != accountObj['phone']): newPhonePassedCheck = True
    if(newCountry != accountObj['country']): newCountryPassedCheck = True

    #check new password
    if(newPassword != '' and oldPassword != ''):
        if(oldPassword != accountObj['password']): return { "status": "update user settings failed: old password is incorrect" }
        else: newPasswordPassedCheck = True
    
    #check new username
    if(newUsername != '' and newUsername != accountObj['username']): 
        if(forbiddenNameCheck(newUsername) == False): return { "status": "update user settings failed: username is unavailable" }
        
        elif(forbiddenCharacterCheck(newUsername) == False): return { "status": "update user settings failed: username is unavailable" }
        
        else: 
            dbRequestCheckUsernameIsAvailable = dbUsers._fetch({"username": newUsername})
            if(dbRequestCheckUsernameIsAvailable[1]['paging']['size'] == 0): usernameIsAvailable = True
            else: return { "status": "update user settings failed: username is unavailable" }
    
    #check new domain
    if(newDomain != '' and newDomain != accountObj['domain']):
        if(forbiddenNameCheck(newDomain) == False): return { "status": "update user settings failed: domain is unavailable" }
        
        elif(forbiddenCharacterCheck(newDomain) == False): return { "status": "update user settings failed: domain is unavailable" }
        
        else:
            dbRequestCheckDomainIsAvailable = dbUsers._fetch({"domain": newDomain})
            if(dbRequestCheckDomainIsAvailable[1]['paging']['size'] == 0): domainIsAvailable = True
            else: return { "status": "update user settings failed: domain is unavailable" }

    #update user settings & credentials
    try: 
        #update user settings
        if(newSettingsPassedCheck == True): dbUsers.update({"settings": newSettings}, accountKey)

        #update user credentials
        if(usernameIsAvailable == True): dbUsers.update({"username": newUsername}, accountKey)
        if(domainIsAvailable == True): dbUsers.update({"domain": newDomain}, accountKey) 
        if(newEmailPassedCheck == True): dbUsers.update({"email": newEmail}, accountKey) 
        if(newNamePassedCheck == True): dbUsers.update({"name": newName}, accountKey)
        if(newPhonePassedCheck == True): dbUsers.update({"phone": newPhone}, accountKey)
        if(newCountryPassedCheck == True): dbUsers.update({"country": newCountry}, accountKey)
        if(newPasswordPassedCheck == True): dbUsers.update({"password": newPassword}, accountKey) 

        #return value
        return { "status": "update user settings successful" }
    
    #update error
    except: return { "status": "update user settings failed" }



#route: reset user
@app.post("/user-reset", tags=['users'])
async def user_reset(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) 
    
    #variables
    password = dataObj['password']
    userInfo = dataObj['userInfo']
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]
    settings = DEFAULT_SETTINGS
    passwordPass = False
    # print(newSettings)
    # print(userInfo)

    #log
    print("user-reset: " + username)

    #fetch user data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    # print(accountObj)

    if(password == accountObj["password"]): passwordPass = True
    else: return { "status": "update user reset failed: password is incorrect" }

    #reset account
    try: 
        if(passwordPass == True):
            dbUsers.update({ "domain": "",
                             "email": "",
                             "name": "",
                             "phone": "",
                             "country": "",
                             "settings": settings,
                             "sections": [],
                             "categories": [],
                             "data": [] },accountKey)

        return { "status": "update user reset successful" }

        
    
    #reset error
    except: return { "status": "update user reset failed" }



#route: delete user
@app.post("/user-delete", tags=['users'])
async def user_delete(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj)  
    
    #variables
    password = dataObj['password']
    userInfo = dataObj['userInfo']
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]
    print(userInfo)
    
    #log
    print("user-delete: " + username)

    #fetch user data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    # print(accountObj)

    #delete account
    try: 
        if(password == accountObj["password"]):
            dbUsers.delete(accountKey)
            return { "status": "delete user successful" }
        
        else: return { "status": "delete user failed: password is incorrect" }
    
    #delete error
    except: return { "status": "update user reset failed" }



#route: get specific domain
@app.post("/domain-specific", tags=['domain'])
async def domain_specific(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj)

    #debugging
    # print(dataObj)

    #variables
    data = dataObj["data"]
    domain = data["domain"]
    section = data["section"]
    category = data["category"]
    route = domain + "/" + section + "/" + category
    routeParams = data
    print(domain)
    print(route)

    #log
    print("domain-specific: " + domain)

    #fetch domain data
    dbRequestAccountData = dbUsers._fetch({"domain": domain})
    domainObj = dbRequestAccountData[1]["paging"]["size"]

    #domain does not exist
    if(dbRequestAccountData[1]["paging"]["size"] == 0):
        return { "status": "domain does not exist" }
    
    #domain exists
    else:
        domainObj = dbRequestAccountData[1]["items"][0]
 
        #set domain data
        domainSections = domainObj["sections"]
        domainCategories = domainObj["categories"]
        domainData = domainObj["data"]
        domainSettings = domainObj["settings"]
        domainEmail = domainObj["email"]
        domainName = domainObj["name"]
        domainPhone = domainObj["phone"]
        domainCountry = domainObj["country"]
        domainContact = ""
        
        #check if site is private
        if(domainSettings["siteAccess"] == "private"):
            return { "status": "domain does not exist", "domainName": domain }

        #check if site is password protected
        if(domainSettings["sitePasswordProtected"] == "true"):
            return { "status": "domain is password protected", "domainName": domain }    

        #check if contact button is enabled
        if(domainSettings["buttonContact"] == "true"):
            domainContact = { "email": domainEmail, "name": domainName, "phone": domainPhone, "country": domainCountry }
            
        #domain is not password protected
        return { "status": "fetch specific domain successful",
                "sections": domainSections, 
                "categories": domainCategories, 
                "data": domainData,
                "settings": domainSettings,
                "contact": domainContact,
                "route": routeParams }



#route: domain protected
@app.post("/domain-protected", tags=['domain'])
async def domain_protected(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj)

    #debugging
    # print(dataObj)

    #variables
    domainName = dataObj["domainName"]
    domainPassword = dataObj["domainPassword"]

    #fetch domain data
    dbRequestAccountData = dbUsers._fetch({"domain": domainName})
    domainObj = dbRequestAccountData[1]["items"][0]
    domainSections = domainObj["sections"]
    domainCategories = domainObj["categories"]
    domainData = domainObj["data"]
    domainSettings = domainObj["settings"]
    domainEmail = domainObj["email"]
    domainName = domainObj["name"]
    domainPhone = domainObj["phone"]
    domainCountry = domainObj["country"]
    domainContact = ""

    # print("domain-protected: " + domain)
    
    if(domainPassword == domainObj["settings"]["sitePasswordProtectedPassword"]):
        
        #check if contact button is enabled
        if(domainSettings["buttonContact"] == "true"):
            domainContact = { "email": domainEmail, "name": domainName, "phone": domainPhone, "country": domainCountry }

        return { "status": "fetch protected domain successful",
             "sections": domainSections, 
             "categories": domainCategories, 
             "data": domainData,
             "settings": domainSettings,
             "contact": domainContact }

    else: return {"status": "fetch protected domain failed" }



#------ functions -------#
def forbiddenNameCheck(value):
    #variables
    forbiddenNames = ["temp", "null", "domain", "empty", "blank", "undefined", "none", " "]

    #check if value == name
    for item in forbiddenNames: 
        if(value == item): return False

    #check if value is in name
    for item in forbiddenNames: 
        if(item in value): return False



def forbiddenCharacterCheck(value):
    #variables
    forbiddenCharacters = [" ", "!", "@", "$", "%", ",", ".", "<", ">", "'", "\"", "_", "?", "|", "^", "`", "/", "\\"] #removed from list: "-"

    #check if value == name
    for item in forbiddenCharacters:
        if (value == item): return False

    #check if value is in name
    for item in forbiddenCharacters:
        if (item in value): return False



def cleanObjects(dbRequestAccountData, accountKey, type):
    #clean categories & data
    accountObj = dbRequestAccountData[1]["items"][0]
    accountSections = json.loads(str(accountObj["sections"]).replace("'", "\"").replace("None", "\"None\"").replace("none", "\"none\""))
    accountCategories = json.loads(str(accountObj["categories"]).replace("'", "\"").replace("None", "\"None\"").replace("none", "\"none\""))
    accountData = accountObj["data"]    
    totalSections = len(accountSections)
    totalCategories = len(accountCategories)
    totalData = len(accountData)
    arraySections = []
    arrayCategories = []
    arrayData = []
    arrayCategoriesNew = []
    arrayDataNew = []

    # print("totalSections: " + str(totalSections))
    # print("totalCategories: " + str(totalCategories))
    # print("totalData: " + str(totalData))

    for item in accountSections:
        arraySections.append(item["title"])

    for item in accountCategories:
        arrayCategories.append(item)

    for item in accountData:
        arrayData.append(item)

    # print(arraySections)
    # print(arrayCategories)
    # print(arrayData)
    
    #remove categories
    for s in arraySections:
        for c in arrayCategories:
            if(c["section"] == s): arrayCategoriesNew.append(c)

    #remove data
    for s in arraySections:
        for d in arrayData:
            if(d["section"] == s): arrayDataNew.append(d)
    
    if(type == "updateSections"):
        dbUsers.update({"categories": arrayCategoriesNew}, accountKey)
        dbUsers.update({"data": arrayDataNew}, accountKey)