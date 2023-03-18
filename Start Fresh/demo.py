import sqlite3

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readBlobData(filename):
    try:
        sqliteConnection = sqlite3.connect(r'C:\\Users\\kyath\\OneDrive\\Desktop\\STRATAGEM\\STRATAGEM-HACKATHON-main\\Start Fresh\\instance\\info.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from info where filename = ?"""
        cursor.execute(sql_fetch_blob_query, (filename,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[7])
            filename = row[7]
            photo = row[6]
            # resumeFile = row[3]

            print("Storing employee image and resume on disk \n")
            photoPath = r"C:\\Users\\kyath\\OneDrive\\Desktop\\STRATAGEM\\STRATAGEM-HACKATHON-main\\Start Fresh\\website\\static\\images\\" + filename
            # resumePath = "E:\pynative\Python\photos\db_data\\" + name + "_resume.txt"
            writeTofile(photo, photoPath)
            # writeTofile(resumeFile, resumePath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

# readBlobData(1)
# readBlobData(2)
# readBlobData(3)
