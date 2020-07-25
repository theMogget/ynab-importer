from tkinter import filedialog
from datetime import date
import tkinter as tk
import pandas as pd
import fileconfig
import re
import os


def truncate_file(fpath, pattern, name):
    """Locate the line where the table starts and truncate the file"""
    with open(fpath, 'r') as fopen:
        lines = fopen.readlines()
        for i in range(len(lines)):
            if re.match(pattern, lines[i]):
                break
        res = [l.strip() for l in lines[i:] if l != '\n']
    with open('temp.csv', 'w') as fout:
        for l in res:
            if name=='multiplier':
                fout.write(l[:-1] + '\n')
            elif name=='livefresh':
                fout.write(l + '\n')
    return res



class file_selector(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        # Initialise radiobuttons
        self.file_format = tk.StringVar()
        self.R1 = tk.Radiobutton(self, variable=self.file_format, value='multiplier',
                          command=self.set_save_fpath)
        self.R1.grid(row=0, column=0)
        L1 = tk.Label(text='multiplier')
        L1.grid(row=0, column=1)
        self.R2 = tk.Radiobutton(self, variable=self.file_format, value='livefresh',
                          command=self.set_save_fpath)
        self.R2.grid(row=1, column=0)
        L2 = tk.Label(text='livefresh')
        L2.grid(row=1, column=1)

        # Initialise text field
        self.save_fpath = tk.StringVar(value='/Users/kai/Documents/ynab_imports/tmp.csv')
        L3 = tk.Label(text='Save path:')
        L3.grid(row=2, column=1)
        save_path_field = tk.Entry(self, textvariable=self.save_fpath, width=50)
        save_path_field.grid(row=2, column=2)

        # Initialise close button
        B1 = tk.Button(self, text='Select', command=self.close)
        B1.grid(row=3, column=1)

    def set_save_fpath(self):
        today = str(date.today()).replace('-','_')
        p = '/Users/kai/Documents/ynab_imports/%s_%s.csv' % (self.file_format.get(), today)
        self.save_fpath.set(p)

    def close(self):
        self.quit()


if __name__ == '__main__':
    
    print('Runner starting..')
    cfg = fileconfig.multiplier_dict

    # Initialise gui
    root = file_selector()
    root.mainloop()
    root.withdraw()
    filename = filedialog.askopenfilename()

    # Configurations
    cfg = fileconfig.multiplier_dict if (root.file_format.get() == 'multiplier') else fileconfig.livefresh_dict
    print('Account format: %s' % cfg['name'])
    print('Reading from  : %s' % filename)
    print('Saving to     : %s' % root.save_fpath.get())

    # Read input file and truncate
    truncated = truncate_file(filename, cfg['truncate_pattern'], cfg['name'])
    df = pd.read_csv('temp.csv')

    # Select cols and rename
    df = df[cfg['mapping'].keys()]
    data = df.rename(columns=cfg['mapping'])
    data['date'] = pd.to_datetime(data['date'], format=cfg['date_format'])
    data.to_csv(root.save_fpath.get(), index=False)
    print('All processes complete.')
