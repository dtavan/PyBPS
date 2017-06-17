"""
Miscellaneous utility functions
"""

# Common imports
import os
import sys
import re
import csv
import string
import random
import smtplib
import zipfile
from subprocess import check_call, STDOUT
from tempfile import NamedTemporaryFile
from shutil import rmtree
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

# Handle Python 2/3 compatibility
from six.moves import email_mime_base
MIMEBase = email_mime_base.MIMEBase


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def random_str(n):
    """Generates a random string of length n containing upper and lowercase
    letters and numbers"""
    return "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(n))


def tmp_dir(action, tmp_dir):
    """Create/remove temporary folder.

    Creates or removes a temporary folder at the indicated path.

    Args:
        action: either 'create' or 'remove' temporary folder.
        tmp_dir: absolute path to temporary folder to be created/removed.

    Returns:
        nothing

    Raises:
        IOError: Exception:
    """

    # Create temporary folder
    if action == 'create':
        if not os.path.exists(tmp_dir):
            try:
                os.mkdir(tmp_dir)
            except:
                print("Exception: ", str(sys.exc_info()))
    # Remove temporary folder
    elif action == 'remove':
        if os.path.exists(tmp_dir):
            try:
                rmtree(tmp_dir)
            except:
                print("Exception: ", str(sys.exc_info()))


def get_file_paths(pattern_list, dir):
    """Get paths to files with name following specified pattern.

    Args:
        pattern_list: list of search patterns (each pattern as string).
        dir: absolute path to directory to search for files.

    Returns:
        list of paths to files containing specified pattern.
    """

    paths_list = []

    for root, dirs, files in os.walk(dir):
        for name in files:
            for pattern in pattern_list:
                match = re.search(r'.*' + pattern.strip() + r'.*', name)
                if match:
                    paths_list.append(os.path.join(root, name))

    return paths_list


def dict_cleanconvert(dict):
    """Clean and convert dict keys and values.

    Strips whitespaces from dict keys and values, convert string identified as
    numbers to float and removes empty dict keys and values.

    Args:
        dict: dict to cleaned.

    Returns:
        Cleaned dict.
    """

    # Remove unwanted whitespaces in dict keys / values and remove empty keys
    dict = {k.strip(): v.strip() for k, v in dict.items() if k}

	# Convert all strings identified as numbers to float type
    for key in dict.keys():
        if is_float(dict[key]):
            dict[key] = round(float(dict[key]), 3)

    return dict


def run_cmd(cmd, debug=False):
    """Run a shell command.

    Args:
        cmd: shell command in list format.

    Raises:
        Problem executing: cmd
    """

    try:
        if debug == False:
            with NamedTemporaryFile() as f:
                check_call(cmd, stdout=f, stderr=STDOUT)
                #f.seek(0)
                #output = f.read()
        else:
            check_call(cmd)
    except OSError:
        sys.stderr.write('Problem executing: ' + ' '.join(cmd))


def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            if filename.endswith('csv') or filename.endswith('db'):
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                print('zipping {} as {}'.format(os.path.join(dirname, filename), arcname))
                zf.write(absname, arcname)
    zf.close()


def sendgmail(from_addr, to_addr_list, subject, message,
              login, password, att_file=None, smtpserver='smtp.gmail.com:587'):

    # Build message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ','.join(to_addr_list)
    msg.attach( MIMEText(message) )

    # Attach file
    if att_file is not None:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(att_file, 'rb').read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(att_file))
        msg.attach(part)

    # Send email
    server = smtplib.SMTP(smtpserver)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login,password)
    try:
        server.sendmail(from_addr, to_addr_list, msg.as_string())
        print ('email sent')
    except:
        print ('error sending mail')
    server.quit()
