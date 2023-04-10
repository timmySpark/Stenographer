import os
from django.core.files.storage import FileSystemStorage
from stegano import lsb
import time
import requests
import random
import string

REGULAR_UPLOAD_PATH = 'media/r_uploads'
ENCRYPTED_UPLOAD_PATH = 'media/encryptedImages'

def remove_old_files():
    folders =[REGULAR_UPLOAD_PATH, ENCRYPTED_UPLOAD_PATH]
    M = 2
    current_time = time.time()
    minute_in_sec = M*60
    # os.chdir(os.path.join(os.getcwd(), folder))
    for image_path in folders:
        list_of_files = os.listdir(image_path)
        if list_of_files != []:
            for i in list_of_files:
                file_location = os.path.join(image_path, i)
                file_time = os.stat(file_location).st_mtime

                # if a file is modified before M minute then delete it
                if(file_time < current_time - minute_in_sec):
                    print(f" Delete : {i}")
                    os.remove(file_location)

# remove_old_files(folder_path=REGULAR_UPLOAD_PATH)


class SaveImage:
    def __init__(self, img, is_link=False, encode=True):
        self.error = []
        self.img_name = None
        self.is_saved = False
        self.img_path = None
        self.save(img, is_link, encode)
        remove_old_files()

        
    def save(self, unsaved_img, is_link, encode):
        characters = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(5))

        if encode:
            image_name = str(unsaved_img).split('.')[0]
            if is_link:
                cv_Imgname = f"url-steganographer_{characters}.png"
            else:
                cv_Imgname = f"{str(image_name)}-steganographer{characters}.png"

        else:
            cv_Imgname = f"steganograph_decode{characters}.png"

        if is_link:
            try:
                img_data = requests.get(unsaved_img).content
                
            except:
                error = 'There was an error in fetching the image; Try using a different Image Url'
                self.error.append(error)
                return False

            else:
                with open(f'{REGULAR_UPLOAD_PATH}/{cv_Imgname}', 'wb') as handler:
                    handler.write(img_data)
                    self.img_name = cv_Imgname
                    self.img_path = f'{REGULAR_UPLOAD_PATH}/{cv_Imgname}'
                    self.is_saved = True


        else:
            upload = unsaved_img
            fss = FileSystemStorage()
            file = fss.save(f'r_uploads/{cv_Imgname}', upload)
            self.img_name = cv_Imgname
            self.img_path = f'{REGULAR_UPLOAD_PATH}/{cv_Imgname}'
            self.is_saved = True
        
        # Deleting image after 30 mins

    # def delete(self, img):
    #     if os.path.exists(f'uploads/{img}'):
    #         next_1min = datetime.now() + timedelta(minutes=1)
    #         print(img)
    #     if datetime.now() > next_1min:
    #         os.remove(f'uploads/{self.img}')


def encrypt_image(img_path, msg, img_name):
    try:
        secret = lsb.hide(img_path, msg)

    except:
        context = {'status': 'error', 'error': 'An error occured while encoding your message. Try using an Image with a different file extention'}
        print(context)
        return context
    else:
        secret.save(f"{ENCRYPTED_UPLOAD_PATH}/{img_name}")
        context = {'status': 'success', 'encrypted_img_path': f"{ENCRYPTED_UPLOAD_PATH}/{img_name}"}
        return context



def decrypt_image(img_path):
    try:
        revealed_txt = lsb.reveal(img_path)

    except IndexError:
        context = {'status': 'error', 'error': 'Looks like Image was not encoded from Stenganograph'}
        return context

    except:
        context = {'status': 'error', 'error': 'An error occured while decoding your message'}
        return context

    else:
        context = {'status': 'success', 'revealed_msg': revealed_txt}
        return context
    
    
