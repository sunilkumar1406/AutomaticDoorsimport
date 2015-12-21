'''
Created on Jul 16, 2015
Version 1
@author: Sunil
'''
from Tkinter import Tk
from tkFileDialog import askopenfilename
import os, time, string, re
import codecs
from collections import Counter
import csv

def Read_file(in_file):
    Tk().withdraw()
    if in_file == 'cpp':
        filename = askopenfilename(initialdir='C:/',filetypes=[("CPP Files",".cpp"),("C Files",".c")])
        #print filename
    if in_file == 'c':
        filename = askopenfilename(initialdir='C:/',filetypes=[("C Files",".c")])
        #print filename
    if in_file == 'ctr':
        filename = askopenfilename(initialdir='C:/',filetypes=[("Ctr Files",".ctr")])
        #print filename
    #print(filename)
    InFile = codecs.open(filename, 'r')
    textline = InFile.read()
    return textline,filename

def seperate_tests_for_source_functon(in_testCpp_cont):
    try:
        pattern = re.compile('run_tests\(\)\n*\t*\s*\{\n*\t*\s*(test_.*_\d\(\d\);)', re.DOTALL)
        test_func = pattern.findall(in_testCpp_cont)


        #print test_func
        #print test_func
        test_func1 = re.finditer('(test_.*\(\d*\);)', str(test_func), re.DOTALL)
        for m in test_func1:
            #print m.group(1)
            #test_line1 = m.group(1).replace("\n", "").replace("\s", "").replace("\t", "").replace('\\n\\t','').replace('\\n','').replace('\\t','')#.split(';')
            #print test_line1
            test_line2 = re.sub(r"_\d*\s*\(\d\)\;",';',m.group(1))
            test_line2 = re.sub(r"\(\d\)\;",';',test_line2)
            test_line2 = re.sub(r"\n*",'',test_line2)
            test_line2 = re.sub(r"\s*",'',test_line2)
            test_line2 = re.sub(r"\t*",'',test_line2)
            test_line2 = test_line2.replace("\n", "").replace("\s", "").replace("\t", "").replace('\\n\\t','').replace('\\n','').replace('\\t','')#.split(';')
            test_line4 = test_line2.split(';')
            
            while '' in test_line4:
                test_line4.remove('')
            #print test_line4
            #print test_line3
            #print test_line4
            #print test_line3
            #print test_line4
        c = Counter(test_line4)
        #print c
        return c

    except IOError:
        print "ERROR:Check whether test script contains Testcases!!!"

def get_test_content(in_testCpp_cont,in_x,inget_tests):
    try:
        #print in_x,'###################',str(inget_tests)
        
            
        search = in_x + '_' + str(inget_tests)
        
        seach_res = re.findall(search+'\(int doIt\)(.*?)END_TEST\(\);', in_testCpp_cont, re.DOTALL)
        if not seach_res:
            if inget_tests == 1:
                search = in_x
                seach_res = re.findall(search+'\(int doIt\)(.*?)END_TEST\(\);', in_testCpp_cont, re.DOTALL)
            if inget_tests > 1:
                search = in_x + '_' + str(inget_tests-1)
                seach_res = re.findall(search+'\(int doIt\)(.*?)END_TEST\(\);', in_testCpp_cont, re.DOTALL) 
        print '############################################################################################################'             
        print search
        print 'Function Calls:'
        return seach_res
    except IOError:
        print "ERROR:Exception occured while geting the test content of the test cases!!!"
        return ''

def get_test_desc(in_test_cont):
    try:
        seach = re.findall('START_TEST\(\s*".*?"\,\n*\t*\s*"(.*?)\"\)\;', str(in_test_cont),re.DOTALL)
        #print seach
        seachdesc = seach[0].replace("\n", "").replace("\s", "").replace("\t", "")
        seachdesc = re.sub('"', '', seachdesc)
        seachdesc = re.sub('\s{2,}', ' ', seachdesc)
        seachdesc = re.sub(r'\s*\\n\s*', ' ', seachdesc)
        #print seachdesc
        return seachdesc
    except IOError:
        print "ERROR:occured while geting the test content of the test cases!!!"

