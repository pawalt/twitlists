# Twitlists

A while ago, Twitter changed their timeline to be algorithmically-fed rather than a simple reverse-chronological feed. In particular, they push a lot of content on me from people I don't follow, which I really don't like.

You can fix this by using Twitter Lists. Lists are exactly reverse-chronological, and they only show content from people you follow. The problem, though, is that following someone no longer corresponds to adding them to your feed. You have to explicitly add them to one of your lists which is much more work than hitting the follow button.

To fix this, I wrote a script that takes your username along with an "overflow list". It then takes all your following, set subtracts all your list members from it, and sees what's left over. If there are any users that you follow but aren't in your lists, it adds them to your overflow list. This overflow list effectively becomes your "following list".

To keep things in sync, I've set up a Github Action on a cron schedule to run once an hour. I think this is actually against Actions TOS so please don't tell GitHub :P

### Unfinished Work

I need to make it so that if I unfollow someone they get removed from my lists as well. Should this removal only happen for the overflow list or for all of them?
