# -*- coding: utf-8 -*-
import sys, os
import pypyodbc as pypyodbc
import ctypes
import time, datetime
from decimal import Decimal
import base64

binary_data = base64.b64decode('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')




def cur_file_dir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

#c_Path = ctypes.create_string_buffer(u"CREATE_DB=.\\e.mdb General\0\0".encode('mbcs'))
#ODBC_ADD_SYS_DSN = 1
#ctypes.windll.ODBCCP32.SQLConfigDataSource(None,ODBC_ADD_SYS_DSN,"Microsoft Access Driver (*.mdb)", c_Path)


def u8_enc(v, force_str = False):
    if v == None:
        return ('')
    elif isinstance(v,unicode):
        return (v.encode('utf_8','replace'))
    elif isinstance(v, buffer):
        return ('')
    else:
        if force_str:
            return (str(v))
        else:
            return (v)





def prof_func():
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+cur_file_dir()+u'\\e.mdb', unicode_results = True)
    cur = conn.cursor()
    cur.execute(u"""select * from pypyodbc_test_data""")

    i = 0
    row = cur.fetchone()
    while row != None:
        for field in row:
            x = field
        i += 1
        if i % 5000 == 0:
            print i,
        
        row = cur.fetchone()
        
    #print conn.FetchAll()
    #Close before exit
    cur.close()
    conn.close()
    




if __name__ == "__main__":
    pypyodbc.DEBUG = 0
    DSN_list = pypyodbc.dataSources()
    print (DSN_list)
    
    if sys.platform == "win32":
        dsn_test =  'mdb'
    else:
        dsn_test =  'pg'
    user = 'tutti'
    
    pypyodbc.win_create_mdb(cur_file_dir()+u'\\灵活.mdb'.encode('mbcs'))

    conxs = [\
        ('Access',
        pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+cur_file_dir()+u'\\灵活.mdb', unicode_results = True),
        u"""create table pypyodbc_test_data (编号 integer PRIMARY KEY,产品名 text,数量 numeric,价格 float,日期 
                datetime,shijian time,riqi datetime, kong float)""",
        ),
#        ('SQLServer',
#        pypyodbc.connect('DSN=MSSQL'),
#        u"""create table pypyodbc_test_data (编号 integer PRIMARY KEY,产品名 text,数量 numeric(14,4),价格 float,日期 
#                datetime,shijian time,riqi date, kong float)""",
#        ),
#        ('MySQL',
#        pypyodbc.connect('DSN=MYSQL'),
#        u"""create table pypyodbc_test_data (编号 integer PRIMARY KEY,产品名 text,数量 numeric(14,4),价格 float,日期 
#                datetime,shijian time,riqi date, kong float)""",
#        
#        ),
#        ('PostgreSQL',
#        pypyodbc.connect('DSN=PostgreSQL35W'),
#        u"""create table pypyodbc_test_data (编号 integer PRIMARY KEY,产品名 text,数量 numeric(14,4),价格 float,日期 
#                        timestamp,shijian time,riqi date, kong float)""",
#        ),
        ]
    
    for db_desc, conn, create_table_sql in conxs:
        '''
        cur = conn.cursor()
        for row in (cur.getTypeInfo().fetchall()):
            i = 1
            for field in row:
                print i,
                print field
                i += 1
        cur = None
        '''
        
        print ' *'.join(['' for i in range(80)])
        print ' *'.join(['' for i in range(80)])

        print db_desc 
        print ' *'.join(['' for i in range(80)])
        cur = conn.cursor()
        
        
        has_table_data = cur.tables(table='pypyodbc_test_data').fetchone()
        print 'has table "pypyodbc_test_data"?' + str(has_table_data)
        
        cur.close()
        
        
        cur = conn.cursor()
        if has_table_data:
            cur.execute('Drop table pypyodbc_test_data;')


        cur.execute(create_table_sql)
        conn.commit()
        for row in cur.columns(table='data').fetchall():
            print row
        cur.close()
        
        print 'inserting...',
        start_time = time.time()
        cur = conn.cursor()
        cur.execute(u"insert into pypyodbc_test_data values(1,'pypyodbc',12.3,1234.55,?,'17:31:32','2012-12-23',NULL)", (datetime.datetime.now(),))
        longtext = u''.join([u'我在马路边，捡到一分钱。']*2)
        cur.execute("insert into pypyodbc_test_data values (?,?,?,?,?,?,?,NULL)", \
                                (2, \
                                longtext,\
                                Decimal('1233.4513'), \
                                123.44, \
                                datetime.datetime.now(), \
                                datetime.datetime.now().time(),\
                                datetime.date.today(),\
                                ))


        for i in xrange(3,3003):
            cur.executemany(u"""insert into pypyodbc_test_data values 
            (?,?,12.32311, 1234.55, ?,?,'2012-12-23',NULL)""", 
            [(i, "【巴黎圣母院】".decode('utf-8'), datetime.datetime.now(), datetime.datetime.now().time()),
            (i+100000, u"《普罗米修斯》", datetime.datetime.now(), datetime.datetime.now().time()),
            (i+200000, "〖太极张三丰〗".decode('utf-8'), datetime.datetime.now(), datetime.datetime.now().time()),
            (i+300000, '〖!@#$$%"^&%&〗'.decode('utf-8'), datetime.datetime.now(), datetime.datetime.now().time()),
            (i+400000, "〖querty-','〗".decode('utf-8'), datetime.datetime.now(), datetime.datetime.now().time()),
            
            ]
            )
        
        print 'insert complete, total time ',
        end_time = time.time()
        print end_time-start_time
        conn.commit()
        print 'commit comlete, commit time ',
        print time.time() - end_time
        
        print time.time()

        cur.execute(u"""select * from pypyodbc_test_data""")
        print cur.description
        #Get results
        
        for row in cur.fetchmany(6):
            for field in row:
                print type(field),
                if isinstance(field, unicode):
                    print field.encode('mbcs'),
                else:
                    print field,
            print ('')
        
        #print (len(cur.fetchall()))
        
        cur.close()
        cur = conn.cursor()
        #cur.execute(u"delete from pypyodbc_test_data ".encode('mbcs'))
        
        cur.execute(u"""select * from pypyodbc_test_data""")

        #Get results
        
        for row in cur.fetchmany(6):
            for field in row:
                if isinstance(field, unicode):
                    print len(field),
                    print field.encode('mbcs'),
                else:
                    print field,
                print '|',
            print ''
        
        cur.close()
        #conn.rollback()
        cur = conn.cursor()
        print time.time()
        cur.execute(u'update pypyodbc_test_data set 数量 = ? where 数量 > 0 '.encode('mbcs'),(time.time(),))
        print cur.rowcount
        print time.time()
        conn.commit()
        for field in cur.execute(u"""select * from pypyodbc_test_data""").fetchone():
            if isinstance(field, unicode):
                print field.encode('mbcs'),
            else:
                print field,
        print ('')
        print (cur.description)
        
        start_time = time.time()
        i = 1
        row = cur.fetchone()
        while row != None:
            for field in row:
                x = field
            i += 1
            if i % 5000 == 0:
                print i,
            
            row = cur.fetchone()
        print '\n Total records retrive time:',
        print time.time() - start_time
        #print conn.FetchAll()
        #Close before exit
        cur.close()
        import cProfile
        #cProfile.run('prof_func()')

        #conn.close()
    print ('End of testing')
    time.sleep(3)
    