def get_test_step_init(in_test_cont,in_testCpp_cont):
    try:
        seach = re.findall('INIT\:\s*\=*(.*)SET\:\s*\=*', str(in_test_cont),re.DOTALL)
        #print seach[0]
        seach1 = re.findall('WRITE_LOG\(\".*None\s*\=*', str(seach[0]),re.DOTALL)
        if seach1:
            #print"inside seach1"
            return 'None'
        else:
            seach2 = re.findall('CHECK_\w+\s*\(\s*(.*)\s*,\s*(.*)\)\;', str(seach[0]))
            if seach2:
                init_text1 = ''
                for i in range(len(seach2)):
                    init = str(seach2[i][0]).replace('\n', '').replace('\\n', '')
                    init_text = '\n' + str(i+1) + ')' + init + '=' + seach2[i][1]
                    init_text = re.sub('\s+','',init_text)
                    init_text1 = init_text1 + "\n" + init_text + ';'
                    #init_text1 = init_text1.replace('\n', '').replace('\\n', '')
                #print init_text1
                return init_text1
            else:
                return 'None'
    except IOError:
        print "ERROR:Exception occured while geting the test init section of the test cases!!!"

def get_test_step_set(in_test_cont,in_testCpp_cont):
    try:
        #print in_test_cont
        #print '##########################################################################'
        seach = re.findall('SET\:\s*\=*(.*)VERIFY\:\s*\=*', str(in_test_cont),re.DOTALL)
        #print seach[0]
        seach1 = re.findall('WRITE_LOG\(\".*None\s*\=*', str(seach[0]),re.DOTALL)
        if seach1:
            #print"inside seach1"
            return 'None'
        else:
            seach2 = re.findall('CHECK_\w+\s*\(\s*(.*)\s*,\s*(.*)\)\;', str(seach[0]))
            if seach2:
                set_text1 = ''
                for i in range(len(seach2)):
                    set = str(seach2[i][0]).replace('\n', '').replace('\\n', '')
                    set_text = '\n' + str(i+1) + ')' + set + '=' + seach2[i][1]
                    set_text = re.sub('\s+','',set_text)
                    set_text1 = set_text1+ "\n"  + set_text + ';'
                    #set_text1 = set_text1.replace('\n', '').replace('\\n', '')
                return set_text1
            else:
                return 'None'

    except IOError:
        print "ERROR: Exception occured while geting the test set of the test cases!!!"

def get_test_step_verify(in_test_cont,in_testCpp_cont):
    try:
        #print '##########################################################################'
        seach = re.findall('VERIFY\:\s*\=*(.*)END_CALLS\(\)', str(in_test_cont),re.DOTALL)
        #print seach[0]
        seach1 = re.findall('WRITE_LOG\(\".*None\s*\=*', str(seach[0]),re.DOTALL)
        if seach1:
            #print"inside seach1"
            return 'None'
        else:
            seach2 = re.findall('CHECK_\w+\s*\(\s*(.*)\s*,\s*(.*)\)\;', str(seach[0]))
            if seach2:
                verify_text1 = ''
                for i in range(len(seach2)):
                    verify = str(seach2[i][0]).replace('\n', '').replace('\\n', '')
                    verify_text = '\n\n' + str(i+1) + ')' + verify + '=' + seach2[i][1]
                    verify_text = re.sub('\s+','',verify_text)
                    verify_text1 = verify_text1 + "\n" + verify_text + ';'
                return verify_text1
            else:
                return 'None'
    except IOError:
        print "Error: Exception occured while geting the test set of the test cases!!!"

