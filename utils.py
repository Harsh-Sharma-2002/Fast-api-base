def find_post(id: int, my_posts: list):
    post = None
    for p in my_posts:
        if p['id'] == id:
            post = p
            break
    return post