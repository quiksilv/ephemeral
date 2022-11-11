import imaplib2, time
import os
from Idler import Idler
from dotenv import load_dotenv

load_dotenv()
# Had to do this stuff in a try-finally, since some testing 
# went a little wrong.....
try:
    # Set the following two lines to your creds and server
    M = imaplib2.IMAP4_SSL(os.getenv("SERVER") )
    M.login(os.getenv("EMAIL"), os.getenv("PASSWORD") )
    # We need to get out of the AUTH state, so we just select 
    # the INBOX.
    M.select("INBOX")
    # Start the Idler thread
    idler = Idler(M)
    idler.start()
    # Because this is just an example, exit after 1 minute.
    time.sleep(1*60)
finally:
    # Clean up.
    idler.stop()
    idler.join()
    M.close()
    # This is important!
    M.logout()
