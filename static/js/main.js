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
$(document).ready(function(){
    

});

function hideShow(hideElem, showElem){
    $(`.${hideElem}`).css("display", "none");
    $(`.${showElem}`).css("display", "flex");
}


function selectInput(){
    $('.file_input').trigger('click');
    document.getElementById("upload_file_form").addEventListener('input', (evt) => {
        // console.log(music.target.files);
        if (evt.target.files.length) {
            var reader = new FileReader();
 
            reader.onload = function(){
                $(".preview_img").attr("src", reader.result);
            }

            reader.readAsDataURL(evt.target.files[0]);
            hideShow('upload_box', 'upload_box_2')

            // $('#upload_file_form').submit()
        }
        
    });
}

function urlPrompt() {
    url = prompt('Paste a url')

    if (url == null || url == "") {
        console.log('noting was pasted')
    }

    else{
        // setting form value
        $.get(url)
            .done(function() { 
                $('.url_text').val(url)
                $('.preview_img').attr("src", url)
                // $('#upload_file_form').submit()
                 hideShow('upload_box', 'upload_box_2')
            })

            .fail(function() { 
                alert('Image not found on the web')
            // Image doesn't exist - do something else.

        })
        
        
       
    }
}