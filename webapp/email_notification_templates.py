'''
Created on Mar 5, 2020

@author: fsells
'''
from webapp.constants import *

TemplateLookup = dict()
TemplateLookup[ADMISSION]='''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                            <h3>Census Notification: {action}</h3>
                            <span style="color:blue;">Level of Care: </span>{newloc}<br>
                            <span style="color:blue;">Name: </span>{firstname} {lastname}<br>
                            <span style="color:blue;">Admission Date: </span>{date}<br>
                            <span style="color:blue;">Admission Time: </span>{time}<br>
                            <span style="color:blue;">Room: </span>{newbed}<br>
                            <span style="color:blue;">Level of Care: </span>{newloc}<br>
                            <span style="color:blue;">Admission From: </span>{admitfrom}<br>
                            <span style="color:blue;">Data Entry By: </span>{user}<br><br><br><br>'''

TemplateLookup[RETURN_FROM_HOSPITAL]='''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                            <h3>Census Notification: {action}</h3>
                            <span style="color:blue;">Level of Care: </span>{newloc}<br>
                            <span style="color:blue;">Name: </span>{firstname} {lastname}<br>
                            <span style="color:blue;">Transfer Date: </span>{date}<br>
                            <span style="color:blue;">Transfer Time: </span>{time}<br>
                            <span style="color:blue;">Room: </span>{newbed}<br>
                            <span style="color:blue;">Transfer From: </span>{admitfrom}<br>
                            <span style="color:blue;">Data Entry By: </span>{user}<br><br><br><br>'''

TemplateLookup[RETURN_FROM_LEAVE_OF_ABSENCE]='''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                            <h3>Census Notification: {action}</h3>
                            <span style="color:blue;">Level of Care: </span>{newloc}<br>
                            <span style="color:blue;">Name: </span>{firstname} {lastname}<br>
                            <span style="color:blue;">Return Date: </span>{date}<br>
                            <span style="color:blue;">Return Time: </span>{time}<br>
                            <span style="color:blue;">Room: </span>{newbed}<br>
                            <span style="color:blue;">Returned From: </span>{admitfrom}<br>
                            <span style="color:blue;">Data Entry By: </span>{user}<br><br><br><br>'''


TemplateLookup[OUT_TO_HOSPITAL] = '''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                                <h3>Census Notification: {action}</h3>
                                <span style="color:blue;">Prior Level of Care: </span>{oldloc}<br>
                                <span style="color:blue;">Name: </span>{firstname} {lastname}<br>
                                <span style="color:blue;">Transfer Date: </span>{date}<br>
                                <span style="color:blue;">Transfer Time: </span>{time}<br>
                                <span style="color:blue;">From Room: </span>{oldbed}<br>
                                <span style="color:blue;">Transfer to: </span>{dischargeto}<br>
                                <span style="color:blue;">Data Entry By: </span>{user}<br><br><br><br>'''
                            
TemplateLookup[OUT_TO_LEAVE_OF_ABSENCE] = '''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                                <h3>Census Notification: {action}</h3>
                                <span style="color:blue;">Prior Level of Care: </span>{oldloc}<br>
                                <span style="color:blue;">Name: </span>{firstname} {lastname}<br>
                                <span style="color:blue;">Transfer Date: </span>{date}<br>
                                <span style="color:blue;">Transfer Time: </span>{time}<br>
                                <span style="color:blue;">Prior Room: </span>{oldbed}<br>
                                <span style="color:blue;">Transfer to: </span>{dischargeto}<br>
                                <span style="color:blue;">Data Entry By: </span>{user}<br><br><br><br>'''
#check oldloc required?
TemplateLookup[ROOM_CHANGE] = '''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                                <h3>Census Notification: {action}</h3>
                                <span style="color:blue;">Name: </span>{firstname} {lastname}<br>
                                <span style="color:blue;">Transfer Date: </span>{date}<br>
                                <span style="color:blue;">Transfer Time: </span>{time}<br>
                                <span style="color:blue;">Transfer From </span>{oldbed}<br>
                                <span style="color:blue;">Transfer to: </span>{newbed}<br>
                                <span style="color:blue;">Prior Level of Care: </span>{oldloc} <br>
                                <span style="color:blue;">Change Level of Care to: </span>{newloc}<br>
                                <span style="color:blue;">Data Entry By: </span>{user}<br><br><br><br>'''
                                
TemplateLookup[DISCHARGE] = '''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                                <h3>Census Notification: {action}</h3>
                                <span style="color:blue;">Prior Level of Care: </span>{oldloc}<br>
                                <span style="color:blue;">Name: </span>{firstname} {lastname}<br>
                                <span style="color:blue;">Discharge Date: </span>{date}<br>
                                <span style="color:blue;">Discharge Time: </span>{time}<br>
                                <span style="color:blue;">Prior Room </span>{oldbed}<br>
                                <span style="color:blue;">Discharge to: </span>{dischargeto}<br>
                                <span style="color:blue;">Data Entry By: </span>{user}<br><br><br><br>'''
                                
TemplateLookup[DEATH] = '''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                                <h3>Census Notification: {action}</h3>
                                <span style="color:blue;">Prior Level of Care: </span>{oldloc}<br>
                                <span style="color:blue;">Name: </span>{firstname} {lastname}<br>
                                <span style="color:blue;">Deceased Date: </span>{date}<br>
                                <span style="color:blue;">Deceased Time: </span>{time}<br>
                                <span style="color:blue;">Prior Room </span>{oldbed}<br>
                                <span style="color:blue;">Data Entry By: </span>{user}<br><br><br><br>'''        
                                
ERROR = '''<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
                                <h3 style="color:red;">Undefined Census Action: {action}</h3>
                                <span style="color:blue;">Name: </span>{firstname} {lastname}<br>
                                <span style="color:blue;">Data Entry By: </span>{user}<br><br><br><br>'''        

def get_subject_and_body(values):
    template =  TemplateLookup.get(values['action'], ERROR) #if action does not exist in lookup keys, returns ERROR template
    #timestamp = values['timestamp']
    body = template.format(**values)
    subject = 'Census Notification: {action}'.format(**values)
    return (subject, body)

