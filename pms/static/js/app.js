$(document).ready(function(){

let rexp = {
    name : /^[a-zA-Z]+$/,
    number : /^[0-9]+$/,
    username : /^[\w]+$/,
    email : /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
    adress : /^[\w\-\s\,]+$/,
    password : /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/,
    sreg : /^[\w\-\?\s]+$/i
}

//Preview Image before submission
let preview_image = (event) => {
    var reader = new FileReader();
    reader.onload = function(){
    document.getElementById('imgcircle').src = reader.result;
   }
    reader.readAsDataURL(event.target.files[0]);
}

let validate = (field) => {
    if(!document.querySelector(".error")){
        let value = $(`#id_${field}`).val();
        let exts = ['jpg', 'jpeg', 'png'];
        if(field == "image"){
			var get_ext = value.split('.').reverse()[0].toLowerCase();
			if(!($.inArray (get_ext, exts) > -1)){
                $(`#id_${field}`).after(`<span class="error">Invalid Image</span>`);
            }
        }else if(field == "password" || field == "password2"){
            if( value.length < 8   ){
                $(`#id_${field}`).after(`<span class="error">Password must be @least 8 character}</span>`);
            }else if( $("#id_password").val() != $("#id_password2").val() ){
                $(`#id_${field}`).after('<div class="error">Password doesnt match</div>');
            }else if( !rexp.password.test(value) ){
                $(`#id_${field}`).after('<span class="error">Password not strong enough</span>');
            }else if( value == $("#id_username").val()  ){
                $(`#id_${field}`).after('<span class="error">Password must be different from username</span>');
            }
        }
        else if(field == "email"){
            if( value == "" || !rexp.email.test(value) ){
                $(`#id_${field}`).after(`<span class="error">Invalid Email</span>`);
            }
        }else if(field == "username" || field == "option"){
            if( value == "" ){
                $(`#id_${field}`).after(`<span class="error">${field} must not be empty</span>`);
            }
        }else{
            document.querySelector("#tab2").classList.remove("disbled")
            $("#personal").trigger("click");
        }
    } 
}

$("#id_image").change(() => {
    preview_image(event);
})

let allField = ["image","option", "username", "password", "password2", "email", ""]

$("#next").click(() => {
    try{
        for(field of allField){
            validate(field )
         }
    }catch(error){
        alert("Error Validating Fields");
    }
})

$("#back").click(() => {
    $("#login").trigger("click");
})

//remove the error from input field
$("input").change(function(){
    $(".error").remove();
});
$("input").keypress(function(){
    $(".error").remove();
});
$("select").change(function(){
    $(".error").remove();
});
$("select").keypress(function(){
    $(".error").remove();
});
    

//Validating File upload for Eligible student
$("#id_sheet").change(function(){
    let value = $("#id_sheet").val()
    value  = value.split(".")[1]
    if(value != "xlsx"){
        document.querySelector("#sheet_btn").classList.add("disabled");
        alert("Invalid FIle Format")
    }else{
        document.querySelector("#sheet_btn").classList.remove("disabled");
    }
});


// $(function(){
// 	$("#query").autocomplete({
//     minLength: 2,
//     source: ["Omojugba", "Olawale", "Computer", "Computer Science"]
//     });
//   });

var loadForm = function() {
    var btn = $(this);
    $.ajax({
   url: btn.attr("data-url"),
   type: 'get',
   dataType: 'json',
   beforeSend: function () {
     $("#modal_user .modal-content").html("");
     $("#modal_user").modal("show");
   },
   success: function (data) {
     $("#modal_user .modal-content").html(data.request_form);
   }
 });
};
//End of request form trigger

var saveForm = function(event){
 var form = $(this);
 $.ajax({
   url: form.attr("data-url"),
   data: form.serialize(),
   type: form.attr("method"),
   dataType: 'json',
   success: function (data) {
     if (data.form_is_valid) {
        $("#modal_del").modal("hide");
        url = "{% url 'pms:std_list' %}";
     }
     else {
       $("#modal_del .modal-content").html(data.request_form);
     }
   }
 }); 
};

//create request
$(".js-create-request").click(loadForm);
$("#req_form").submit(saveForm);

//update request
$(".js-edit-user").click(loadForm);
$("#req_update").submit(saveForm);

//delete User
$(".js-delete-user").click(loadForm);
$("#user_delete").submit(saveForm);

});

