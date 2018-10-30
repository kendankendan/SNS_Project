from pprint import pprint

def newsfeed(db,user):
    fol = db.users.find_one({"_id":user},{"_id":0,"followings":1})['followings']
    fol.append(user)
    print("-"*30,"[Newsfeed]","-"*30)
    cnt = db.posts.find({"Writerid":{'$in':fol}}).count()
    page = cnt//5
    p = 0
    while (p<=page):
        try:
            walls = list(db.posts.find({"Writerid": {'$in':fol}}).sort([("_id",-1)]).skip(p*5).limit(5))
            for mywall in walls:
                print("Post_num : ", mywall["_id"], '\n',
                      "Date : ", mywall["Date"], '\n',
                      "WriterID : ", mywall["Writerid"], '\n',
                      "WriterName : ", mywall["Writername"], '\n',
                      "Title : ", mywall["Title"], '\n',
                      "Text : ", mywall["Text"], '\n',
                      "tags : ", mywall["tags"], '\n',
                      "Comment : ", mywall["comment"], '\n')
                print("=" * 50)
            if p==0:
                print("This is the first page")
            if p == page:
                print("This is the last page")    
            
            if p == page:
                np = input("previous page(a), next page(b), exit(c), insertcomment(i),deletecomment(d):")
                if np in ['a','A']:
                    if p == 0:
                        pass
                    else:
                        p -= 1
                elif np in ['c','C']:
                    return False
                elif np in ['i','I']:
                    textnum = int(input("Input post number to comment:"))
                    insertcomment(db,user,textnum)
                elif np in ['d','D']:
                    textnum = int(input("Input post number to delete comment:"))
                    deletecomment(db,user,textnum)
                else:
                    pass
            else:
                np = input("previous page(a), next page(b), exit(c), insertcomment(i),deletecomment(d):")
                if np in ['a','A']:
                    if p == 0:
                        pass
                    else:
                        p -= 1
                elif np in ['b','B']:
                    p += 1
                elif np in ['c','C']:
                    p = page+1
                elif np in ['i','I']:
                    textnum = int(input("Input post number to comment:"))
                    insertcomment(db,user,textnum)
                elif np in ['d','D']:
                    textnum = int(input("Input post number to delete:"))
                    deletecomment(db,user,textnum)
                else:
                    pass
        except:
            print("Error!")


def insertcomment(db,user,textnum):
    try:
        if not db.posts.find({"_id":textnum}):
            raise NameError
        else:
            pass
        comm = input("Enter your comment:")
        db.posts.update_one({"_id":textnum},{'$push':{'comment':{'commentor':user,'text':comm}}})
    except NameError:
        print("The post is not exist!")
    except:
        print("Error!")

def deletecomment(db,user,textnum):
    try:
        if not db.posts.find({"_id":textnum}):
            raise NameError
        else:
            pass
        pprint(db.posts.find_one({"_id":textnum}))
        tex = input("Input comment to delete:")
        db.posts.update_one({"_id":textnum},{'$pull':{'comment':{'commentor':user,'text':tex}}})
    except NameError:
        print("The post is not exist!")
    except :
        print("Error!")

        
def getPosts(db,user):
    print("-"*30,"[My wall]","-"*30)
    cnt = db.posts.find({"Writerid":user}).count()
    page = cnt//5
    p = 0
    while (p<=page):
        try:
            walls = list(db.posts.find({"Writerid": user}).hint([('Writerid', 1), ('_id', -1)]).skip(p*5).limit(5))
            for mywall in walls:
                print("Post_num : ", mywall["_id"], '\n',
                      "Date : ", mywall["Date"], '\n',
                      "WriterID : ", mywall["Writerid"], '\n',
                      "WriterName : ", mywall["Writername"], '\n',
                      "Title : ", mywall["Title"], '\n',
                      "Text : ", mywall["Text"], '\n',
                      "tags : ", mywall["tags"], '\n',
                      "Comment : ", mywall["comment"], '\n')
                print("=" * 50)
            if p==0:
                print("This is the first page")
            if p == page:
                print("This is the last page")  
            if p == page:
                np = input("previous page(a), exit(c), insertcomment(i),deletecomment(d):")
                if np in ['a','A']:
                    if p == 0:
                        pass
                    else:
                        p -= 1
                elif np in ['c','c']:
                    return False
                elif np in ['i','I']:
                    textnum = int(input("Input post number to comment:"))
                    insertcomment(db,user,textnum)
                elif np in ['d','D']:
                    textnum = int(input("Input post number to delete:"))
                    deletecomment(db,user,textnum)
                else:
                    return False
            else:
                np = input("previous page(a), next page(b), exit(c), insertcomment(i),deletecomment(d):")
                if np in ['a','A']:
                    if p == 0:
                        pass
                    else:
                        p -= 1
                elif np in ['b','B']:
                    p += 1
                elif np in ['c','C']:
                    p = page+1
                elif np in ['i','I']:
                    textnum = int(input("Input post number to comment:"))
                    insertcomment(db,user,textnum)
                elif np in ['d','D']:
                    textnum = int(input("Input post number to delete:"))
                    deletecomment(db,user,textnum)
                else:
                    pass
        except:
            print("Error!")
