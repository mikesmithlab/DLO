from docx import Document
import dateutil.parser
import datetime





def parse_date(datestring):
    return dateutil.parser.parse(datestring, dayfirst=True)

def process_docx(filename='test.docx', signature='signature.png', filepath ='C:\\Users\\ppzmis\\OneDrive - The University of Nottingham\\Documents\\DLO\\'):
    auto_process=True
    doc = Document(filepath + 'Extensions_to_approve\\' + filename)

    request = {
        'name':doc.tables[0].cell(0,1).text,
        'id': doc.tables[0].cell(1,1).text,
        'module': doc.tables[1].cell(1,0).text,
        'original_deadline' : parse_date(doc.tables[1].cell(1,2).text),
        'new_deadline' : parse_date(doc.tables[1].cell(1,3).text),
        }
    request['date_diff'] = (request['new_deadline']-request['original_deadline']).days

    if request['date_diff'] > 7:
        auto_process=False
    if 'PHYS4' in request['module']:
        auto_process=False

    if auto_process:
        doc.tables[1].cell(1,4).paragraphs[0].text=''
        doc.tables[1].cell(1,4).paragraphs[0].add_run().add_picture(filepath+signature)

        today = str(datetime.date.today().strftime("%d/%m/%Y"))

        for paragraph in doc.paragraphs:
            if 'Staff Signature:' in paragraph.text:
                paragraph.text = ''
                paragraph.add_run('Staff Signature:').bold = True
                paragraph.add_run('..........')
                run2=paragraph.add_run()
                run2.add_picture(filepath+signature)
                paragraph.add_run('................')
                paragraph.add_run('Staff name:').bold = True
                paragraph.add_run('........Mike Smith...........')
                paragraph.add_run('Date:').bold = True
                paragraph.add_run('..............' + today + '...................')

        doc.save(filepath + 'Approved_extensions\\' + str(datetime.date.today().strftime("%Y_%m_%d")) + request['name'].replace(' ','') +'.docx')
    else:
        doc.save(filepath + 'Extensions_to_approve\\manual\\' + str(datetime.date.today().strftime("%Y_%m_%d")) + request['name'].replace(' ','') +'.docx')

    return auto_process






