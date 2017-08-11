# coding:utf-8
def pagination(page,total_num,single_page_num,show_page_num):
    current_page=int(page)

    total_page=total_num//single_page_num
    if total_num%single_page_num:
        total_page+=1

    start=single_page_num*(current_page-1)
    end=start+single_page_num

    tmp_page=current_page-1

    page_list=[]

    while tmp_page>0:
        if tmp_page%show_page_num:
            page_list.append(tmp_page)
        else:
            break
        tmp_page-=1

    tmp_page=current_page

    while tmp_page<=total_page:
        page_list.append(tmp_page)
        if tmp_page%show_page_num:
            tmp_page+=1
        else:
            break
    page_list.sort()
    return (total_page,start,end,page_list)