def get_expcalls_data(in_test_cont,in_testCpp_cont,in_x,in_i):
    try:
        #print '##########################################################################'

        seach = re.findall('EXPECTED\_CALLS\s*\n*\t*\(\s*\n*\t*"\s*\n*\t*"\s*\n*\t*\)', str(in_test_cont),re.DOTALL)
        if seach:
            #print seach
            return '',''
        else:
            seach1 = re.findall('EXPECTED\_CALLS\s*\n*\t*\(\s*\n*\t*"\{*.*\(.*\)\#\w+\}*\;*"\s*\n*\t*\)\s*\n*\t*\;', str(in_test_cont),re.DOTALL)
            if seach1:
            #seach2 = re.findall('\s*\t*\n*"\{*(.*)\(.*\)\#(.*)\}*\;*\"',seach1[0])
            #seach1 = re.findall('EXPECTED\_CALLS\s*\n*\t*\(\s*\n*\t*".*\(.*\)\#\w+\;\"\)\;', str(in_test_cont),re.DOTALL)
                seach2 = re.findall('"\s*\n*\t*\{*\d*\**\(*(.*)\(.*\)\#(.*?)\)*;*\"',seach1[0])
                check = ''
                for i in range(len(seach2)):
                    check = check + seach2[i][0] + seach2[i][1] 
                if '#' in check:
                    seach2 = re.findall('\{+(.*?)#(.*?)\}\;?',seach1[0])
                #print seach2
                #seach2 = seach2.replace('}','').replace(';','')
    
                #print seach2
                #print str(seach2)
                finalverify_function_call_text = ''
                finalexp_call_returnvalue = ''
                for i in range(len(seach2)):
                    seach16 = str(seach2[i][1]).replace('}', '').replace(';', '')
                    #seach2[i][1] = seach2[i][1].replace('}','').replace(';','')
                    #print str(seach2[i][0]),'#########################',seach16
                    seach11 = re.sub('<.*?>','',str(seach2[i][0]))
                    seach11 = re.sub('\d+\s*\*\s*\(\{*','',seach11)
                    #print seach11
                    seach3 = seach11.split('::')
                    #print seach3
                    seach4 = seach3[len(seach3)-1]
                    seach12 = re.sub('<','\<',str(seach2[i][0]))
                    seach13 = re.sub('>','\>',str(seach12))
                    seach14 = re.sub(' ','\s',str(seach13))
                    seach15 = re.sub('__','\s\s',str(seach14))
                    seach15 = re.sub('_','\_*\s*',str(seach15))
                    seach15 = re.sub('\d+\s*\*\s*\(\{*','',seach15)
                    print str(seach2[i][0])+'()#'+str(seach16)
                    #print str(seach16)

                    #print seach15
                    #exp_callcontent = re.findall('Before-Wrapper for function\s?'+str(seach4)+'\s?\*\/.*LOG\_SCRIPT\_ERROR\(.*LOG\_SCRIPT\_ERROR\(.*LOG\_SCRIPT\_ERROR', str(in_testCpp_cont),re.DOTALL)
                    exp_callcontent_wrap = re.search('Before\-Wrapper\s*for\s*function\s*'+str(seach15)+'\s*\*\/', str(in_testCpp_cont))
                    if exp_callcontent_wrap:
                        #print 'insidewrapper'
    
                        #print exp_callcontent
                        #print len(in_testCpp_cont)
                        start_index = exp_callcontent_wrap.start()
                        #Search_cont = in_testCpp_cont[start_index:len(in_testCpp_cont)]
                        exp_callcontent_wrap = re.search('Replace\-Wrapper\sfor\sfunction\s'+str(seach15)+'(.*?)LOG_SCRIPT_ERROR', str(in_testCpp_cont),re.DOTALL)
                        wrap_text =  in_testCpp_cont[start_index:exp_callcontent_wrap.end()]
                        #print wrap_text
                        wrap_text_instance = re.findall('IF_INSTANCE\("'+str(seach16)+'"\)\s*(.*?)}', wrap_text,re.DOTALL)
                        wrap_text_actual = ''.join(wrap_text_instance)
                        #print wrap_text_instance
                        #print wrap_text_actual
                        wrap_text_checks = re.findall('CHECK_\w+\s*\(\s*(.*)\s*,\s*(.*)\)\;', wrap_text_actual)
                        if wrap_text_checks:
                            set_text1 = ''
                            for x in range(len(wrap_text_checks)):
                                set_text = wrap_text_checks[x][0] + '=' + wrap_text_checks[x][1]
                                set_text = re.sub('\s+','',set_text)
                                set_text1 = set_text1 + set_text + ';'
                            verify_function_call_text_wrap = str(i+1) + ')' + str(seach4) + '() ' + 'with parameters ' + set_text1
    
                        else:
                            verify_function_call_text_wrap = str(i+1) + ')' + str(seach4) +'() '
                        finalverify_function_call_text = finalverify_function_call_text + verify_function_call_text_wrap + ' '
    
                        wrap_text_return = re.findall('\s*(.*)\s*=\s*(.*)\s*\;', wrap_text_actual)
                        if wrap_text_return:
                            for z in range(len(wrap_text_return)):
                                return_text = 'Return Value[ '+wrap_text_return[z][0] + '] of '+ str(seach4) + '()'  + 'is set to ' + wrap_text_return[z][1] + ';'
                            exp_call_returnvalue = return_text + ' '
                        else:
                            exp_call_returnvalue = ''
                        finalexp_call_returnvalue = finalexp_call_returnvalue + exp_call_returnvalue + ''
                        #print wrap_text
    #                    for i in range(1,4):
    #                        wrap_end_log = re.search('LOG\_SCRIPT\_ERROR\(\"', str(Search_cont))
    #                        Search_cont  = in_testCpp_cont[wrap_end_log.start():len(in_testCpp_cont)]
    #                    wrap_cont = in_testCpp_cont[start_index:wrap_end_log.start()]
    #                    print wrap_cont
                    else:
                        #print str(seach4)
                        exp_callcontent = re.search('(Stub|Isolate)\sfor\sfunction\s'+str(seach15)+'(.*?)LOG_SCRIPT_ERROR', str(in_testCpp_cont), re.DOTALL)
                        if exp_callcontent:
                            stub_text = in_testCpp_cont[exp_callcontent.start():exp_callcontent.end()]
                            stub_text_instance = re.findall('IF_INSTANCE\("'+str(seach16)+'"\)\s*(.*?)}', stub_text,re.DOTALL)
                            stub_text_actual = ''.join(stub_text_instance)
                            wrap_text_checks = re.findall('CHECK_\w+\s*\(\s*(.*)\s*,\s*(.*)\)\;', stub_text_actual)
                            if wrap_text_checks:
                                set_text1 = ''
                                verify_function_call_text_stub = ''
                                for x in range(len(wrap_text_checks)):
                                    set_text =  wrap_text_checks[x][0] + '=' + wrap_text_checks[x][1]
                                    set_text = re.sub('\s+','',set_text)
                                    set_text1 = set_text1 + set_text + ' '
                                verify_function_call_text_stub = str(i+1) + ')' + str(seach4) +'() '+ 'with parameters ' + set_text + ';'
                            else :
                                verify_function_call_text_stub = str(i+1) + ')' + str(seach4) +'() '
                            finalverify_function_call_text = finalverify_function_call_text + verify_function_call_text_stub + ' '
    
                            wrap_text_return = re.findall('\s*(.*)\s*=\s*(.*)\s*\;', stub_text_actual)
                            if wrap_text_return:
                                for z in range(len(wrap_text_return)):
                                    return_text = 'Return Value[ '+wrap_text_return[z][0] + '] of '+ str(seach4) + '()'  + 'is set to ' + wrap_text_return[z][1] + ';'
                                exp_call_returnvalue_stub = return_text + ' '
                            else:
                                exp_call_returnvalue_stub = ''
                            finalexp_call_returnvalue = finalexp_call_returnvalue + exp_call_returnvalue_stub + ''
    
                        else:
                            print "ERROR:Stub/wrap for function call doesnt exist, Please check and write manually for the functioncall %s()" %seach4
                return finalexp_call_returnvalue,finalverify_function_call_text
            else:
                print "Error:: Expected calls text cannot be parsed for the test case %s_%d" %(in_x,in_i)
                return '',''
                    #print exp_callcontent
            #print str(seach2[0])
            #exp_callcontent = in_testCpp_cont.find('REGISTER_CALL("'+str(seach2[0][0]))

            #print exp_callcontent



        #seach1 = re.findall('WRITE_LOG\(\".*None\s*\=*', str(seach[0]),re.DOTALL)

    except IOError:
        print "ERROR:Exception occured while geting the test set of the test cases!!!"



