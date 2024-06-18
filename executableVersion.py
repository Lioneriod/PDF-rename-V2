import tkinter as tk
from tkinter import filedialog as fd
import pymupdf
from os import DirEntry, curdir, chdir, getcwd, rename
from glob import glob as glob
import re

# Create a GUI app
app = tk.Tk()
app.geometry('500x300')

initialText = tk.Label(text="\nOlá! Bem vinda ao renomeador de PDFs da Vera!\n\nPara usar esse programa, você precisa primeiro criar uma pasta e copiar para ela todos os arquivos que você deseja renomear.\n\nCUIDADOS AO USAR: \nSempre tenha salvo uma cópia dos arquivos originais em outra pasta!\n", wraplength=490)
initialText.pack()
# Specify the title and dimensions to app
app.title('Renomeador da Vera')


def pathMemo():
    global renamePath
    renamePath = fd.askdirectory(initialdir="./Downloads")
    mainPath = tk.Label(text=f'O caminho escolhido foi:\n{renamePath}')
    mainPath.pack()
    runButton.pack()


def renamer(folderPath):
    failed_pdfs = []
    count = 0
    cr_regex1_0 = r'(?<=Para) ((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)'
    cr_regex1_single = r'(?<=Para \n)(\w+)|(?<=Para\n)(\w+)'
    cr_regex1_1 = r'(?<=Para\n)((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)|(?<=Para \n)((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)'
    cr_regex1_2 = r'(?<=Para\n\n)((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)'
    cr_regex1_3 = r'(?<=Para\n\n\n)((\w+)|\b\b.*).*(?:\n.*){0}.*(|\b(\w+)\b.*).*(?:\n.*){0}.*(\b\w+)'
    cr_regex2_0 = r'(?<=Valor Pago R\$) (\w+,\w+)'
    cr_regex2_1 = r'(?<=Valor Pago\n\bR\$) (\w+,\w+)'
    cr_regex2_2 = r'(?<=Valor Pago\n\n\bR\$)\D(\w+,\w+)'
    cr_regex2_3 = r'(?<=Valor Pago\n\n\n\bR\$)\D(\w+,\w+)'
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

    get_curr = getcwd()
    chdir(folderPath)

    pdf_list = glob('*.pdf')

    for pdf in pdf_list:
        with pymupdf.open(pdf) as pdf_obj:
            for page in pdf_obj:
                text += page.get_text()
        finalText1 = ''
        if re.search(cr_regex1_0, text) is not None:
            finalText1_1 = re.search(cr_regex1_0, text).group(2).strip()
            finalText1_2 = re.search(cr_regex1_0, text).group(5).strip()
        elif re.search(cr_regex1_1, text) is not None:
            if re.search(cr_regex1_1, text).group(2) is not None:
                finalText1_1 = re.search(cr_regex1_1, text).group(2).strip()
                finalText1_2 = re.search(cr_regex1_1, text).group(5).strip()
            elif re.search(cr_regex1_1, text).group(2) is None:
                if re.search(cr_regex1_single, text).group(1) is None:
                    finalText1_1 = re.search(cr_regex1_single, text).group(2)
                    finalText1_2 = ''
            elif re.search(cr_regex1_single, text).group(1) is not None:
                finalText1_1 = re.search(cr_regex1_single, text).group(1)
                finalText1_2 = ''
        elif re.search(cr_regex1_2, text) is not None:
            finalText1_1 = re.search(cr_regex1_2, text).group(2).strip()
            finalText1_2 = re.search(cr_regex1_2, text).group(5).strip()
        elif re.search(cr_regex1_3, text) is not None:
            finalText1_1 = re.search(cr_regex1_3, text).group(2).strip()
            finalText1_2 = re.search(cr_regex1_3, text).group(5).strip()

        finalText2 = ''
        if re.search(cr_regex2_0, text) is not None:
            finalText2 = re.search(cr_regex2_0, text).group(1).strip()
        elif re.search(cr_regex2_1, text) is not None:
            finalText2 = re.search(cr_regex2_1, text).group(1).strip()
        elif re.search(cr_regex2_2, text) is not None:
            finalText2 = re.search(cr_regex2_2, text)
        elif re.search(cr_regex2_3, text) is not None:
            finalText2 = re.search(cr_regex2_3, text)

        finalText3 = ''
        finalText4 = ''
        finalText5 = ''
        if re.search(cr_regex3_0, text) is not None:
            if re.search(cr_regex3_0, text).group(1) is not None:
                finalText3 = re.search(cr_regex3_0, text).group(1).strip()
                finalText4 = re.search(cr_regex3_0, text).group(2).strip()
                finalText5 = re.search(cr_regex3_0, text).group(3).strip()
            elif re.search(cr_regex3_0, text).group(1) is None:
                finalText3 = re.search(cr_regex3_0, text).group(4).strip()
                finalText4 = re.search(cr_regex3_0, text).group(5).strip()
                finalText5 = re.search(cr_regex3_0, text).group(6).strip()
        elif re.search(cr_regex3_1, text) is not None:
            if re.search(cr_regex3_1, text).group(1) is not None:
                finalText3 = re.search(cr_regex3_1, text).group(1).strip()
                finalText4 = re.search(cr_regex3_1, text).group(2).strip()
                finalText5 = re.search(cr_regex3_1, text).group(3).strip()
            elif re.search(cr_regex3_1, text).group(1) is None:
                finalText3 = re.search(cr_regex3_1, text).group(4).strip()
                finalText4 = re.search(cr_regex3_1, text).group(5).strip()
                finalText5 = re.search(cr_regex3_1, text).group(6).strip()
        elif re.search(cr_regex3_2, text) is not None:
            if re.search(cr_regex3_2, text).group(1) is not None:
                finalText3 = re.search(cr_regex3_2, text).group(1).strip()
                finalText4 = re.search(cr_regex3_2, text).group(2).strip()
                finalText5 = re.search(cr_regex3_2, text).group(3).strip()
            elif re.search(cr_regex3_2, text).group(1) is None:
                finalText3 = re.search(cr_regex3_2, text).group(4).strip()
                finalText4 = re.search(cr_regex3_2, text).group(5).strip()
                finalText5 = re.search(cr_regex3_2, text).group(6).strip()
        finalText4 = month_conversion.get(finalText4, "Invalid input")

        new_file_name = 'pgto '+finalText1_1.title() + ' ' + finalText1_2.title() + \
            ' ' + finalText2 + ' ' + finalText3 + finalText4 + finalText5+'.pdf'
        text = ""

        try:
            rename(pdf, new_file_name)
        except WindowsError:
            count += 1
            failed_pdfs.append(str(
                count) + ' - FAILED TO RENAME:[' + pdf + " ----> " + str(new_file_name) + "]")

    chdir(get_curr)
    if (len(failed_pdfs) > 0):
        with open('PDF_FAILURES.txt', 'w') as f:
            for failure in failed_pdfs:
                f.writelines(failure + '\n')


# Make infinite loop for displaying app on the screen
mainButton = tk.Button(text='Pasta dos arquivos', command=pathMemo)
runButton = tk.Button(text='Iniciar renomeação',
                      command=lambda: renamer(renamePath))
mainButton.pack()

app.mainloop()

# For compiling use: python -m PyInstaller -F -i renamer.ico -w -n "RenomeadorV1" executableVersion.py
