#------ IMPORTS ------#
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from deta import Deta
from fastapi.responses import ORJSONResponse
import json
import datetime
import uuid
import requests
#from fastapi.responses import JSONResponse



#------ START ------#
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]) # CORS settings
dbRoot = Deta("") # project data key



#------ VARIABLES ------#
dbSections = dbRoot.Base("sections") # creates db if does not exists
dbCategories = dbRoot.Base("categories")
dbData = dbRoot.Base("data")
dbUsers = dbRoot.Base("users")
# origins = ["http://localhost","http://localhost:8080"]


#------ QUICK NAV ------#
def _():
    #routes error (1)
    root

    #routes sections (4)
    section_all
    section_add
    section_edit
    section_delete

    #routes categories (4)
    category_all
    category_add
    category_edit
    category_delete

    #routes data (4)
    data_all
    data_add
    data_edit
    data_delete

    #routes users (12)
    user_all
    user_add
    user_sign_in
    user_sign_out
    user_specific
    user_update_data
    user_update_categories
    user_update_sections
    user_update_settings
    user_reset
    user_delete

    #routes domain (1)
    domain_specific

    #standalone functions (2)
    forbiddenCharacterCheck
    forbiddenNameCheck



#------ ROUTES ------#
@app.get("/", tags=['root']) #response_class=JSONResponse #ORJSONResponse([{"root": "there is nothing here"}])
async def root(): return {"data": "there is nothing here"}



# 1. section all
@app.get("/section-all", tags=['sections'])
async def section_all():
    sectionsFromDb = dbSections.fetch() #next(dbSections.fetch())
    #carsParsed = []
    #for car in carsFromDb:
        #c = {"id": car["id"], "lastEdited": car["lastEdited"], "model": "S", "title": car["title"], "versions": car["versions"]}
        #carsParsed.append(c)
    return {"sections": sectionsFromDb}



# 2. section add
@app.post("/section-add", tags=['sections'])
async def section_add(request: Request):
    #variables
    sectionObj = await request.json()
    
    #update DB
    dbSections.insert(sectionObj)
    
    #response
    return {"data": "section added successfully"} 



# 3. section edit
@app.post("/section-edit/{key}", tags=['sections'])
async def section_edit(key, request: Request):
    #variables
    sectionObj = await request.json()
    
    #update DB
    dbSections.update(sectionObj, key)
    
    #reponse
    return {"data": "section: " + str(sectionObj['title']) + " edited successfully"}



# 4. section delete
@app.post("/section-delete/{key}", tags=['sections'])
async def section_delete(key, request: Request):
    #update DB
    dbSections.delete(key)
    
    #response
    return {"data": "section deleted successfully"}



# 5. category all
@app.get("/category-all", tags=['categories'])
async def category_all(): 
    #fetch data
    categoriesFromDb = dbCategories.fetch()
    
    #response
    return {"categories": categoriesFromDb}



# 6. category add
@app.post("/category-add", tags=['categories'])
async def category_add(request: Request): 
    #variables
    categoryObj = await request.json()

    #update DB
    dbCategories.insert(categoryObj)

    #repsonse
    return {"data": "category added successfully"}



# 7. category edit
@app.post("/category-edit/{key}", tags=['categories'])
async def category_edit(key, request: Request):
    #variables
    categoryObj = await request.json() #request.body()

    #update DB
    dbCategories.update(categoryObj, key) #update

    #response
    return {"data": "category: " + str(categoryObj['title']) + " edited successfully"} #response



# 8. category delete
@app.post("/category-delete/{key}", tags=['categories'])
async def category_delete(key, request: Request):
    #update DB
    dbCategories.delete(key)

    #response
    return {"data": "category deleted successfully"} 



# 9. data all
@app.get("/data", tags=['data'])
async def data_all(section=None, category=None):
    if category != None and section != None:
        dataFromDb = dbData.fetch({"section": section, "category": category})
        return {"data": dataFromDb}
    elif section != None:
        dataFromDb = dbData.fetch({"section": section})
        return {"data": dataFromDb}
    else:
        dataFromDb = dbData.fetch()
        return {"data": dataFromDb}



# 10. data add
@app.post("/add-data", tags=['data'])
async def data_add(request: Request):
    dataObj = await request.json()
    dbData.insert(dataObj) #insert
    return {"data": "data added successfully"}



