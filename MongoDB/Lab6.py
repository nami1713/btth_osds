from pymongo import MongoClient
from datetime import datetime

#Step1: Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
client.drop_database('driveManagement')
db = client['driveManagement'] #choose database

#Step2: Create collection
files_collection = db['files']

#Step3: Add files data
files_data = [
    {'file_id': 1, 'name': "Report.pdf", 'size': 2048, 'owner': "Nguyen Van A", 'created_at': 'datetime("2024-01-10")', 'shared': 'false'},
    {'file_id': 2, 'name': "Presentation.pptx", 'size': 5120, 'owner': "Tran Thi B", 'created_at': 'datetime("2024-01-15")', 'shared': 'true'},
    {'file_id': 3, 'name': "Image.png", 'size': 1024, 'owner': "Le Van C", 'created_at': 'datetime("2024-01-20")', 'shared': 'false'},
    {'file_id': 4, 'name': "Spreadsheet.xlsx", 'size': 3072, 'owner': "Pham Van D", 'created_at': 'datetime("2024-01-25")', 'shared': 'true'},
    {'file_id': 5, 'name': "Notes.txt", 'size': 512, 'owner': "Nguyen Thi E", 'created_at': 'datetime("2024-01-30")', 'shared': 'false'}
]
files_collection.insert_many(files_data)

#Step4: thuc hien truy van de quan ly tep
#4.1. See all files in collection 'files'
print('Tat ca file:')
for file in files_collection.find():
    print(file)

#4.2. Tim tep co size lon hon 2000KB
print('\nCac file co kich thuoc lon hon 2000KB la:')
file_size = files_collection.find({'size': {'$gt':2000}})
for size in file_size:
    print(size)

#4.3. Count tong so file
print('\nTong so file:')
count_file = files_collection.count_documents({})
print(count_file)

#4.4. Find all files have been shared
print('\nTat ca file duoc chia se:')
share_file = files_collection.find({'shared': 'true'})
for share in share_file:
    print(share)

#4.5. Thong ke so luong file theo chu so huu
print('\nSo luong file theo chu so huu:')
owner_file = files_collection.aggregate([{'$group': {'_id': '$owner', 'count':{'$sum': 1}}}])
for owner in owner_file:
    print(owner)

#4.6. Tim tat ca tep cua user co ten "Nguyen Van A"
print('\nTat ca cac file cua user "Nguyen Van A" la:')
all_file = files_collection.find({'owner': 'Nguyen Van A'})
for files in all_file:
    print(files)

#4.7. Tim tep lon nhat trong bo suu tap
print('\nFile lon nhat trong bo suu tap la:')
largest_file = files_collection.find().sort({'size': -1}).limit(1)
for largest in largest_file:
    print(largest)

#4.8. Tim so luong file co kich thuoc nho hon 1000KB
print('\nSo luong tep co kich thuoc nho hon 1000KB la:')
smaller_file = files_collection.count_documents({'size': {'$lt': 1000}})
print(smaller_file)

#4.9. Tim tat ca file duoc tao trong thang 1 nam 2024
print('\nCac file duoc tao trong thang 1 nam 2024 la:')
created_file = files_collection.find({'created_at': {'$gte': 'datetime("2024-01-01")', '$lt': 'datetime("2024-02-01")'}})
for create in created_file:
    print(create)

#4.11. Delete tat ca file co kich thuoc nho hon 1000KB

#Step5: Update and delete file data
#5.1. Update trang thai chia se cua file voi file_id = 1 thanh True
files_collection.update_one({'file_id': 1}, {'$set': {'shared': 'true'}})

#5.2. Update ten file voi 'file_id' tu 4 thanh 'New Spreadsheet.xlsx'
files_collection.update_one({'file_id': 4}, {'$set': {'name': 'New Spreadsheet.xlsx'}})

#5.3. Delete file w/ file_id = 3
print('\n')
files_collection.delete_one({'file_id': 3})

#5.4. Delete tat ca file co kich thuoc nho hon 1000KB
files_collection.delete_many({'size': {'$lt': 1000}})

#Step6: Check data sau khi update va delete
#check all file in collection
for file in files_collection.find():
    print(file)
#Dong ket noi
client.close()