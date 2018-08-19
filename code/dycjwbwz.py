#-*-coding:utf-8-*-
import requests
import re
import time
import pymysql
import datetime


def get_config():
    config = open('config.txt').read()

    re_token = re.compile(r'cookie:(.*?)\n')
    token = re_token.findall(config)[0]

    re_host = re.compile(r'host:(.*?)\n')
    host = re_host.findall(config)[0]

    re_user = re.compile(r'user:(.*?)\n')
    user = re_user.findall(config)[0]

    re_password = re.compile(r'password:(.*?)\n')
    password = re_password.findall(config)[0]

    re_db = re.compile(r'db_name:(.*?)\n')
    db = re_db.findall(config)[0]

    re_page = re.compile(r'page:(.*?)\n')
    page = re_page.findall(config)[0]

    ts = re.compile(r'ts:(.*?)\n')
    ts = ts.findall(config)[0]

    configlist = [token,host,user,password,db,page,ts]
    ###print(configlist)

    return configlist



def get_urllist():

    sql = "select wburl from v_xlwbzh  where dycj = '1';"
    curos.execute(sql)
    db.commit()
    result = curos.fetchall()
    result = str(result)
    re_wxhlist = re.compile(r'\'(.*?)\'')
    wxhlist = re_wxhlist.findall(result)
    #####print(wxhlist)
    #####print(len(wxhlist))
    return wxhlist


def get_data(s,wburl,wbmc):
    try:

        if '登录 - 新浪微博' not in s:

            wbmc =wbmc


            re_wbnr = re.compile(r'</div><div class="c" id(.*?)来自')
            wbnr = re_wbnr.findall(s)
            #####print(wbnr)



            for i in wbnr:
                #####print(i)
                #####print('///////////////////////')
                re_nr = re.compile(r'class="ctt">(.*?)</div>')
                nr = re_nr.findall(i)
                #####print(nr)

                re_uid = re.compile(r'/u/(\d.*)')
                uid = re_uid.findall(wburl)
                ####print(uid)
                #####print(uid[0])
                # ###print(uid)
                # ###print(wburl)

                if len(nr) ==0 :
                    re_nr = re.compile(r'class="ctt">(.*?)赞')
                    nr = re_nr.findall(i)
                    dr = re.compile(r'<[^>]+>', re.S)
                    nr = dr.sub('', nr[0])
                    nr = [nr.replace('&nbsp','')]
                else:
                    dr = re.compile(r'<[^>]+>', re.S)
                    nr = dr.sub('', nr[0])
                    nr = [nr.replace('&nbsp','')]

                #####print(nr)

                # re_img = re.compile(r'<img src="(http.*?jpg)" alt="图片"')
                # img = re_img.findall(i)
                # #####print(img)
                # if len(img) == 0:
                #     img = ['']

                re_wzurl = re.compile(r'="M_(.*?)">')
                wzurl = re_wzurl.findall(i)

                wzurl = 'https://weibo.com/'+uid[0]+'/'+wzurl[0]+'?type=comment'
                wzurl = [wzurl]
                #####print(wzurl)

                re_zfs = re.compile(r'转发\[(\d*?)\]')
                zfs = re_zfs.findall(i)
                #####print(zfs)

                re_dzs = re.compile(r'赞\[(\d*?)\]')
                dzs = re_dzs.findall(i)
                #####print(dzs)

                re_pls = re.compile(r'评论\[(\d*?)\]')
                pls = re_pls.findall(i)
                #####print(pls)

                re_fbsj = re.compile(r'class="ct">(.*?)&nbsp;')
                fbsj = re_fbsj.findall(i)
                #####print(fbsj)

                cjsj = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                #####print(cjsj)

                key = [wbmc,nr,wzurl,zfs,dzs,pls,fbsj,cjsj]
                #####print(key)
                save_mysql(key,wburl)


        else:
            #####print('网址有111111111111111111问题')
            log = str(wburl) + '网址有错误，微博号有误'
            zt = 2
            sava_log(log, zt)
    except:
        log = str(wburl) + '网址有错误，微博号有误'
        zt = 2
        sava_log(log, zt)
        #####print('网址有33333333333333333问题')


