#------ imports ------#
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



#------ initializations ------#
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]) # CORS settings
dbRoot = Deta("") # project data key



#------ variables ------#
dbSections = dbRoot.Base("sections") # creates db if does not exists
dbCategories = dbRoot.Base("categories")
dbData = dbRoot.Base("data")
dbUsers = dbRoot.Base("users")
# origins = ["http://localhost","http://localhost:8080"]



#------ root ------#
@app.get("/", tags=['root']) #response_class=JSONResponse #ORJSONResponse([{"root": "there is nothing here"}])
async def root(): return {"data": "there is nothing here"}



#------ sections ------#
@app.get("/sections", tags=['sections'])
async def sections():
    sectionsFromDb = dbSections.fetch() #next(dbSections.fetch())
    #carsParsed = []
    #for car in carsFromDb:
        #c = {"id": car["id"], "lastEdited": car["lastEdited"], "model": "S", "title": car["title"], "versions": car["versions"]}
        #carsParsed.append(c)
    return {"sections": sectionsFromDb}


@app.post("/add-section", tags=['sections'])
async def addSection(request: Request):
    sectionObj = await request.json()
    dbSections.insert(sectionObj) #insert
    return {"data": "section added successfully"} #response


@app.post("/edit-section/{key}", tags=['sections'])
async def editSection(key, request: Request):
    sectionObj = await request.json() #request.body()
    dbSections.update(sectionObj, key) #update
    return {"data": "section: " + str(sectionObj['title']) + " edited successfully"} #response


@app.post("/delete-section/{key}", tags=['sections'])
async def deleteSection(key, request: Request):
    dbSections.delete(key) #delete
    return {"data": "section deleted successfully"} #response



#------ categories ------#
@app.get("/categories", tags=['categories'])
async def categories(): categoriesFromDb = dbCategories.fetch(); return {"categories": categoriesFromDb}


@app.post("/add-category", tags=['categories'])
async def addCategory(request: Request): 
    categoryObj = await request.json()
    dbCategories.insert(categoryObj)
    return {"data": "category added successfully"}


@app.post("/edit-category/{key}", tags=['categories'])
async def editCategory(key, request: Request):
    categoryObj = await request.json() #request.body()
    dbCategories.update(categoryObj, key) #update
    return {"data": "category: " + str(categoryObj['title']) + " edited successfully"} #response


@app.post("/delete-category/{key}", tags=['categories'])
async def deleteSection(key, request: Request):
    dbCategories.delete(key) #delete
    return {"data": "category deleted successfully"} #response



#------ data ------#
@app.get("/data", tags=['data'])
async def data(section=None, category=None):
    if category != None and section != None:
        dataFromDb = dbData.fetch({"section": section, "category": category})
        return {"data": dataFromDb}
    elif section != None:
        dataFromDb = dbData.fetch({"section": section})
        return {"data": dataFromDb}
    else:
        dataFromDb = dbData.fetch()
        return {"data": dataFromDb}


@app.post("/add-data", tags=['data'])
async def addData(request: Request):
    dataObj = await request.json()
    dbData.insert(dataObj) #insert
    return {"data": "data added successfully"}


@app.post("/edit-data/{key}", tags=['data'])
async def editData(key, request: Request):
    dataObj = await request.json() #request.body()
    dbData.update(dataObj, key) #update
    return {"data": "data: " + str(dataObj['category']) + " edited successfully"} #response


@app.post("/delete-data/{key}", tags=['data']) #data delete
async def deleteData(key, request: Request):
    dbData.delete(key) #delete
    return {"data": "data deleted successfully"} #response



#------ users ------#
@app.get("/users", tags=['users']) 
async def users(): 
    usersFromDb = dbUsers.fetch()
    return {"users": usersFromDb}


@app.post("/add-user", tags=['users'])
async def addUser(request: Request):
    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json
    # json.dumps(dataObj) # convert to json
    # print(dataObj)

    #set user obj
    dataObj["createdAt"] = str(datetime.datetime.now())[:-7]
    dataObj["id"] = str(uuid.uuid4()).replace("-", "")
    dataObj["token"] = ""
    dataObj["sections"] = "[]"
    dataObj["categories"] = "[]"
    dataObj["data"] = "[]"
    
    #check total users
    dbUsersObj = dbUsers._fetch() 
    totalUsers = dbUsersObj[1]["paging"]["size"]
    print("Accounts = " + str(totalUsers))
    if(totalUsers > 100): return { "data": "user registration is closed"}

    #check if user exists
    for user in dbUsersObj[1]["items"]:
        if(dataObj["username"] == user["username"]): return { "data": "username is taken"}

    #save user to db
    dbUsers.insert(dataObj); return {"data": "user added successfully"} #response
    

@app.post("/sign-in-user", tags=['users'])
async def signInUser(request: Request):
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

     
# @app.post("/sign-out-user", tags=['users'])
# async def signOutUser(request: Request):
    # print("sign-out-user")
    # return {"status": "logout test"}


@app.post("/specific-user", tags=['users'])
async def specificUser(request: Request):
    print("specific-user")

    dataObj = await request.body()
    dataObj = dataObj.decode()
    dataObj = json.loads(dataObj) # parse json
    # json.dumps(dataObj) # convert to json
    print(dataObj)

    username = dataObj["username"]
    token = dataObj["token"]
    lastLogin = dataObj["lastLogin"]

    test = dbUsers._fetch({"username": username, "token": token, "lastLogin": lastLogin})
    sections = test[1]["items"][0]["sections"]
    categories = test[1]["items"][0]["categories"]
    data = test[1]["items"][0]["data"]
    username = test[1]["items"][0]["username"]
    createdAt = test[1]["items"][0]["createdAt"]
    lastLogin = test[1]["items"][0]["lastLogin"]

    return {
                "status": "fetch specific user successful",
                "username": username, 
                "createdAt": createdAt, 
                "lastLogin": lastLogin, 
                "sections": sections, 
                "categories": categories, 
                "data": data
            }
    