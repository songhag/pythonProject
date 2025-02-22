# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Songhao Gao
# songhag@uci.edu
# 42515328

from Profile import Profile, Post
import ds_client


def main():
    profile = Profile()
    profile.load_profile('abc.dsu')

    server = profile.dsuserver
    port = 3001
    username = profile.username
    password = profile.password
    bio = profile.bio
    post = profile._posts
    message = post[0]['entry']
    success = ds_client.send(server, port, username, password, message, bio)

    if success:
        print("Message and bio sent successfully.")
    else:
        print("Failed to send message and bio.")


if __name__ == "__main__":
    main()