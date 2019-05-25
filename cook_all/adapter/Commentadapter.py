from cook_all.bean.comment import Comment
from cook_all.dao.Chef import Chef


def getallcomment(dishid, chef_id):
    comments = []
    print(chef_id)
    print(dishid)
    for comment in Chef.get_dish_comment_from_chef_id(int(chef_id)):
        print(comment)
        if comment['dish_id'] == int(dishid):
            dish_bean = Comment(comment['comment_rank'],
                                comment['comment_detail'])
            comments.append(dish_bean)
    return comments
