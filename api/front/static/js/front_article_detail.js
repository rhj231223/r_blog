/**
 * Created by renhuijun on 2017/8/14.
 */
'use strict';

$(function(){
    var comment_btn=$('#comment_btn');
    comment_btn.click(function(event){
        event.preventDefault();

        var content=$('textarea[name=content]');
        var article_id=comment_btn.attr('data_article_id');
        var comment_id=comment_btn.attr('data_comment_id');
        var url='';
        var msg='';
        if(comment_id){
            url='/edit_comment/';
            msg='评论修改成功!'
        }else{
            url='/add_comment/';
            msg='评论成功!'
        }




        rhjajax.post({
            url:url,
            data:{
                content:content.val(),
                article_id:article_id,
                comment_id:comment_id,
            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function(){
                        if(url=='/edit_comment/'){
                            window.location='/article_detail/'+article_id+'/#footer';
                        }else{
                            window.location.reload()
                        }
                    },1200)
                }else{
                    xtalert.alertInfo(data['message'])
                }
            }
        })

    })
});