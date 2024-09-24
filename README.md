# Django Middlewares

Some powerful middleware in Django

## DDOS Defender

It's just a simple ddos guard.

If you want to use this :

- first fill up some settings in `settings.py`
- change `MAX_LIMIT_REQUEST` value as you please.

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

## Shell Defender
