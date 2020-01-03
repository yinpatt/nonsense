import pandas as pd
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import os

def get_table(ytd, td):
    df1 = pd.read_csv('main_df_{}.csv'.format(ytd))
    df2 = pd.read_csv('main_df_{}.csv'.format(td))
    df1['pid'] = df1.ccass_id+'_'+df1.taker.astype(str)
    df2['pid'] = df2.ccass_id+'_'+df2.taker.astype(str)
    df = pd.merge(df1, df2, on = 'pid', how = 'right')

    df['stake_changes'] = df.stake_y - df.stake_x
    df['holding_changes'] = df.holding_y - df.holding_x
    df.stake_changes.sort_values()
    col = ['taker_x','ccass_id_x','name_x','holding_y','holding_changes','stake_y','stake_changes']
    df = df[col].sort_values('stake_changes', ascending = False).dropna()
    df.columns = ['Ticker','Participant ID','CCASS Participant','Shareholding','Shareholding Change','Stake%','Stake% Change']
    df['Stake%'] = df['Stake%']/100
    df['Stake% Change'] = df['Stake% Change']/100
    
    return df


def write_xlsx(td, df_all):
    df_top = df_all.head(50)
    df_bottom = df_all.tail(50).sort_values('Stake% Change', ascending = True)

    writer = pd.ExcelWriter(r'{}.xlsx'.format(td), engine='xlsxwriter')

    df_top.to_excel(writer,'top50', index=False)
    df_bottom.to_excel(writer,'btm50', index=False)
    workbook  = writer.book

    # Add some cell formats.
    format1 = workbook.add_format({'num_format': '#,##0'})
    format2 = workbook.add_format({'num_format': '0%'})


    ###### Working on top 50
    worksheet = writer.sheets['top50']

    # Set the column width and format.
    worksheet.set_column('A:A', 8, None)
    worksheet.set_column('B:B', 15, None)
    worksheet.set_column('C:C', 40, None)

    worksheet.set_column('D:D', 18, format1)
    worksheet.set_column('E:E', 18, format1)

    # Set the format but not the column width.
    worksheet.set_column('F:F', None, format2)
    worksheet.set_column('G:G', 18, format2)


    ###### Working on btm 50
    worksheet = writer.sheets['btm50']

    # Set the column width and format.
    worksheet.set_column('A:A', 8, None)
    worksheet.set_column('B:B', 15, None)
    worksheet.set_column('C:C', 40, None)

    worksheet.set_column('D:D', 18, format1)
    worksheet.set_column('E:E', 18, format1)

    # Set the format but not the column width.
    worksheet.set_column('F:F', None, format2)
    worksheet.set_column('G:G', 18, format2)

    writer.save()
    


def send_email(td, fromaddr,toaddr, pw):

    #fromaddr = "raysquant.operation@gmail.com"
    #toaddr = "yinpatt@gmail.com, raysquant.operation@gmail.com"

    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # storing the senders email address 
    msg['From'] = fromaddr 

    # storing the receivers email address 
    msg['To'] = toaddr 

    # storing the subject 
    msg['Subject'] = "Daily CCASS ({})".format(td)

    # string to store the body of the mail 
    body = "Please find attached the CCASS files. This email is generated automatically."

    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    # open the file to be sent 
    filename = "test.xlsx"
    attachment = open("{}.xlsx".format(td), "rb") 

    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 

    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 

    # encode into base64 
    encoders.encode_base64(p) 

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 

    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 

    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login(fromaddr, pw) 

    # Converts the Multipart msg into a string 
    text = msg.as_string() 

    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 

    # terminating the session 
    s.quit() 
