 -*- coding: utf-8 -*-
import db_connect


def permitValidation(id,pwd,objectList,fileName):
    
    #print("validation get started")
    caseResult = 'Pass'
    failRecord=[]
    report = []
    #run command in DB to get the execute result
    result = db_connect.exec_sql_pda(id,pwd,objectList)
    
    
    #print(report)    
    for object in objectList:
        if isinstance(result[object],int):
            report.append(object+","+str(result[object]))
            continue
        else:
             failRecord.append(object+":"+result[object])
             continue
    if len(failRecord) != 0:
        report.append(object+","+result[object])
        print('The permission validate failed, below is the failed records')
        caseResult='Failed'
        print(failRecord)
    else:
       pass
   #write the execute result to the file
    with open(fileName,'w') as f: 
        f.write('OBJECT_NM'+','+'COUNT')
        for object in objectList:
            f.write(object+','+result[object]+'\n')           
    return caseResult
    
    
if __name__ == "__main__":   
    permitValidation('siwsit','oct18oct',['RDMSTG.SERVICE_LINE','RDMSTG.SERVICE_LINE_GROUP'])