# 11. data edit
@app.post("/edit-data/{key}", tags=['data'])
async def data_edit(key, request: Request):
    dataObj = await request.json() #request.body()
    dbData.update(dataObj, key) #update
    return {"data": "data: " + str(dataObj['category']) + " edited successfully"} #response



# 12. data delete
@app.post("/delete-data/{key}", tags=['data']) #data delete
async def data_delete(key, request: Request):
    dbData.delete(key) #delete
    return {"data": "data deleted successfully"} #response



# 13. user all
@app.get("/users", tags=['users']) 
async def user_all(): 
    usersFromDb = dbUsers.fetch()
    return {"users": usersFromDb}



# 14. add user
@app.post("/add-user", tags=['users'])
async def user_add(request: Request):
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json
    # json.dumps(dataObj) # convert to json
    # print(dataObj)

    #set user obj
    dataObj["createdAt"] = str(datetime.datetime.now())[:-7]
    dataObj["id"] = str(uuid.uuid4()).replace("-", "")
    dataObj["sections"] = []
    dataObj["categories"] = []
    dataObj["data"] = []
    dataObj["settings"] = {
        "buttonAbout": "false",
        "buttonAboutText": "",
        "buttonContact": "false",
        "buttonFullscreen": "false",
        "buttonSearch": "false",
        "colorLoadingScreen": "#000000",
        "colorNavBackground": "#000000",
        "colorNavIcons": "#000000",
        "colorSectionsBackground": "#000000",
        "colorText": "#000000",
        "loadingScreen": "false",
        "loadingScreenUrl": "",
        "modeSlideshow": "false",
        "navIconSize": "medium",
        "navIconType": "numbers",
        "navPosition": "left",
        "pageEnd": "false",
        "pageEndText": "",
        "pageEndTitle": "",
        "pageIndex": "false",
        "pageStart": "false",
        "pageStartText": "",
        "pageStartTitle": "",
        "sectionBackgroundImage": "false",
        "sectionBackgroundImageUrl": "",
        "siteAccess": "public",
        "sitePasswordProtected": "false",
        "sitePasswordProtectedPassword": "",
        "textSize": "medium",
        "textStyle": "normal"
    }
    dataObj["token"] = ""
    dataObj["domain"] = ""
    dataObj["email"] = ""
    dataObj["name"] = ""
    dataObj["phone"] = ""
    dataObj["country"] = ""
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
    dbUsers.insert(dataObj); return {"status": "user added successfully"} #response



# 15. sign in user
@app.post("/sign-in-user", tags=['users'])
async def user_sign_in(request: Request):
    #debugging
    # print("sign-in-user")

    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json
    # json.dumps(dataObj) # convert to json
    # print(dataObj)
    
    username = dataObj["username"]
    password = dataObj["password"]
    correctUserObj = ""

    dbUsersObj = dbUsers._fetch()
    allUsers = dbUsersObj[1]["items"]

    for item in allUsers:
        if(username == item["username"] and password == item["password"]): 
            print(item)
            correctUserObj = item
            correctUserObj["token"] = str(uuid.uuid4()).replace("-", "")
            correctUserObj["lastLogin"] = str(datetime.datetime.now())
            break

    if(correctUserObj == ""): 
        return {"status": "user login failed"}
        
    elif(correctUserObj != ""): 
        dbUsers.put(correctUserObj)
        return {
                  "status": "user login successful", 
                  "account": correctUserObj["username"], 
                  "lastLogin": correctUserObj["lastLogin"],
                  "token": correctUserObj["token"]
                }



# 16. sign out user 
@app.post("/sign-out-user", tags=['users'])
async def user_sign_out(request: Request):
    print("sign-out-user")
    # return {"status": "logout test"}



