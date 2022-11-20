import imaplib2, time
import os
from Idler import Idler
from dotenv import load_dotenv

load_dotenv()
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
    # exit after 5 minutes.
    time.sleep(5*60)
finally:
    # Clean up.
    idler.stop()
    idler.join()
    M.close()
    # This is important!
    M.logout()
