// $(document).ready(function(){
//     $('.upload_box').on('dragenter',function(e) {
//         $('.upload_box').addClass('file-over')  
//     });

//     $('.upload_box').on('dragleave',function(e) {
//         $('.upload_box').removeClass('file-over')    
//     });

//     $('.upload_box').on('drop', function(e) {
//         e.preventDefault()
//         e.stopPropagation()
//         $('.upload_box').removeClass('file-over')    
//         console.log('dropped')
//     });

//     $('.upload_box').on('dragover', function(e) {
//         e.preventDefault();    
//     });


// });

// selectInput

// Prvent reload
// const onConfirmRefresh = function (event) {
//     event.preventDefault();
//     alert('here')
//     return event.returnValue = "Are you sure you want to leave the page?";
//   }
  
// window.addEventListener("beforeunload", onConfirmRefresh, { capture: true });

function hideShow(hideElem, showElem){
    $(`.${hideElem}`).css("display", "none");
    $(`.${showElem}`).css("display", "flex");
}

function switchImg(elem, image){
    // alert(image)
    toggleText = document.getElementsByClassName('image-toggle-text')
    original_img = document.getElementsByClassName('original_img')[0]
    encoded_img = document.getElementsByClassName('encoded_img')[0]    

    for (let index = 0; index < toggleText.length; index++) {
        // if (elem != toggleText[index].classList.contains('active')){
        if (toggleText[index].classList.contains('active')){
            toggleText[index].classList.remove('active')
        }
        else{
            toggleText[index].classList.add('active')
        }
        // }
     
    }

    if (image == 'encoded'){
        encoded_img.style.display = 'inline-block'
        original_img.style.display = 'none'
    }

    else{
        original_img.style.display = 'inline-block'
        encoded_img.style.display = 'none'
    }
   
}
// how it works toggle

function guideToggler(user){
    // var selctedGuide = document.getElementsByClassName('guide')

    // for (let index = 0; index < selctedGuide.length; index++) {

    //     console.log(index)
    //     console.log(user)

    //     if (user = index) {
    //         selctedGuide[index].style.display='block'  

    //     }

    //     else{
    //         selctedGuide[index].style.display='none'
    //     }
        
    // }

    // if (word = 'premium') {
    //     alert(user)
    // }

    // else{
    //     alert(user)
    // }

}

function selectInput(opt){
    $('.file_input').trigger('click');
    document.getElementById("upload_file_form").addEventListener('input', (evt) => {
        // console.log(music.target.files);

        

        if (evt.target.files.length) {

            if (opt == 'decode') {
                $('#upload_file_form').submit()
            }


            var reader = new FileReader();

            reader.onload = function(){
                $(".preview_img").attr("src", reader.result);
            }

            reader.readAsDataURL(evt.target.files[0]);
            hideShow('upload_box', 'upload_box_2')


            }
        
    });
}

function urlPrompt(opt) {
    url = prompt('Paste a url')

    if (url == null || url == "") {
        console.log('noting was pasted')
    }

    else{

        $.get(url)
            .done(function() { 
                $('.url_text').val(url)
                console.log($('.url_text'))

                if (opt == 'decode'){
                    // var num = 1
                    $('#upload_file_form').submit()
                }

                $('.preview_img').attr("src", url)
                hideShow('upload_box', 'upload_box_2')
            })

            .fail(function() { 
                alert('Image not found on the web')

            })
        
         

            // $('.url_text').val(url)
            // $('.preview_img').attr("src", url)
            // hideShow('upload_box', 'upload_box_2')

        
       
    }
}

function downloadImg() {
    downloadTag = document.getElementsByClassName('download-link')[0]
    // modal = document.getElementsByClassName('download-failed')[0]

    $.get(downloadTag.href)
        .done(function() { 
            downloadTag.click()
            // $('.download-failed').modal('show')

        })

        .fail(function() { 
            $('.download-failed').modal('show')
        })

}