def save_mysql(key,wburl):

    time.sleep(0.34)

    try:
        '[i,tx,wbdj,wbrz,fss,gzs,wbs,xqbq,jj,dz,byxx,gxym,hylb,csrq,sjly,cjsj]'
        #####print('1111111111111111111111111111111111111111111111111')
        wbmc = key[0][0]
        bwnr = str(key[1][0].replace(r'\'',''))
        bwnr = bwnr.replace('"','')
        img_url = key[2][0]
        zfs = key[3][0]
        dzs = key[4][0]
        pls = key[5][0]
        fbsj = key[6][0]
        cjsj = key[7]
        #####print('444444444444444444444444444')
        zhfbsj = fbsj

        if '月' in fbsj:
            zhfbsj = str(datetime.datetime.now().year) + '-'+fbsj
            zhfbsj =zhfbsj.replace('月','-')
            zhfbsj = zhfbsj.replace('日','')
            zhfbsj = zhfbsj + ':00'
            #####print(zhfbsj)
            #####print('///********----------')
        if '今天' in fbsj:
            sj = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
            zhfbsj = sj + fbsj.replace('今天','') + ':00'
            #####print(zhfbsj)
            #####print('///********----------')
        if '分钟' in fbsj:
            '40分钟前'
            sjs = int(fbsj.split('分')[0])
            nowt = datetime.datetime.now()
            zhfbsj = nowt + datetime.timedelta(minutes=-sjs)
            zhfbsj = zhfbsj.strftime("%Y-%m-%d %H:%M:%S")
            #####print(zhfbsj)
            #####print('///********----------')
        '2018-05-22 11:05:00'
        ##print('************************')
        '开始计算采集天数'

        fbsjts = zhfbsj.replace(' ','-')
        fbsjts = fbsjts.split('-')
        ##print(fbsjts)
        fbsjts = datetime.datetime(int(fbsjts[0]),int(fbsjts[1]),int(fbsjts[2]))
        ##print(fbsjts)
        cjsjts = cjsj.replace(' ','-')
        cjsjts = cjsjts.split('-')
        cjsjts = datetime.datetime(int(cjsjts[0]),int(cjsjts[1]),int(cjsjts[2]))
        ##print(cjsjts)
        dayss = (cjsjts - fbsjts).days
        ##print(dayss)
        if dayss < int(ts):
            #####print('*-8561111111111111111')

            sql = "REPLACE into v_xlwbwz (wbmc,wburl,bwnr,wzurl,zfs,dzs,pls,fbsj,zhfbsj,cjsj) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(wbmc,wburl,bwnr,img_url,zfs,dzs,pls,fbsj,zhfbsj,cjsj);
            curos.execute(sql)
            db.commit()
            ##print(sql)
            log = str(wburl) + '文章信息存入数据库'
            zt = 1
            time.sleep(0.1)
            sava_log(log, zt)
        else:
            pass
        # if img_url not in wburllist:
        #     #####print(img_url)
        #     #####print(wburllist)
        #     # sql = "update t_xlwbzh set tx='%s',wbdj='%s',wbrz='%s',fss='%s',gzs='%s',wbs='%s',xqbq='%s',jj='%s',dz='%s',byxx='%s',gxym='%s',hylb='%s'," \
        #     #       "csrq='%s',sjly='%s',cjsj='%s' WHERE " \
        #     #       "wburl='%s';" % (tx,wbdj,wbrz,fss,gzs,wbs,xqbq,jj,dz,byxx,gxym,hylb,csrq,sjly,cjsj,wburl)
        #
        #     sql = "insert into v_xlwbwz (wbmc,wburl,bwnr,wzurl,zfs,dzs,pls,fbsj,zhfbsj,cjsj) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(wbmc,wburl,bwnr,img_url,zfs,dzs,pls,fbsj,zhfbsj,cjsj)
        #     ###print(sql)
        #     curos.execute(sql)
        #     #####print('333333333333333333333333')
        #     log = str(wburl) + '网址文章信息插入成功'
        #     zt = 1
        #     sava_log(log, zt)
        # else:
        #     sql = "update v_xlwbwz set zfs ='%s',dzs = '%s', pls = '%s',fbsj = '%s',zhfbsj='%s',cjsj ='%s' WHERE  wzurl ='%s';"%(zfs,dzs,pls,fbsj,zhfbsj,cjsj,img_url)
        #     #####print(sql)
        #     curos.execute(sql)
        #     log = str(wburl) + '网址文章信息更新成功'
        #     zt = 1
        #     sava_log(log, zt)

    except:
        #####print('************----------------**********')
        #####print(str(key[0]) + '网址信息存入失败',+ sql)
        log = str(key[0]) + '文章信息存入失败'
        zt = 2
        sava_log(log,zt)

def sava_log(log,zt):
    sj = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    sql = "insert into v_xlwbwzlog (sj,log,zt) VALUES ('%s','%s','%s');"%(sj,log,zt)
    curos.execute(sql)
    db.commit()
    ##print(sql)

def main():

    urlist = get_urllist()

    configlist = get_config()
    cookie = configlist[0]
    page = int(configlist[5])
    ###print(page)
    for i in urlist:
        time.sleep(0.3)
        sql = "select wbmc from v_xlwbzh  where wburl='%s';"%i
        curos.execute(sql)
        db.commit()
        result = curos.fetchall()
        result = str(result)
        # ###print(result)
        wbmc = re.compile(r"\(\'(.*?)\',\)")
        wbmc = wbmc.findall(result)
        ###print(wbmc)
        for pagenum in range(0,page+1):
            try:
                time.sleep(3)
                #####print(i)

                url = i.replace('com','cn')

                url = url + '?page=' + str(pagenum)
                print(url)
                ###print(url)
                #####print('9999999')
                #####print(url)
                #####print('1111111111')
                data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, sdch, br',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'keep-alive',
                        'Host': 'weibo.cn',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                        'Cookie':cookie}
                res = requests.get(url,headers = data)
                get_data(res.text,i,wbmc)

            except:
                pass

    db.close()


if __name__ == '__main__':
    print('版本号V-2，更新时间2018-5.26 16:00')
    configlist = get_config()
    host = configlist[1]
    user = configlist[2]
    password = configlist[3]
    dbname = configlist[4]
    ts = configlist[6]
    db = pymysql.connect(host=host, user=user, passwd=password, db=dbname, charset='utf8')
    curos = db.cursor()
    # sql1 = 'select wzurl from v_xlwbwz;'
    # curos.execute(sql1)
    # result1 = curos.fetchall()
    # result1 = str(result1)
    # re_wburllist = re.compile(r'\'(.*?)\'')
    # wburllist = re_wburllist.findall(result1)
    #####print(wburllist)
    #####print(len(wburllist))
    main()