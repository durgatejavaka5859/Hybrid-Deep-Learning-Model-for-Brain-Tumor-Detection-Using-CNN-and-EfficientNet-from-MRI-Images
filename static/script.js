$(document).ready(function() {
    var dropArea = $("#drop-area");
    var inputFile = $("#input-file");
    var imageView = $("#img-view");

    inputFile.change(function() {
        uploadImage();
    });

    function uploadImage() {
        var imgLink = URL.createObjectURL(inputFile[0].files[0]);
        imageView.css({
            'background': '#fff',
            'background-repeat': 'no-repeat',
            'background-position': 'center',
            'background-image': 'url(' + imgLink + ')',
            'border': '0'
        });
        imageView.text("");
    }

    dropArea.on("dragover", function(e) {
        e.preventDefault();
    });

    dropArea.on("drop", function(e) {
        e.preventDefault();
        inputFile[0].files = e.originalEvent.dataTransfer.files;
        uploadImage();
    });

    $('#input-file').change(function() {
        var button = $("#uploadButton");
        if ($(this).val()) {
            button.css({
                'display': 'flex', 
                'justify-content': 'center',
                'align-items': 'center',
            });
            button.show();
            $('.loader').hide();
        } else {
            button.hide();
        }
    });

    $('#uploadButton').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/submit',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(data);
                console.log('JS/MODEL.JS : Successfully Predicted Output!');
            },
        });
    });
});


// $(document).ready(function () {
//     // Init
//     $('.image-section').hide();
//     $('.loader').hide();
//     $('#result').hide();
//     function readURL(input) {
//         if (input.files && input.files[0]) {
//             var reader = new FileReader();
//             reader.onload = function (e) {
//                 $('#imagePreview').attr( 'src', e.target.result );
//             }
//             reader.readAsDataURL(input.files[0]);
//         }
//     }
    
//     $("#imageUpload").change(function () {
//         $('.image-section').show();
//         $('#btn-predict').show();
//         $('#result').text('');
//         $('#result').hide();
//         $('#dropzone').hide();
//         readURL(this);
//     });

//     // Predict
//     $('#btn-predict').click(function () {
//         var form_data = new FormData($('#upload-file')[0]);

//         // Show loading animation
//         $(this).hide();
//         $('.loader').show();

//         // Make prediction by calling api /predict
//         $.ajax({
//             type: 'POST',
//             url: '/predict',
//             data: form_data,
//             contentType: false,
//             cache: false,
//             processData: false,
//             async: true,
//             success: function (data) {
//                 // Get and display the result
//                 $('.loader').hide();
//                 $('#result').fadeIn(600);
//                 $('#result').text(' Result:  ' + data);
//                 console.log('JS/MODEL.JS : Successfully Predicted Output!');
//             },
//         });
//     });

// });


// const dropArea = document.getElementById("drop-area");
// const inputFile = document.getElementById("input-file");
// const imageView = document.getElementById("img-view");
// inputFile.addEventListener("change", uploadImage);

// function uploadImage(){
//     let imgLink = URL.createObjectURL(inputFile.files[0]);
//     imageView.style.background="#fff";
//     imageView.style.backgroundRepeat= "no-repeat";
//     imageView.style.backgroundPosition= "center";
//     imageView.style.backgroundImage =  `url(${imgLink})`;
//     imageView.textContent = "";
//     imageView.style.border = 0;
// }

// dropArea.addEventListener("dragover", function(e){
//     e.preventDefault();
// });

// dropArea.addEventListener("drop", function(e){
//     e.preventDefault();
//     inputFile.files = e.dataTransfer.files;
//     uploadImage();
// });

// document.getElementById('input-file').addEventListener('change', function() {
//     if (this.value) {
//         document.getElementById('uploadButton').style.display = 'block';
//     } else {
//         document.getElementById('uploadButton').style.display = 'none';
//     }
// });

// $('#uploadButton').click(function () {
//         var form_data = new FormData($('#input-file')[0]);

//         //Show loading animation
//         // $(this).hide();
//         // $('.loader').show();

//         // Make prediction by calling api /predict
//         $.ajax({
//             type: 'POST',
//             url: '/submit',
//             data: form_data,
//             contentType: false,
//             cache: false,
//             processData: false,
//             async: true,
//             success: function (data) {
//                 // Get and display the result
//                 $('.loader').hide();
//                 $('#result').fadeIn(600);
//                 $('#result').text(' Result:  ' + data);
//                 console.log('JS/MODEL.JS : Successfully Predicted Output!');
//             },
//         });
// });