if __name__ == "__main__":

    #print "choose the ctr file"
    #Ctr_cont = Read_file('ctr')
    print "choose the test file"
    testCpp_cont,file_path = Read_file('cpp')
    test_author = raw_input('If you like to enter TestScript Author name,Please enter the name or press enter key to enter the author name manually in doors:')
    test_reviewer = raw_input('If you like to enter TestScript Reviewer name,Please enter the name or press enter key to enter the reviewer name manually in doors:')
    print 'Creating Doors import for below testcases, Please wait'
    file_path1 = file_path.split("/")
    filepath2 = str(file_path1[len(file_path1)-1])
    filepath3 = filepath2.replace('.cpp', '').replace('.c','') 
    file_directory = os.path.dirname(file_path)
    get_tests=seperate_tests_for_source_functon(testCpp_cont)
    #print get_tests
    #print get_tests
    set_content = ''
    for x in get_tests:
        data = ['Object Text','Test Description','Test Steps','Test Priority','Test Environment','Test Script','Test Type','Test Script Author','Test Specification Method','Test Script Review Status','Test Script Reviewer','Test Script Review Findings','Test Script Review Response','Test Status','Test Design Author','Test Design Review Status','Test Design Reviewer','Test Design Review Findings','Test Script']
        #print x
        try:           
            resul_folder = "C:/Doors/%s/" %filepath3
            if not os.path.exists( resul_folder ) :
                os.makedirs( resul_folder )
            csvpath = os.path.join(resul_folder, 'Import-%s.csv' % x)
            file = open(csvpath,"w")
            out = csv.writer(file,delimiter=',',lineterminator='\n',quoting=csv.QUOTE_ALL)
            out.writerow(data)
        except IOError:
            print "ERROR:Creating CSV files created problem!!!"
        #print x

        for i in range(1,get_tests[x]+1):
            #print i,get_tests[x]+1
            test_cont=get_test_content(testCpp_cont,x,i)
            if test_cont != []:
                
                #print test_cont
                test_desc = get_test_desc(test_cont[0])
                #print test_desc
                test_step_init = get_test_step_init(test_cont[0],testCpp_cont)
                #print test_step_init
                test_step_set = get_test_step_set(test_cont[0],testCpp_cont)
                #print test_step_set
                test_step_verify = get_test_step_verify(test_cont[0],testCpp_cont)
                #print test_step_verify
                expcalls_setdata,expcalls_verifydata = get_expcalls_data(test_cont[0],testCpp_cont,x,i)
                if expcalls_setdata=='':
                   expcalls_setdata = 'None'
                if expcalls_verifydata=='':
                   expcalls_verifydata = 'None'
                set_data = 'INIT:' +  test_step_init  +'\n\n' +'SET:' + test_step_set + '\n'+ 'Set from Stub/Wrap:'+'\n'+expcalls_setdata + '\n\n' +'VERIFY:'+ test_step_verify + '\n'+'Function call Sequence:' + '\n'+expcalls_verifydata
                test_data = [str(x)+'_'+str(i),test_desc,set_data,'std','cantata++','','',test_author,'','implementation_reviewed',test_reviewer,'No Review Comments','','',test_author,'specification_reviewed',test_reviewer,'No Review Comments',filepath2]
                out.writerow(test_data)
            else:
                print 'Error : Not able to get test content for the search %s, please check the search test is correct!!!' %x  
    file.close()          
    os.system('pause')
