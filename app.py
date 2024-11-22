from fastapi import FastAPI
from db_connection import db_config
from models import Data
from pydantic import BaseModel
import random
import string
import uvicorn
from sqlalchemy import select,update,delete
from fastapi.responses import JSONResponse


class URLRequest(BaseModel):
    url: str


def generate_random_string(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


app = FastAPI()

@app.post("/shorten")
def create_url(req:URLRequest):
    try:
        url = req.url
        short_code = generate_random_string()
        create_time =None
        update_time =None
        d_id = None
        with db_config.get_db_session() as session:

            check_data = select(Data).where(Data.url == url)
            check = session.execute(check_data).scalar_one_or_none()

            print(check," +__+__+__+__+")

            if check is not None:
                print("------------URL ALREADY EXISTS---------------------")
                res_data={"msg":"url already exists"}
                return JSONResponse(str(res_data),status_code=400)

            data =Data(url=url,short_url = short_code)
            session.add(data)
            session.flush()
            create_time=data.created_at
            update_time=data.updated_at
            d_id = data.id


            
        res_data = {"id":d_id,
                    "url": url,
                    "short_url": short_code,
                    "created_at":create_time.isoformat() if create_time else None,
                    "updated_at":update_time.isoformat() if update_time else None}
        return JSONResponse(res_data,status_code=200)
    except Exception as e:
        return JSONResponse({"e":str(e)},status_code=400)



@app.get("/shorten/{short_code}")
def retrieve_url(short_code:str):
    try:
        sc = short_code
        with db_config.get_db_session() as session:
            print(sc," ===========================")
            get_data = select(Data).where(Data.short_url == sc)
            data = session.execute(get_data).scalar_one_or_none()

            if data is None:
                print(" -------------------------NO SHORT_URL FOUND-------------------------")
                res_data = {"msg":"no short url found"}
                return JSONResponse(res_data,status_code=400)

            update_q = (
                update(Data)
                .where(Data.short_url == sc)
                .values(count=Data.count + 1)
            )
            session.execute(update_q)
            

            res_data = {"id":data.id,
                        "url":data.url,
                        "short_url":data.short_url,
                        "created_at":data.created_at.isoformat() if data.created_at else None,
                        "updated_at":data.updated_at.isoformat() if data.updated_at else None}

        return JSONResponse(res_data,status_code=200)
    except Exception as e:
        return JSONResponse({"e":str(e)},status_code=400)



@app.put("/shorten/{short_url}")
def update_url(short_url:str,req:URLRequest):
    try:
        url = req.url
        with db_config.get_db_session() as session:
            check_data = select(Data).where(Data.short_url==short_url)
            check = session.execute(check_data).scalar_one_or_none()
            
            if check is None:
                print(" ------------------NO SUCH URL FOR UPDATE ------------------------------")
                return JSONResponse({"msg":"no short url"},status_code=400)
            
            update_query = (update(Data)
                            .where(Data.short_url == short_url)
                            .values(url = url)
                            )
            session.execute(update_query)
            
            res_data = {
                "id":check.id,
                "url":check.url,
                "short_url":check.short_url,
                "created_at":check.created_at.isoformat() if check.created_at else None,
                "updated_at":check.updated_at.isoformat() if check.updated_at else None
            }
        
        return JSONResponse(res_data,status_code=200)
    except Exception as e:
        return JSONResponse({"e":str(e)},status_code=400)
    


    


if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=5000)
    
        
