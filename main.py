import tweepy
import os
from dotenv import load_dotenv
from typing import List, Set

USERNAME="peywalt"
OVERFLOW_LIST="misc"

load_dotenv()

def get_user_ids(users : List[tweepy.User]) -> Set[int]:
    return set(map(lambda user: user.id, users))

client = tweepy.Client(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
    bearer_token=os.environ["BEARER_TOKEN"]
)

# i hate python why do i have to manually specify this damn type
list_user : tweepy.User = client.get_user(username=USERNAME).data

following = []
next_token = None
while True:
    next_following = client.get_users_following(
        list_user.id,
        pagination_token=next_token
    )

    follow_list = next_following.data
    following = following + follow_list

    if "next_token" not in next_following.meta:
        break
    next_token = next_following.meta["next_token"]

# not going to paginate over this because i dont have 100 lists
# and am lazy
owned_lists = client.get_owned_lists(list_user.id, user_auth=True).data
overflow_list_id = None
overflow_users = None
for l in owned_lists:
    if l.name == OVERFLOW_LIST:
        overflow_list_id = l.id
        overflow_users = client.get_list_members(l.id, user_auth=True).data

if overflow_list_id == None:
    raise Exception(f"Could not find list named {OVERFLOW_LIST} for user {USERNAME}")

following_ids = get_user_ids(following)
for l in owned_lists:
    list_users = client.get_list_members(l.id, user_auth=True).data
    following_ids = following_ids - get_user_ids(list_users)

# At this point, following_ids should only have user IDs for users who
# I'm following but do not have in any lists

for user_id in following_ids:
    user : tweepy.User = client.get_user(id=user_id).data
    print(f"Adding user {user.username} to list {OVERFLOW_LIST}")
    client.add_list_member(overflow_list_id, user_id)

print(f"Added {len(following_ids)} users to {OVERFLOW_LIST}")

# Now let's remove everyone who we aren't following from overflow

overflow_user_ids = get_user_ids(overflow_users)
ids_to_remove = overflow_user_ids - get_user_ids(following)
for user_id in ids_to_remove:
    user : tweepy.User = client.get_user(id=user_id).data
    print(f"Removing user {user.username} from list {OVERFLOW_LIST}")
    client.remove_list_member(overflow_list_id, user_id)

print(f"Removed {len(ids_to_remove)} users from {OVERFLOW_LIST}")
