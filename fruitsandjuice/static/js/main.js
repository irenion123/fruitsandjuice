// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var reg_validator = {
    rules: {
        name: {
            required: true,
            lettersonly: true
        },
        email: {
            required: true,
            email: true
        },
        password1: {
            required: true
        },
        password2: {
            required: true,
            equalTo: "#regInputPassword1"
        },

    },
    messages: {
        name: {
            required: "Поле не может быть пустым"
        },
        email: {
            required: "Поле не может быть пустым",
            email: "Адрес должен быть вида name@domain.com"
        },
        password1: {
            required: "Поле не может быть пустым"
        },
        password2: {
            required: "Поле не может быть пустым",
            equalTo: "Пароли не совпадают"
        }

    },
    focusInvalid: true,
    errorClass: "error_small is-invalid",
    debug: true
};

$.validator.addMethod("lettersonly", function (value, element) {
    return this.optional(element) || /^[a-z]+$/i.test(value);
}, "Разрешены только латинские буквы");

var reg_form = $("#reg_form");
var objreg_validate = reg_form.validate(reg_validator);

function registration() {
    console.log("registartion!") // sanity check
    if (reg_form.valid()) {
        console.log('valid')
        $.ajax({
            url: "/registration/", // the endpoint
            type: "POST", // http method
            data: {
                username: $('#regInputName').val(),
                email: $('#regInputEmail1').val(),
                password1: $('#regInputPassword1').val(),
                password2: $('#regInputPassword2').val()
            }, // data sent with the post request

            // handle a successful response
            success: function (json) {
                $('#regInputName').val('');
                $('#regInputEmail1').val('');
                $('#regInputPassword1').val('');
                $('#regInputPassword2').val('');// remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                $('#results').html("<div class='alert alert-success' role='alert'>Поздравляем, "
                    + json.user
                    + "! Вы успешно зарегистрированы. "
                    + " На Ваш емаил "
                    + json.email
                    + " было отправлено письмо с подтверждением регистрации."
                    + "</div>");
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Ой, что-то пошло не так. (Возможно пользователь с таким Логином уже существует)"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });

    } else {
        objreg_validate.focusInvalid();
    }

    return false;
};

var login_validator = {
    rules: {
        name: {
            required: true,
            lettersonly: true
        },
        password: {
            required: true
        },

    },
    messages: {
        name: {
            required: "Поле не может быть пустым"
        },

        password: {
            required: "Поле не может быть пустым"
        },


    },
    focusInvalid: true,
    errorClass: "error_small is-invalid",
    debug: true
};

var login_form = $("#login_form");
var objlogin_validate = login_form.validate(login_validator);

function login() {
    console.log("login!");
    if (login_form.valid()) {
        console.log('Valid OK!')
        $.ajax({
            url: "/login/", // the endpoint
            type: "POST", // http method
            data: {
                username: $('#loginInputName').val(),
                password: $('#loginInputPassword').val()
            }, // data sent with the post request

            // handle a successful response
            success: function (json) {
                $('#loginInputName').val('')

                $('#loginInputPassword').val('');

                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                window.location.reload();
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#login_error').html("<div class='alert alert-danger' role='alert'>"
                    + "Неверный логин или пароль"
                    + "</div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    } else {
        objlogin_validate.focusInvalid();

    }
    ;
    return false;
};

function addProduct(e) {
    console.log('addProduct: ' + $(this).val($(this).attr("value")));
    e.preventDefault();
    $.ajax({
        url: "/cart/add/", // the endpoint
        type: "POST", // http method
        data: {
            item: $(this).attr("value")
        }, // data sent with the post request

        // handle a successful response
        success: function (json) {

            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function removeProduct() {
    console.log('removeProduct: ' + $(this).val($(this).attr("value")));

    $.ajax({
        url: "/cart/remove/", // the endpoint
        type: "POST", // http method
        data: {
            item: $(this).attr("value")
        }, // data sent with the post request

        // handle a successful response
        success: function (json) {

            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

$("#reg_post").click(registration);
$("#login_post").click(login);
$(".card_add").click(addProduct);
$(".prod_remove").click(removeProduct);
