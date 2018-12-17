$(function () {
    $(".delete-fuser-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var comment_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这个用户吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dcomments/',
                    'data':{
                        'comment_id': comment_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            zlalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});