import tkinter as tk
from tkinter import filedialog as fd
from shutil import rmtree, copytree
import pymupdf
from PyPDF2 import PdfWriter, PdfReader
from os import chdir, rename, listdir, path
from glob import glob as glob
from re import search

# Create a GUI app
app = tk.Tk()
app.geometry('500x400')

initialText = tk.Label(text="\nOlá! Bem vinda ao renomeador de PDFs da Vera!\n\nPara usar esse programa, basta escolher a pasta onde seus arquivos estão e em seguida escolher para onde vão suas versões renomeadas (e separadas).\n", wraplength=490)
initialText.pack()
# Specify the title and dimensions to app
app.title('RenomeadorV3')
app.resizable(False, False)
splitMode = tk.BooleanVar()

def secPathMemo():
    global finalPath
    finalPath = fd.askdirectory(initialdir="~/Downloads")
    secPath = tk.Label(text=f'A pasta de destino para os arquivos foi:\n{finalPath}')
    secPath.pack()
    runButton.pack()
    if(splitMode.get() == True):
        print(splitMode.get())

destinyButton = tk.Button(text='Destino', command=secPathMemo)

def pathMemo():
    global initialPath
    initialPath = fd.askdirectory(initialdir="~/Downloads")
    mainPath = tk.Label(text=f'A pasta dos arquivos não renomeados escolhida foi:\n{initialPath}')
    mainPath.pack()
    destinyButton.pack()
    if(splitMode.get() == True):
        print(splitMode.get())


splitButton = tk.Checkbutton(text= 'Separar PDFs por página', variable=splitMode)
splitButton.pack()

