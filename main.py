#------ imports ------#
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from deta import Deta
from fastapi.responses import ORJSONResponse
#from fastapi.responses import JSONResponse
#import datetime


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
    sectionsFromDb = next(dbSections.fetch())
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
async def categories(): categoriesFromDb = next(dbCategories.fetch()); return {"categories": categoriesFromDb}

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
        dataFromDb = next(dbData.fetch({"section": section, "category": category}))
        return {"data": dataFromDb}
    elif section != None:
        dataFromDb = next(dbData.fetch({"section": section}))
        return {"data": dataFromDb}
    else:
        dataFromDb =  next(dbData.fetch())
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
async def users(): usersFromDb = next(dbUsers.fetch()); return {"users": usersFromDb}

@app.post("/add-user", tags=['users'])
async def addUser(request: Request):
    dataObj = await request.json()
    dbUsers.insert(dataObj) #insert
    return {"data": "user added successfully"} #response