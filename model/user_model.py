import mysql.connector 
from flask import  jsonify
import jwt
from datetime import datetime , timedelta
from dotenv import load_dotenv
import os

load_dotenv()

db_password = os.getenv('FLASK_DB_PASSWORD')

class user_model():

    #constructor for connection establishment with SQL Workbench
    def __init__(self):
        try:
            self.con= mysql.connector.connect(host="localhost" ,username="root" , password=db_password ,database="crud_db" )
            self.cur= self.con.cursor(dictionary=True) # ensures that the data we recieve is in form of a dictionary 
            print("Connection Successful")
        except:
            print("Connection failed")

    def user_getall(self):
        self.cur.execute("SELECT * FROM users")
        res = self.cur.fetchall()
        if len(res) > 0 :
            return jsonify({"data" : res}) , 200
        else :
            return jsonify({"message" : "No data found"}) , 400
    
    def user_get(self , limit , page):
        limit = int(limit)
        page = int(page)
        start = (page * limit ) - limit 
        self.cur.execute(f"SELECT * FROM users LIMIT {start} , {limit}")
        res = self.cur.fetchall()
        if len(res) > 0 :
            return jsonify({"data" : res , "Page No.":page }) , 200
        else :
            return jsonify({"message" : "No data found"}) , 400
    
    def user_add(self , data):
        try:
            query = "INSERT INTO users (name, password, gmail) VALUES (%s, %s, %s)"
            values = (data['name'], data['password'], data['gmail'])
            self.cur.execute(query, values)
            self.con.commit()
            return  jsonify({"message" : "Data added successfully"}) ,201
        except:
            return  jsonify({"message" : "OOPS Request failed" }) , 404
        
    def user_delete(self , id):
        try:
            query = "DELETE FROM users WHERE id = %s"
            values = (id,)
            self.cur.execute(query, values)
            self.con.commit()
            return jsonify({"message" : "User deleted successfully"}) , 200
        except:
            return  jsonify({"message" : "OOPS Request failed" }) , 400
        

    def user_edit(self ,id , data):
        try:
            query = f"UPDATE  users  SET"  
            for i in data:
                query += " " + f"{i} = '{data[i]}'" + ","
            query = query[:-1]
            query += " " + f"where id={id}"
            self.cur.execute(query)
            self.con.commit()
            return  jsonify({"message" : "Data added successfully" }) ,201
        except:
            return  jsonify({"message" : "OOPS Request failed" }) , 404
        
    def file_upload(self , filepath , uid):
        try:
            query = "UPDATE users SET avatar=%s WHERE id=%s"
            self.cur.execute(query, (filepath, uid))
            self.con.commit()
            return jsonify({"message": "File uploaded successfully"}), 201
        except Exception as e:
            print(f"Error occurred: {e}")  
            return jsonify({"message": "OOPS Request failed"}), 404
        
    def login(self, data):
        try:
            # Use parameterized query to prevent SQL injection
            query = "SELECT id, name, role_id, password, gmail FROM users WHERE gmail = %s"
            self.cur.execute(query, (data["gmail"],))
            result = self.cur.fetchone()

            if result:
                user_id, name, role_id, password, gmail = result
                
                # Validate the password (assuming data["password"] is plaintext)
                if password == data["password"]:  # You should hash passwords and check the hash instead!
            
                    # Token expiration time
                    exp_time = datetime.now() + timedelta(minutes=15)
                    exp_epoch_time = int(exp_time.timestamp())
                    
                    # Payload for JWT (excluding sensitive information like password)
                    payload = {
                        "user_id": user_id,
                        "name": name,
                        "role_id": role_id,
                        "exp": exp_epoch_time
                    }
                    
                    # Generate JWT token
                    token = jwt.encode(payload, "SecretEncryptionKey", algorithm="HS256")
                    
                    return jsonify({"token": token}), 200
                else:
                    return jsonify({"message": "Invalid password"}), 401
            else:
                return jsonify({"message": "User not found"}), 404
        
        except Exception as e:
            print(f"Error occurred: {e}")  
            return jsonify({"message": "OOPS Request failed"}), 500
    