import os
from django.core.files.storage import FileSystemStorage
from stegano import lsb
from datetime import datetime, timedelta  
import cv2
import time
import requests
import random
import string

REGULAR_UPLOAD_PATH = 'media/r_uploads'


class SaveImage:
    def __init__(self, img, is_link=False, encode=True):
        self.error = []
        self.img_name = None
        self.is_saved = False
        self.img_path = None
        self.save(img, is_link, encode)

        
    def save(self, unsaved_img, is_link, encode):
        characters = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(5))

        if encode:
            cv_Imgname = f"steganograph_{characters}.PNG"

        else:
            cv_Imgname = f"steganograph(decode){characters}.PNG"

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
            print(fss.url(file))
        
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
        context = {'status': 'error', 'error': 'An error occured while decoding your message'}
        return context
    else:
        secret.save(f"encryptedImages/{img_name}")
        context = {'status': 'success', 'encrypted_img_path': f"encryptedImages/{img_name}"}
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
    
    
