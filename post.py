import re
from datetime import datetime

def postInterface(db, user):
    username = db.users.find_one({"_id": user}, {"name": 1, "_id": 0})['name']
    try:
        print("=" * 25, "Post", "=" * 25)
        print("\n1. insertPost\n"
              "2. deletePost\n"
              "3. go back")
        a = int(input("Choose one: "))

        if a == 1:
            insertPost(db, user, username)
        elif a == 2:
            deletePost(db, user)
        elif a == 3:
            print("\n\n")
            pass
        else:
            print("Invalid input")
    except ValueError:
        print('Invalid input!')


def insertPost(db, user, username):
    try:
        title = input("please write title : ")
        text = input("please write text : ")
        hashtag = input("Please input words with '#' to tag: ")
        p = re.compile(r"#\w+")
        res = p.findall(hashtag)
        tags = list(map(lambda x: x[1:], res))
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pt=list(db.posts.find({},{"_id":1}))

        if pt==[]:
            number = 0
        else:
            number = pt[-1]['_id']  
        db.posts.insert_one({"_id":number+1,"Title":title,"Text":text,"Date":date,"Writerid":user,"Writername":username,"comment":[],"tags": tags})




        print("------[successfully inserted]------")
        postInterface(db, user)
    except ValueError:
        print('[inserpost]Error')



def deletePost(db, user):
    user_posts = list(db.posts.find({"Writerid":user},{"Title":1}))

    a_list = []
    print("---[Posts list]---\n"
          "post num")
    for i in user_posts:
        a_list.append(i['_id'])
        print("   ",i['_id'],"   : ",i['Title'])
    try:

        if user_posts:
            b = int(input("Please input post number to delete:"))
            if b in a_list:
                c = input("Are you sure?(y/n):")
                if c in ['y','Y']:
                    db.posts.delete_one({"_id":b})
                    print("Successfully deleted")
                    postInterface(db, user)
                elif c in ['n','N']:
                    deletePost(db, user)
                else:
                    print("Wrong input!")
            else:
                print("The post num is not exist!")
                deletePost(db, user)

        else:
            print("There's no post.")
    except ValueError:
        print("Error!")





def findTag(db, user):
    try:
        tag = input("Input word to search: ")
        if not tag:
            return
        else:
            res = list(db.posts.find({'tags':{"$elemMatch":{'$eq': tag}}}))
            if not res:
                print("no result!")
                findTag(db, user)
            else:
                for idx in range(len(res)):
                    mywall = res[idx]
                    print()
                    print("[" + str(idx + 1) + "]", '\n')
                    print("Post_num : ", mywall["_id"], '\n',
                          "Date : ", mywall["Date"], '\n',
                          "WriterID : ", mywall["Writerid"], '\n',
                          "WriterName : ", mywall["Writername"], '\n',
                          "Title : ", mywall["Title"], '\n',
                          "Text : ", mywall["Text"], '\n',
                          "tags : ", mywall["tags"], '\n',
                          "Comment : ", mywall["comment"], '\n')
                    print("=" * 50)
                    input("If you want to go back, press enter key.")
                    findTag(db, user)
    except ValueError:
        print("Error!")