def renamer(folderPath):    
    failed_pdfs = []
    count = 0
    cr_regex1_0 = r'(?<=Para) ((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)'
    cr_regex1_single = r'(?<=Para \n)(\w+)|(?<=Para\n)(\w+)'
    cr_regex1_1 = r'(?<=Para\n)((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)|(?<=Para \n)((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)'
    cr_regex1_2 = r'(?<=Para\n\n)((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)'
    cr_regex1_3 = r'(?<=Para\n\n\n)((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)'
    cr_regex2 = r'(?<=R\$) (\w+,\w+)'
    cr_regex3_0 = r'(?<=Hora da transação\n)(\w+)\b\/(\w+)\b\/20(\w+)|(?<=Hora da transação \n)(\w+)\b\/(\w+)\b\/20(\w+)'
    cr_regex3_1 = r'(?<=Hora da transação\n\n)(\w+)\b\/(\w+)\b\/20(\w+)|(?<=Hora da transação \n\n)(\w+)\b\/(\w+)\b\/20(\w+)'
    cr_regex3_2 = r'(?<=Hora da transação\n\n\n)(\w+)\b\/(\w+)\b\/20(\w+)|(?<=Hora da transação \n\n\n)(\w+)\b\/(\w+)\b\/20(\w+)'
    text = ""

    month_conversion = {
        '01': 'jan',
        '02': 'fev',
        '03': 'mar',
        '04': 'abr',
        '05': 'mai',
        '06': 'jun',
        '07': 'jul',
        '08': 'ago',
        '09': 'set',
        '10': 'out',
        '11': 'nov',
        '12': 'dez'
    }
    chdir(folderPath)
    pdf_list = glob('*.pdf')
    for pdf in pdf_list:
        with pymupdf.open(pdf) as pdf_obj:
            for page in pdf_obj:
                text += page.get_text()
        finalText1 = ''
        if search(cr_regex1_0, text) is not None:
            finalText1_1 = search(cr_regex1_0, text).group(2).strip()
            finalText1_2 = search(cr_regex1_0, text).group(5).strip()
        elif search(cr_regex1_1, text) is not None:
            if search(cr_regex1_1, text).group(2) is not None:
                finalText1_1 = search(cr_regex1_1, text).group(2).strip()
                finalText1_2 = search(cr_regex1_1, text).group(5).strip()
            elif search(cr_regex1_1, text).group(2) is None:
                if search(cr_regex1_single, text).group(1) is None:
                    finalText1_1 = search(cr_regex1_single, text).group(2)
                    finalText1_2 = ''
            elif search(cr_regex1_single, text).group(1) is not None:
                finalText1_1 = search(cr_regex1_single, text).group(1)
                finalText1_2 = ''
        elif search(cr_regex1_2, text) is not None:
            finalText1_1 = search(cr_regex1_2, text).group(2).strip()
            finalText1_2 = search(cr_regex1_2, text).group(5).strip()
        elif search(cr_regex1_3, text) is not None:
            finalText1_1 = search(cr_regex1_3, text).group(2).strip()
            finalText1_2 = search(cr_regex1_3, text).group(5).strip()

        finalText2 = ''
        if search(cr_regex2, text) is not None:
            finalText2 = search(cr_regex2, text).group(1)
        finalText3 = ''
        finalText4 = ''
        finalText5 = ''
        if search(cr_regex3_0, text) is not None:
            if search(cr_regex3_0, text).group(1) is not None:
                finalText3 = search(cr_regex3_0, text).group(1).strip()
                finalText4 = search(cr_regex3_0, text).group(2).strip()
                finalText5 = search(cr_regex3_0, text).group(3).strip()
            elif search(cr_regex3_0, text).group(1) is None:
                finalText3 = search(cr_regex3_0, text).group(4).strip()
                finalText4 = search(cr_regex3_0, text).group(5).strip()
                finalText5 = search(cr_regex3_0, text).group(6).strip()
        elif search(cr_regex3_1, text) is not None:
            if search(cr_regex3_1, text).group(1) is not None:
                finalText3 = search(cr_regex3_1, text).group(1).strip()
                finalText4 = search(cr_regex3_1, text).group(2).strip()
                finalText5 = search(cr_regex3_1, text).group(3).strip()
            elif search(cr_regex3_1, text).group(1) is None:
                finalText3 = search(cr_regex3_1, text).group(4).strip()
                finalText4 = search(cr_regex3_1, text).group(5).strip()
                finalText5 = search(cr_regex3_1, text).group(6).strip()
        elif search(cr_regex3_2, text) is not None:
            if search(cr_regex3_2, text).group(1) is not None:
                finalText3 = search(cr_regex3_2, text).group(1).strip()
                finalText4 = search(cr_regex3_2, text).group(2).strip()
                finalText5 = search(cr_regex3_2, text).group(3).strip()
            elif search(cr_regex3_2, text).group(1) is None:
                finalText3 = search(cr_regex3_2, text).group(4).strip()
                finalText4 = search(cr_regex3_2, text).group(5).strip()
                finalText5 = search(cr_regex3_2, text).group(6).strip()
        finalText4 = month_conversion.get(finalText4, "Invalid input")

        new_file_name = 'pgto '+ finalText1_1.title() + ' ' + finalText1_2.title() + ' ' + finalText2 + ' ' + finalText3 + finalText4 + finalText5 + '.pdf'
        text = ""

        try:
            rename(pdf, new_file_name)
        except WindowsError:
            count += 1
            failed_pdfs.append(str(
                count) + ' - Não foi possível renomear:[' + pdf + " ----> " + str(new_file_name) + "]")

    chdir(folderPath)
    if (len(failed_pdfs) > 0):
        with open('ARQUIVOS NÃO RENOMEADOS.txt', 'w') as f:
            for failure in failed_pdfs:
                f.writelines(failure + '\n')
    finalMessage = tk.Label(text='Os arquivos foram renomeados!')
    finalMessage.pack()

def copier(firstPath, secondPath):
    if(splitMode.get() == True):
        files = listdir(firstPath)
        i = 0
        for file in files:
            i += 1
            pdf = PdfReader(f'{firstPath}/{file}')
            for page in range(len(pdf.pages)):
                fname = 'fname'
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf.pages[page])
                output_filename = f'{secondPath}'+'/{}_page_{}.pdf'.format(fname+f'{i}', page+1)
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
                print('Created: {}'.format(output_filename))
    else:
        files = listdir(firstPath)
        if path.exists(secondPath):
            rmtree(secondPath)
            copytree(firstPath, secondPath)

def finalFunction (x,y):
    copier(x,y)
    renamer(y)


mainButton = tk.Button(text='Pasta dos arquivos', command=pathMemo)
runButton = tk.Button(text='Iniciar renomeação',
                      command=lambda: finalFunction(initialPath,finalPath))
mainButton.pack()
app.mainloop()

# For compiling use: python -m PyInstaller -F -i renamer.ico -w -n "RenomeadorV3" executableVersion.py