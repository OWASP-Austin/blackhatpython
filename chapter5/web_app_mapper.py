import Queue
import threading
import os
import urllib2

'''
Using joomla requires you to run a web server etc.
you can just crawl a site you're allowed access to.
if you really feel the need though here's the dl:
    it's for the file structure, to build paths to hit remote.
    otherwise if you touch a file in your dest directory, it'll return 200 for it. 
https://downloads.joomla.org/cms/joomla3/3-1-1
'''

threads = 10
# target = "http://www.nostarch.com"
target = "http://www.google.com"
directory = "/root/Documents/mapping_web_app_blackhatpy_ch5"
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)

# store files we attempt to locate
web_paths = Queue.Queue()

for r, d, f in os.walk("."):
    for files in f:
        remote_path = "%s/%s" % (r, files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

        request = urllib2.Request(url)

        try:
            print("Inside yer try @Test_remote")
            response = urllib2.urlopen(request)
            content = response.read()

            print "[%d] => %s" % (response.code, path)
            response.close()

        except urllib2.HTTPError as error:
            # print "Failed %s" % error.code
            pass

for i in range(threads):
    print "Spawning thread: %d" % i
    t = threading.Thread(target=test_remote())  # add parens to invoke
    t.start()
