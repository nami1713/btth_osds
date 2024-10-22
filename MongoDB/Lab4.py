from pymongo import MongoClient
from datetime import datetime

#Step1: Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
client.drop_database('tiktokABC')
db = client['tiktokABC'] #choose database tiktok

#Step2: Create collections
users_collection = db['users']
videos_collection = db['video']

#Step3: Add users data
users_data = [
    {'user_id': 1, 'username': "user1", 'full_name': "Nguyen Van A", 'followers': 1500, 'following': 200},
    {'user_id': 2, 'username': "user2", 'full_name': "Tran Thi B", 'followers': 2000, 'following': 300},
    {'user_id': 3, 'username': "user3", 'full_name': "Le Van C", 'followers': 500, 'following': 100}
]
users_collection.insert_many(users_data)

#Step4: Add videos data
videos_data = [
    { 'video_id': 1, 'user_id': 1, 'title': "Video 1", 'views': 10000, 'likes': 500, 'created_at': datetime(2024,1,1) },
    { 'video_id': 2, 'user_id': 2, 'title': "Video 2", 'views': 20000, 'likes': 1500, 'created_at': datetime(2024,1,5) },
    { 'video_id': 3, 'user_id': 3, 'title': "Video 3", 'views': 5000, 'likes': 200, 'created_at': datetime(2024,1,10) }
]
videos_collection.insert_many(videos_data)

#Step5: truy van data
#5.1. Xem all users
print("All users:")
for user in users_collection.find():
    print(user)

#5.2. Tim video co nhieu nguoi xem nhat
print("Video co nhieu luot xem nhat:")
most_viewed_video = videos_collection.find().sort('views', -1).limit(1)
for user in most_viewed_video:
    print(user)

#5.3. Tim all video of user whose username 'user1'
print('\nTat ca video cua nguoi dung "user1":')
user_videos = videos_collection.find({'user_id': 1})
for video in user_videos:
    print(video)

#Step6: Update data
#cap nhat so nguoi theo doi cua nguoi dung voi user_id la 1 len 2000
users_collection.update_one({'user_id': 1}, {'$set': {'followers': 2000}})

#Step7: xoa video co video_id la 3
videos_collection.delete_one({'video_id': 3})

#step8: xem lai data sau khi cap nhat va xoa
print("\nDu lieu nguoi dung sau khi cap nhat:")
for user in users_collection.find():
    print(user)
print("\nDu lieu video sau khi xoa:")
for video in videos_collection.find():
    print(video)

#dong ket noi
client.close()