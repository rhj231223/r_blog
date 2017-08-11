/**
 * Created by renhuijun on 2017/8/11.
 */
'use strict';

$(function(){
    var current_index=1;
    var current_url=window.location.href;
    var nav_ul= $('.nav_style');

    if(current_url.indexOf('category_manage')>0){
        current_index=2;
    }else if(current_url.indexOf('comment_manage')>0){
       current_index=3;
    }else{
        current_index=1;
    }

   nav_ul.children().eq(current_index-1).addClass('active').siblings().removeClass('active');

});