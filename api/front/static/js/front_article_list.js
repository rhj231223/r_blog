/**
 * Created by renhuijun on 2017/8/13.
 */
'use strict';

$(function(){
    var load_btn=$('#load_btn');
    var total_page=load_btn.attr('data_total_page');
    var current_category_id=parseInt(load_btn.attr('data_current_category_id'));
    var current_page=parseInt(load_btn.attr('data_current_page'));

    load_btn.click(function(event){
        event.preventDefault();
        load_btn.addClass('disabled');
        load_btn.text('加载中...');

        var page=current_page+1;
        var url='/article_list/'+page+'/'+current_category_id+'/';



        rhjajax.get({
            url:url,
            success:function(data){
                var articles=data['data']['articles'];

                var main_article=$('#main_article');
                for(var i=0;i<articles.length;i++){
                    var article=articles[i];
                    var content_html=article['content_html'];
                    content_html=$(content_html).text();
                    if(!content_html){
                        content_html=article['content_html']
                    }else{
                      content_html=content_html.slice(0,100)+'...';
                      article['content_html']=content_html;
                    }

                    var html=xttemplate.template('article_list_tpl',{'article':article});
                    main_article.append(html);
                }

                 if(current_page<total_page){
                    current_page=page;
                    load_btn.removeClass('disabled');
                    load_btn.text('加载更多');
                }else{
                    load_btn.addClass('disabled');
                    load_btn.text('没有更多的文章了')

                 }




            }
        })

    })


});