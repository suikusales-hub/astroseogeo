"""
Extract images from idcspy.com article with their paragraph context.
"""
import re, urllib.request, sys

html = urllib.request.urlopen("https://www.idcspy.com/94799.html", timeout=30).read().decode('utf-8', errors='ignore'...[truncated]