from activitystream.models import Post, Comment, Activity, Following, Feed, Upvote

class FeedManager:

    def __init__(self, cur_user):
        self.user = cur_user

    def create_activity(self, actor, verb, post=None, comment=None):
        if verb == 'PST':
            activity = Activity(actor=actor, verb='PST', comment=None, post=post)
            activity.save()
        elif verb == 'CMT':
            activity = Activity(actor=actor, verb='CMT', comment=comment, post=post)
            activity.save()
        elif verb == 'UVT':
            activity = Activity(actor=actor, verb='UVT', comment=None, post=post)
            activity.save()

    def post_to_feed(self, post, fan_out=False):
        feed = Feed(self.user, post)
        feed.save()
        if fan_out:
            followers = Following.objects.filter(target_user=self.user)
            for follower in followers:
                feed_manager = FeedManager(follower)
                feed_manager.post_to_feed(post)

    def create_post(self, content, image=None):
        post = Post(content, self.user, image)
        post.save()
        self.post_to_feed(post, True)
        self.create_activity(actor=self.user, verb='PST', post=post)

    def create_comment(self, content, post):
        comment = Comment(user=self.user, content=content, post=post)
        comment.save()
        self.create_activity(actor=self.user, verb='CMT', post=post, comment=comment)

    def upvote_post(self, post):
        upvote = Upvote(user=self.user, post=post)
        upvote.save()
        self.create_activity(actor=self.user, verb='UVT', post=post)
