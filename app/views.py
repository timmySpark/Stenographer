from django.shortcuts import render, redirect
from stegano import lsb
from app import brain

REGULAR_UPLOAD_PATH = 'media/r_uploads'

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
                content = {'sten_type': 'encode', 'user_image': userimage.img_path, 'encrypted_img': result['encrypted_img_path'] }
                print(content)
                # return render(request, 'result.html', context=content)
                return redirect('result')
            
            else:
                content = {'sten_type': 'encode', 'user_image': userimage.img_path, 'error': result['error'] }
                # return render(request, 'result.html', context=content)
                return redirect('result')


        print('High error')

        
    content = {}
    return render(request, template_name, content)


def decode(request):
    template_name = 'decode.html'

    if request.method == 'POST':
        form_data = request.POST

        if form_data['link-image']  != '':
            image_url = form_data['link-image']
            userimage = brain.SaveImage(img=image_url, is_link=True, encode=False)

        else:
            image = request.FILES['image']
            userimage = brain.SaveImage(img=image, is_link=False,  encode=False)

        
        if userimage.is_saved:
            result = brain.decrypt_image(img_path= userimage.img_path)
            if result['status'] == 'success':
                content = {'sten_type': 'decode', 'user_image': userimage.img_path, 'revealed_text': result['revealed_msg'] }
                print(content)
                return render(request, 'result.html', context=content)
            
            else:
                content = {'sten_type': 'decode', 'user_image': userimage.img_path, 'error': result['error'] }
                print(content)
                return render(request, 'result.html', context=content)

        print('High error')


    content = {}
    return render(request, template_name, content)



def result(request):
    return render(request, 'result.html', context={})