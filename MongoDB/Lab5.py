from pymongo import MongoClient
from datetime import datetime

#Step1: Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
client.drop_database('facebookData')
db = client['facebookData'] #choose database tiktok

#Step2: Create collections
users_collection = db['users']
posts_collection = db['posts']
comments_collection = db['comments']

#Step3: add user data
user_data = [
    { 'user_id': 1, 'name': "Nguyen Van A", 'email': "a@gmail.com", 'age': 25 },
    { 'user_id': 2, 'name': "Tran Thi B", 'email': "b@gmail.com", 'age': 30 },
    { 'user_id': 3, 'name': "Le Van C", 'email': "c@gmail.com", 'age': 22 }
]
users_collection.insert_many(user_data)

#Step4: add posts data
posts_data = [
    { 'post_id': 1, 'user_id': 1, 'content': "Hôm nay thật đẹp trời!", 'created_at': 'datetime("2024-10-01")' },
    { 'post_id': 2, 'user_id': 2, 'content': "Mình vừa xem một bộ phim hay!", 'created_at': 'datetime("2024-10-02")' },
    { 'post_id': 3, 'user_id': 1, 'content': "Chúc mọi người một ngày tốt lành!", 'created_at': 'datetime("2024-10-03")' }
]
posts_collection.insert_many(posts_data)

#step5: add comments data
comments_data = [
    { 'comment_id': 1, 'post_id': 1, 'user_id': 2, 'content': "Thật tuyệt vời!", 'created_at': 'datetime("2024-10-01")' },
    { 'comment_id': 2, 'post_id': 2, 'user_id': 3, 'content': "Mình cũng muốn xem bộ phim này!", 'created_at': 'datetime("2024-10-02")' },
    { 'comment_id': 3, 'post_id': 3, 'user_id': 1, 'content': "Cảm ơn bạn!", 'created_at': 'datetime("2024-10-03")' }
]
comments_collection.insert_many(comments_data)

#step6: truy van data
#6.1. See all users
print("All users:")
for user in users_collection.find():
    print(user)

#6.2. See all posts of user has user_id=1
print("\nTat ca cac post cua user1:")
user_posts = posts_collection.find({'user_id': 1})
for post in user_posts:
    print(post)

#6.3. See all comments of post which has post_id = 1
print("\nTat ca comment cua bai dang co post_id=1:")
post_comments = comments_collection.find({'post_id': 1})
for comment in post_comments:
    print(comment)

#6.4. truy van user has ages over 25
print("\nUser co do tuoi tren 25:")
user_ages = users_collection.find({'age': {'$gt':25}})
for age in user_ages:
    print(age)

#6.5 truy van all posts được tạo trong tháng 10
print("\nPost được tạo trong tháng 10:")
posts_created = posts_collection.find({'created_at': {'$gte': 'datetime("2024-10-01")', '$lt': 'datetime("2024-11-01")'}})
for posts in posts_created:
    print(posts)

#step7: update and delete data
#7.1. Update noi dung bai dang cua nguoi dung voi post_id = 1
posts_collection.update_one({'post_id': 1}, {'$set': {'content': "Hôm nay thời tiết thật đẹp!"}})

#7.2. Delete comment w/ comment_id = 2
comments_collection.delete_one({'comment_id': 2})

#7.3. xem lại dữ liệu sau khi update và delete
print("\nDu lieu bai dang sau khi cap nhat:")
for post in posts_collection.find():
    print(post)
print("\nDu lieu comment sau khi xoa:")
for comment in comments_collection.find():
    print(comment)

#dong ket noi
client.close()