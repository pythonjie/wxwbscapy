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

    configlist = [token,host,user,password,db]
    #print(configlist)

    return configlist



def get_urllist():
    sql ="select wburl from v_xlwbzh;"
    curos.execute(sql)
    result = curos.fetchall()
    result = str(result)
    re_wxhlist = re.compile(r'\'(.*?)\'')
    wxhlist = re_wxhlist.findall(result)
    #print(wxhlist)
    #print(len(wxhlist))
    return wxhlist


def get_data(html,wburl):
        if '登录 - 新浪微博' not in html:
            re_wbmc = re.compile(r'<div class="ut"><span class="ctt">(.*?)<')
            wbmc = re_wbmc.findall(html)
            #print(wbmc)

            if len(wbmc) == 0:
                #print('网址有111111111111111111问题')
                log = str(wburl) + '网址有错误，微博号有误'
                zt = 2
                sava_log(log, zt)
            else:
                re_tx = re.compile(r'手机微博触屏版,点击前往.*?<img src="(.*?)" alt="头像"')
                tx = re_tx.findall(html)
                #print(tx)

                if len(tx) == 0:
                    tx = ''
                else:
                    tx = tx[0]

                #微博等级暂时没有

                re_wbrz = re.compile(r"认证：(.*?)<")
                wbrz = re_wbrz.findall(html)
                #print(wbrz)
                if len(wbrz) == 0:
                    wbrz = ''
                else:
                    wbrz = wbrz[0]


                re_fss = re.compile(r'粉丝\[(.*?)\]')
                fss = re_fss.findall(html)
                #print(fss)
                if len(fss) == 0:
                    fss = ''
                else:
                    fss = fss[0]

                re_gzs = re.compile(r'关注\[(.*?)\]')
                gzs = re_gzs.findall(html)
                #print(gzs)
                if len(gzs) == 0:
                    gzs = ''
                else:
                    gzs = gzs[0]


                re_wbs = re.compile(r'微博\[(.*?)\]')
                wbs = re_wbs.findall(html)
                #print(wbs)
                if len(wbs) == 0:
                    wbs = ''
                else:
                    wbs = wbs[0]


                re_jj  =re.compile(r'><span class="ctt" style="word-break:break-all; width:50px;">(.*?)</span>')
                jj = re_jj.findall(html)
                #print(jj)
                if len(jj) == 0:
                    jj = ''
                else:
                    jj = jj[0]

                re_dz = re.compile(r'alt="M"/></a>&nbsp;./(.*?)&nbsp;')
                dz = re_dz.findall(html)
                #print(dz)
                #print('+++++++++++++')
                if len(dz) == 0:
                    dz = ''
                else:
                    dz = dz[0]

                cjsj = cjsj = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                sjly = '2'

                key = [wbmc[0],tx,wbrz,fss,gzs,wbs,jj,dz,sjly,cjsj]
                #print(key)

                save_mysql(key,wburl)
        else:
            #print('网址有111111111111111111问题')
            log = str(wburl) + '网址有错误，微博号有误'
            zt = 2
            sava_log(log, zt)


def save_mysql(key,wburl):
    sql = 'select wzurl from v_xlwbwz;'
    curos.execute(sql)

    try:
        '[wbmc[0],tx,wbrz,fss,gzs,wbs,jj,dz,sjly,cjsj]'
        #print('1111111111111111111111111111111111111111111111111')
        wburl = wburl
        wbmc = key[0]
        tx = key[1]
        wbrz = key[2]
        fss = key[3]
        gzs = key[4]
        wbs = key[5]
        jj = str(key[6])
        dz = key[7]
        sjly = key[8]
        cjsj = key[9]

        #print('9999995555555555666666')

        sql = "update v_xlwbzh set wbmc = '%s',tx = '%s',wbrz = '%s',fss='%s',gzs='%s',wbs ='%s',jj='%s',dz='%s',sjly='%s',cjsj='%s' WHERE " \
              "wburl='%s';" % (wbmc,tx,wbrz,fss,gzs,wbs,jj,dz,sjly,cjsj,wburl)
        #print(sql)
        curos.execute(sql)
        #print('333333333333333333333333')
        log = str(wburl) + '网址信息更新成功'
        zt = 1
        sava_log(log, zt)

    except:
        #print('************----------------**********')
        #print(str(key[0]) + '网址信息存入失败'+ sql)
        log = str(key[0]) + '网址信息存入失败'+ sql
        zt = 2
        sava_log(log,zt)




def sava_log(log,zt):


    sj = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    sql = "insert into v_xlwbzhlog (sj,log,zt) VALUES ('%s','%s','%s');"%(sj,log,zt)
    curos.execute(sql)


def main():

    urlist = get_urllist()
    configlist = get_config()
    cookie = configlist[0]
    for i in urlist:
        try:
            time.sleep(4)
            #print(i)
            print(i)
            url = i.replace('com','cn')
            #print('9999999')
            #print(url)
            #print('1111111111')
            data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, sdch, br',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Host': 'weibo.cn',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                    'Cookie': cookie}
            res = requests.get(url, headers=data)
            get_data(res.text,i)
            db.commit()

        except:
            pass
    db.close()


if __name__ == '__main__':
    configlist = get_config()
    host = configlist[1]
    user = configlist[2]
    password = configlist[3]
    dbname = configlist[4]

    db = pymysql.connect(host=host, user=user, passwd=password, db=dbname, charset='utf8')
    curos = db.cursor()
    main()