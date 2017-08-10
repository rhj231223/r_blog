/**
 * Created by renhuijun on 2017/8/10.
 */

'use strict';

//simditor函数
$(function(){
    var content_html=$('#content_html');

    var editor,toolbar;
    toolbar=[
       'title','bold','italic','underline','strikethrough',
            'fontScale','color','ol' ,'ul' ,'blockquote','code' ,
            'table','link','image','hr','indent','outdent','alignment'

    ];

    editor=new Simditor({
        textarea:content_html,
        toolbar:toolbar,
        pasteImage:true,
    });

    window.editor=editor;

});

//添加分类的函数操作
$(function () {
    var category_btn=$('#category_btn');
    category_btn.click(function(event){
        event.preventDefault();

        xtalert.alertOneInput({
            title:'添加分类',
            text:'请输入添加分类的名称!',
            confirmButton:'添加',
            cancelButton:'取消',
            confirmCallback:function(inputValue){
                rhjajax.post({
                    url:'/cms/add_category/',
                    data:{
                        category_name:inputValue
                    },
                    success:function(data){
                        if(data['code']==200){
                            xtalert.alertSuccessToast('分类添加成功');
                            var res=data['data'];
                            var select=$('select[name=category_id]');
                            var option=$('<option></option>');
                            option.val(res['id']);
                            option.text(res['name']);
                            select.append(option);
                            option.attr('selected','selected');

                        }else{
                            xtalert.alertInfo(data['message'])
                        }
                    }
                })
            }
        })
    })
});

//上传图片的函数
$(function(){
    var thumbnail_btn=$('#thumbnail_btn');
    thumbnail_btn.click(function(event){
        event.preventDefault();
    });
    var thumbnail=$('input[name=thumbnail]');
    xtqiniu.setUp({
        browse_button:'thumbnail_btn',
        success:function(up,file,info){
            var file_url=file.name;
            thumbnail.val(file_url);
        },
    })
});

//添加标签的函数
$(function(){
    var tag_btn=$('#tag_btn');
    tag_btn.click(function(event){
        event.preventDefault();

        xtalert.alertOneInput({
            title:'添加标签',
            text:'请输入添加的标签名称',
            confirmButton:'添加',
            cancelButton:'取消',
            confirmCallback:function(inputValue){
                rhjajax.post({
                    url:'/cms/add_tag/',
                    data:{
                        tag_name:inputValue,
                    },
                    success:function(data){
                        if(data['code']==200){
                            var tag_list=$('#tag_list');
                            var tag=data['data'];
                            var html=xttemplate.template('tag_template',{'id':tag['id'],'name':tag['name']});
                            console.log(html);
                            tag_list.append(html);
                            xtalert.alertSuccessToast('分类添加成功!');
                        }else{
                            xtalert.alertInfo(data['message'])
                        }
                    }
                })
            },

        });
    });
});

//提交文章的函数
$(function(){
    var submit_btn=$('#submit_btn');

    submit_btn.click(function(event){
        event.preventDefault();

        var title=$('input[name=title]');
        var category_id=$('select[name=category_id]');
        var desc=$('input[name=desc]');
        var thumbnail=$('input[name=thumbnail]');
        var content_html=window.editor.getValue();
        var tags_checked=$(':checkbox:checked');
        var tags=[];
        tags_checked.each(function(){
            tags.push($(this).val())
        });

        var article_id=submit_btn.attr('data_article_id');

        rhjajax.post({
            url:window.location.href,
            data:{
                title:title.val(),
                category_id:category_id.val(),
                desc:desc.val(),
                thumbnail:thumbnail.val(),
                content_html:content_html,
                tags:tags,
                article_id:article_id,
            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertConfirm({
                        title:'发布成功!',
                        text:'恭喜！文章保存成功!是否再发一篇?',
                        confirmText:'再发一篇',
                        cancelText:'返回首页',
                        confirmCallback:function(){
                     //        title.val('');
                     //        desc.val('');
                     //        thumbnail.val('');
                     // window.editor.setValue('');
                     //        tags_checked.each(function(){
                     //            $(this).prop('checked',false)
                     //        });
                            window.location='/cms/add_article/';

                        },
                        cancelCallback:function(){
                              setTimeout(function(){
                                window.location='/cms/'
                            },500)
                        }

                    })
                }else{
                    xtalert.alertInfo(data['message'])
                       }
            }
        })
    })
});