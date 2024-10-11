# Django Middlewares

Some powerful middleware in Django

## DDOS Defender

It's just a simple ddos guard.

If you want to use this :

- first fill up some settings in `settings.py`
- change `MAX_LIMIT_REQUEST` value as you please.

Now you can just execute `runserver` command:

- Linux/Mac

    python3 manage.py runserver

- Windows

    python manage.py runserver

### Cache framework

You can add your cache framework in the `settings.py` to better controling
over caching requests.
I'v added mine but, I make them comment, because the `cache_backends.py` file
does not configured.
You can configure the `cache_backends.py` as you please.

### Session

I will add details about session staff that if any request does not get a session,
It's probably comes from a malicious origin, so that request should be classified as
a suspicious request.

## Multi Vector Defense System

Now we have the **`Multi Vector Defense System`** feature.

First we will setup **ids**, **ips** & **firewall** and than we will try to find the possible threat
that comes to our server and web app.

I assuming that you have **`Debian`** base linux but hey, for other distro, it should work well.

## Logger

This middleware can log :

- **Requested url**
- **Query if it is existed**
- **Session if it is existed**

Of course I need to optimize the logging time but for now, It works as expected!

## Shell Defender

The most dangerous attack that Django struggles with it, is the shell attack.
Shells always attach to a picture and the intruder upload it as his profile pic, and than he tries to activate it with
some remote access tools. Shells may have some dangerous script like **`SQL Query`** or any other **Python`** scripts.

But, There are one thing in common: 

- **When they attach, they work with that extension**

so we can change the extension of the corrupted file before it gets uploaded.

## Web3 Cookies

I'v designed these two middlewares for you, give them a try and send me your feedback.

### Web3CookieMiddleware

- **Purpose**: This middleware handles the retrieval, validation, and setting of a Web3 cookie in Django requests and responses.

### RoleBasedAccessControlMiddleware

- **Purpose**: This middleware manages role-based access control by extracting roles from the Web3 cookie and attaching them to the request object.
