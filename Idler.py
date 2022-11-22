from PIL import Image
import imaplib2, time
import email
import os
from threading import *
 
# This is the threading object that does all the waiting on 
# the event
class Idler(object):
    def __init__(self, conn):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()
 
    def start(self):
        self.thread.start()
 
    def stop(self):
        # This is a neat trick to make thread end. Took me a 
        # while to figure that one out!
        self.event.set()
 
    def join(self):
        self.thread.join()
 
    def idle(self):
        # Starting an unending loop here
        while True:
            # This is part of the trick to make the loop stop 
            # when the stop() command is given
            if self.event.isSet():
                return
            self.needsync = False
            # A callback method that gets called when a new 
            # email arrives. Very basic, but that's good.
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            # Do the actual idle call. This returns immediately, 
            # since it's asynchronous.
            self.M.idle(callback=callback)
            # This waits until the event is set. The event is 
            # set by the callback, when the server 'answers' 
            # the idle call and the callback function gets 
            # called.
            self.event.wait()
            # Because the function sets the needsync variable,
            # this helps escape the loop without doing 
            # anything if the stop() is called. Kinda neat 
            # solution.
            if self.needsync:
                self.event.clear()
                self.dosync()
 
    # The method that gets called when a new email arrives. 
    # Replace it with something better.
    def dosync(self):
        retcode, messages = self.M.search(None, '(UNSEEN)')
        if retcode == 'OK':
            for num in messages[0].split():
                typ, data = self.M.fetch(num,'(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        typ, data = self.M.store(num, '+FLAGS', '\\Seen')
                        self.save_attachment(msg)

    def save_attachment(self, msg, download_folder="static/images/"):
        """
        Given a message, save its attachments to the specified
        download folder, default is static/images/

        return: file path to attachment
        """
        att_path = "No attachment found."
        print(msg['Subject'])
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            att_path = os.path.join(download_folder, filename)
            # copy file to disk
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            # check if file is a valid image
            img = Image.open(att_path)
            if img.format != 'JPEG' and img.format != 'PNG':
                continue
            thumb_path = os.path.join("static/thumbs/", filename)
            img.thumbnail((90, 90) )
            img.save(thumb_path, exif=img.info['exif'])
        return att_path
