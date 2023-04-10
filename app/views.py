from django.shortcuts import render, redirect
from app import brain

REGULAR_UPLOAD_PATH = 'media/r_uploads'
ENCRYPTED_UPLOAD_PATH = 'media/encryptedImages'

# Create your views here.
def home(request):
    template_name = 'index.html'
    content = {}
    return render(request, template_name, content)


def encode(request):
    template_name = 'encode.html'

    if request.method == 'POST':
        form_data = request.POST
        user_text = form_data['s-msg']

        if form_data['link-image']  != '':
            image_url = form_data['link-image']
            userimage = brain.SaveImage(img=image_url, is_link=True)

        else:
            image = request.FILES['image']
            userimage = brain.SaveImage(img=image, is_link=False)

        if userimage.is_saved:
            result = brain.encrypt_image(img_path=userimage.img_path, msg=user_text, img_name=userimage.img_name)
            if result['status'] == 'success':
                content = {'result': True, 'user_image': userimage.img_path, 'encrypted_img': result['encrypted_img_path'] }
                print(content)
                return render(request, 'encode.html', context=content)
                # return redirect('result')
            
            else:
                content = {'result': 'encode', 'user_image': userimage.img_path, 'error': result['error'] }
                return render(request, 'encode.html', context=content)
                # return redirect('result')


        content = {'result': True, 'user_image': userimage.img_path, 'error': 'This image was not saved, Try using a Image with a different file extention' }
        return render(request, 'decode.html', context=content)

        
    content = {}
    return render(request, template_name, content)


def decode(request):
    template_name = 'decode.html'

    try:
        query_image = request.GET['image']
    except:
        query_image = None


    if request.method == 'POST' or query_image != None:
        form_data = request.POST

        if query_image != None:
            image_url = query_image
            userimage = brain.SaveImage(img=image_url, is_link=True, encode=False)


        elif form_data['link-image']  != '':
            image_url = form_data['link-image']
            userimage = brain.SaveImage(img=image_url, is_link=True, encode=False)

        else:
            image = request.FILES['image']
            userimage = brain.SaveImage(img=image, is_link=False,  encode=False)

        
        if userimage.is_saved:
            result = brain.decrypt_image(img_path= userimage.img_path)
            if result['status'] == 'success':
                content = {'result': True, 'user_image': userimage.img_path, 'revealed_text': result['revealed_msg'] }
                print(content)
                return render(request, 'decode.html', context=content)
            
            else:
                content = {'result': True, 'user_image': userimage.img_path, 'error': result['error'] }
                print(content)
                return render(request, 'decode.html', context=content)
            
        print('high error')
        content = {'result': True, 'user_image': userimage.img_path, 'error': 'The image wasn not saved, Try using a different or valid image' }
        return render(request, 'decode.html', context=content)



    content = {}
    return render(request, template_name, content)



def result(request):
    return render(request, 'result.html', context={})