# 17. get specific user
@app.post("/specific-user", tags=['users'])
async def user_specific(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json
    # dataObj = json.dumps(dataObj) # convert to json
    # print(dataObj)

    #variables
    username = dataObj["username"]
    token = dataObj["token"]
    lastLogin = dataObj["lastLogin"]

    #log
    print("specific-user: " + username)

    #fetch account data
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
    accountCredentials = {
        "username": accountUsername,
        "domain": accountDomain,
        "email": accountEmail,
        "name": accountName,
        "country": accountCountry,
        "phone": accountPhone
    }
    accountInfo = {
        "lastLogin": accountLastLogin,
        "createdAt": accountCreatedAt,
        "accountStatus": accountStatus
    }

    return { 
             "status": "fetch specific user successful",
             "sections": accountSections, 
             "categories": accountCategories, 
             "data": accountData,
             "settings": accountSetttings,
             "credentials": accountCredentials,
             "info": accountInfo
           }



# 18. get specific domain
@app.post("/specific-domain", tags=['users'])
async def domain_specific(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json
    # dataObj = json.dumps(dataObj) # convert to json
    # print(dataObj)

    #variables
    domain = dataObj["domain"]

    #log
    print("specific-domain: " + domain)

    #fetch account data
    dbRequestAccountData = dbUsers._fetch({"domain": domain})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountSections = accountObj["sections"]
    accountCategories = accountObj["categories"]
    accountData = accountObj["data"]
    accountSetttings = accountObj["settings"]

    return { 
             "status": "fetch specific user successful",
             "sections": accountSections, 
             "categories": accountCategories, 
             "data": accountData,
             "settings": accountSetttings,
           }



# 19. update user data
@app.post("/update-user-data", tags=['users'])
async def user_update_data(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json  
    # dataObj = json.dumps(dataObj) # convert to json

    #variables
    userInfo = dataObj[0]
    newData = json.loads(dataObj[1])
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]
    # print(userInfo)
    # print(newData)

    #log
    print("update-user-data: " + username)

    #fetch account data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    
    #update account data
    try: dbUsers.update({"data": newData}, accountKey); return { "status": "update user data successful" }
    except: return { "status": "update user data failed" }



# 20. update user categories
@app.post("/update-user-categories", tags=['users'])
async def user_update_categories(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json  
    # dataObj = json.dumps(dataObj) # convert to json
    
    #variables
    userInfo = dataObj[0]
    newCategories = json.loads(dataObj[1])
    newData = json.loads(dataObj[2])
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]
    # print(userInfo)
    # print(newCategories)
    # print(newData)

    #log
    print("update-user-categories: " + username)

    #fetch account data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    
    #update account categories & data
    try: 
        dbUsers.update({"categories": newCategories}, accountKey); 
        dbUsers.update({"data": newData}, accountKey); 
        return { "status": "update user categories successful" }
        
    except: 
        return { "status": "update user categories failed" }



# 21. update user sections
@app.post("/update-user-sections", tags=['users'])
async def user_update_sections(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json  
    # dataObj = json.dumps(dataObj) # convert to json
    
    #variables
    userInfo = dataObj[0]
    newSections = json.loads(dataObj[1])
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]
    # print(userInfo)
    # print(newSections)

    #log
    print("update-user-sections: " + username)

    #fetch account data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    
    #update account sections & data
    try: 
        dbUsers.update({"sections": newSections}, accountKey); 
        return { "status": "update user sections successful" }
        
    except: 
        return { "status": "update user sections failed" }



# 22. update user settings
@app.post("/update-user-settings", tags=['users'])
async def user_update_settings(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json  
    # dataObj = json.dumps(dataObj) # convert to json
    
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

    #log
    print("update-user-settings: " + username)

    #fetch account data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    # print(accountObj)
    # print("username:" + accountObj['username'])
    # print("password:" + accountObj['password'])
    # print("newPassword: " + newPassword)
    # print("oldPassword: " + oldPassword)

    #check new settings
    if(newSettings != ''): 
        newSettingsPassedCheck = True
        
    #check new email
    if(newEmail != '' and newEmail != accountObj['email']):
        newEmailPassedCheck = True

    #check new name
    if(newName != '' and newName != accountObj['name']): 
        newNamePassedCheck = True

    #check new phone
    if(newPhone != '' and newPhone != accountObj['phone']): 
        newPhonePassedCheck = True

    #check new country
    if(newCountry != '' and newCountry != accountObj['country']): 
        newCountryPassedCheck = True

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

    #update account
    try: 
        #update account settings
        if(newSettingsPassedCheck == True): dbUsers.update({"settings": newSettings}, accountKey)

        #update account credentials
        if(usernameIsAvailable == True): dbUsers.update({"username": newUsername}, accountKey)
        if(domainIsAvailable == True): dbUsers.update({"domain": newDomain}, accountKey) 
        if(newEmailPassedCheck == True): dbUsers.update({"email": newEmail}, accountKey) 
        if(newNamePassedCheck == True): dbUsers.update({"name": newName}, accountKey)
        if(newPhonePassedCheck == True): dbUsers.update({"phone": newPhone}, accountKey)
        if(newCountryPassedCheck == True): dbUsers.update({"country": newCountry}, accountKey)
        if(newPasswordPassedCheck == True): dbUsers.update({"password": newPassword}, accountKey) 

        return { "status": "update user settings successful" }
        
    except: 
        return { "status": "update user settings failed" }



# 23. reset user
@app.post("/reset-user", tags=['users'])
async def user_reset(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json  
    # dataObj = json.dumps(dataObj) # convert to json
    
    #variables
    password = dataObj['password']
    userInfo = dataObj['userInfo']
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]
    defaultSettings = {
        "buttonAbout": "false",
		"buttonAboutText": "",
		"buttonContact": "false",
		"buttonFullscreen": "false",
		"buttonSearch": "false",
		"colorLoadingScreen": "#000000",
		"colorNavBackground": "#000000",
		"colorNavIcons": "#000000",
		"colorSectionsBackground": "#000000",
		"colorText": "#000000",
		"loadingScreen": "false",
		"loadingScreenUrl": "",
		"modeSlideshow": "false",
		"navIconSize": "medium",
		"navIconType": "numbers",
		"navPosition": "left",
		"pageEnd": "false",
		"pageEndText": "",
		"pageEndTitle": "",
		"pageIndex": "false",
		"pageStart": "false",
		"pageStartText": "",
		"pageStartTitle": "",
		"sectionBackgroundImage": "false",
		"sectionBackgroundImageUrl": "",
		"siteAccess": "public",
		"sitePasswordProtected": "false",
		"sitePasswordProtectedPassword": "",
		"textSize": "medium",
		"textStyle": "normal"
    }
    # print(newSettings)
    # print(userInfo)

    #log
    print("reset-user: " + username)

    #fetch account data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    # print(accountObj)

    #reset account
    try: 
        if(password == accountObj["password"]):
            dbUsers.update({
                "domain": "",
                "email": "",
                "name": "",
                "phone": "",
                "country": "",
                "settings": defaultSettings,
                "sections": [],
                "categories": [],
                "data": []},
            accountKey)
            return { "status": "update user reset successful" }

        else: return { "status": "update user reset failed: password is incorrect" }
        
    except: 
        return { "status": "update user reset failed" }



# 24. delete user
@app.post("/delete-user", tags=['users'])
async def user_delete(request: Request):
    #parse request data
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json  
    # dataObj = json.dumps(dataObj) # convert to json
    
    #variables
    password = dataObj['password']
    userInfo = dataObj['userInfo']
    username = userInfo["username"]
    token = userInfo["token"]
    lastLogin = userInfo["lastLogin"]
    print(userInfo)
    
    #log
    print("delete-user: " + username)

    #fetch account data
    dbRequestAccountData = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    accountObj = dbRequestAccountData[1]["items"][0]
    accountKey = accountObj["key"]
    # print(accountObj)

    #delete account
    try: 
        if(password == accountObj["password"]):
            dbUsers.delete(accountKey)
            return { "status": "delete user successful" }
        
        else: 
            return { "status": "delete user failed: password is incorrect" }
        
    except: 
        return { "status": "update user reset failed" }




#------ functions -------#
def forbiddenNameCheck(value):
    forbiddenNames = ["temp", "null", "domain", "empty", "blank", "undefined", "none", " "]

    for item in forbiddenNames: 
        if(value == item): return False

    for item in forbiddenNames: 
        if(item in value): return False



def forbiddenCharacterCheck(value):
    forbiddenCharacters = [" ", "!", "@", "$", "%", ",", ".", "<", ">", "'", "\"", "_", "-", "?", "|", "-", "^", "`", "/", "\\"]

    for item in forbiddenCharacters: 
        if (value == item): return False

    for item in forbiddenCharacters: 
        if (item in value): return False