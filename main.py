import mysql.connector
map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#class that handle all data base schemas and connection
class DBconnection:

    def ConnectToDB(self):
        try:
            connection=mysql.connector.connect(
                host="bpyehzw0tbncbbblslvj-mysql.services.clever-cloud.com",
                user="uzfrys137onqxtxt",
                password="1KnD3S6mCTHw1RZAHL0O",
                database="bpyehzw0tbncbbblslvj")

        except mysql.connector.Error as error:
            print("insert Failed".format(error))
        return connection

    def CheckIdinDB(self,connection,id):
        cursor = connection.cursor()
        sql_select_query = """select * from url where idURL = %s"""
        # set variable in query
        cursor.execute(sql_select_query, (id,))
        # fetch result
        record = cursor.fetchall()
        if len(record)==0:
            return False
        return record

    def SaveIdinDB(self,connection,id,URL):
        cursor = connection.cursor()
        mySql_insert_query = "INSERT INTO url (idURL,LongURL,ShortURL) VALUES (%s,%s, %s)"
        shortURL=Algorithm().idToShortURL(int(id))
        val = (str(id), URL,shortURL)
        cursor.execute(mySql_insert_query, val)
        connection.commit()
        print(cursor.rowcount, "successfully Recorded insert")
        cursor.close()
        return shortURL
#in this class we are handiling the algorithm of converting long URL to short
class Algorithm:
    #function to convert id to short url
    def idToShortURL(self,id):

        shortURL = ""
        if id == 0:
            return "a"
        # for each digit find the base 62
        while (id > 0):
            shortURL += map[id % 62]
            id //= 62
        return shortURL[::-1]
#function to convert url to id
    def URLToId(self,shortURL):
        id = 0
        for i in shortURL:
            val_i = ord(i)
            if (val_i >= ord('a') and val_i <= ord('z')):
                id = id * 62 + val_i - ord('a')
            elif (val_i >= ord('A') and val_i <= ord('Z')):
                id = id * 62 + val_i - ord('A') + 26
            else:
                id = id * 62 + val_i - ord('0') + 52
        return id

    def LongURLToShort(self,URL):
        connection = DBconnection().ConnectToDB()
        id = str(hash(URL))[1:13]
        result = DBconnection().CheckIdinDB(connection, id)
        print(result)
        if result == False:
            shortURL = DBconnection().SaveIdinDB(connection, id,URL)
        else:
            shortURL = result[0][2]
        if connection.is_connected():
            connection.close()
            print("Closed connection in MySQL ")
        return shortURL

Descision=input("To short URL: Click 1\nTo reach for existing URL Click 2\n")
URL=input("Enter your URL: ")
if len(URL)>500:
    print("The URL is length is too long")
    exit(1)
Alg=Algorithm()
DB=DBconnection()
if Descision=='1':
   print("The Short URL is: "+Alg.LongURLToShort(URL))
elif Descision=='2':
    connection = DB.ConnectToDB()
    result = DB.CheckIdinDB(connection, Alg.URLToId(URL))
    if result == False:
        print("Error 404: Page not found")
    else:
        print("You're page is : " + result[0][1])
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")