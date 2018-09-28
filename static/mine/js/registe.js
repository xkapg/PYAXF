$(function () {
    $('.register').width(innerWidth)


    // 失去焦点
    // 用户名输入完成，发起ajax请求，验证该用户名是否能用
    $('#account').blur(function () {
        $.get('/axf/checkuser/', {'account':$(this).val()}, function (response) {
            console.log(response)
            if(response['status'] == '-1'){ // 用户存在
                $('#accounterr').show().html(response['msg'])
            } else {
                $('#accounterr').hide()
            }
        })
    })

    $('#password').blur(function () {
        var password = $(this).val()
        if(password.length<6 || password.length>12){
            $('#passworderr').show()
        } else {
            $('#passworderr').hide()
        }
    })

    $('#mypassword').blur(function () {
        var mypassword = $(this).val()
        if (mypassword.length < 6 || mypassword.length > 12 || mypassword != $('#password').val()) {
            $('#mypassworderr').show()
        } else {
            $('#mypassworderr').hide()
        }
    })
})