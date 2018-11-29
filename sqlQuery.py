import mysql.connector
import os

cnx = mysql.connector.connect(user = 'a.schneider', password = '4u2change', database = 'dBAngelaSchneider', host = 'mysql.cs.rocky.edu')
cnx2 = mysql.connector.connect(user = 'a.schneider', password = '4u2change', database = 'dBAngelaSchneider', host = 'mysql.cs.rocky.edu')
cnx3 = mysql.connector.connect(user = 'a.schneider', password = '4u2change', database = 'dBAngelaSchneider', host = 'mysql.cs.rocky.edu')


cursor = cnx.cursor()


query = ("""SELECT NAMES.UUID, NAMES.BUSINESS_NM, NAMES.SUFFIX, NAMES.LAST_NM, NAMES.FIRST_NM,  NAMES.MIDDLE_NM, ADDRESSES.STREET, ADDRESSES.CITY, ADDRESSES.STATE_PROV, ADDRESSES.POSTAL_CODE
FROM dBAngelaSchneider.NAMES
LEFT JOIN dBAngelaSchneider.ADDRESSES
ON NAMES.UUID = ADDRESSES.UUID
""")
#ask for businesses, names, and complete addresses





def Labels():

    cursor.execute(query)

    #loop through and print all selected items
    for(UUID, BUSINESS_NM, LAST_NM, SUFFIX, FIRST_NM, MIDDLE_NM, STREET, CITY, STATE_PROV, POSTAL_CODE) in cursor:

        addressString = '\n{} \n{} {} {}, {} \n{} \n{} {}, {}'.format(BUSINESS_NM, LAST_NM, SUFFIX, FIRST_NM, MIDDLE_NM, STREET, CITY, STATE_PROV, POSTAL_CODE)

        phone_cursor = cnx2.cursor()

        phone_cursor.execute("""SELECT PHONE_NUMBERS.OWNER_UUID, PHONE_NUMBERS.PHONE_NUMBER
FROM dBAngelaSchneider.PHONE_NUMBERS
WHERE PHONE_NUMBERS.OWNER_UUID = '%s'""" % (UUID))

        phoneString = ''

        for(UUID, PHONE_NUMBER) in phone_cursor:

            phoneString+= '\n{}'.format(PHONE_NUMBER)

        phone_cursor.close()

        email_cursor = cnx3.cursor()

        email_cursor.execute("""SELECT EMAILS.UUID, EMAILS.EMAIL_ADDRESS
FROM dBAngelaSchneider.EMAILS
WHERE EMAILS.UUID = '%s'""" % (UUID))

        emailString = ''

        for(UUID, EMAIL_ADDRESS) in email_cursor:

            emailString += '\n{}'.format(EMAIL_ADDRESS)       

        email_cursor.close()

        print(addressString, phoneString, emailString)


class MailingLabels:
    '''iterator that yields mailing labels'''

    #current instance of class
    def __init__(self):
        self.Labels = Labels()

    def __iter__(self):
        self.currentIndex = -1
        return self

    def __next__(self):
        self.currentIndex += 1
        curIdx = self.currentIndex

        if curIdx >= len(self.Labels):
            raise StopIterations

         lbl = self.Labels[self.currentIndex]
         return lbl

for n in MailingLabels():
    print(n + os.linesep)



cursor.close()
cnx.close()
cnx2.close()
cnx3.close()
