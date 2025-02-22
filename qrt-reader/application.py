import pdfplumber
import PIL.ImageTk
import PIL.Image
import tkinter as tk
from tkinter import ttk
from parameters import Parameters
from filemanager import FileManager
from parser import QRTParser
from database.database import Database

class DisplayWindow(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pdf = None

        self.page_navigator = ttk.Frame(self, style='TFrame', padding=10)
        self.page_navigator.pack(side='top')

        self.navigate_left = ttk.Button(self.page_navigator, text='<')
        self.navigate_left.pack(side='left')
        self.navigate_left.bind('<Button-1>', self.decrement_page)

        self.page_number = tk.StringVar(parent)
        self.page_number.set('1')
        self.page_number.trace_add('write', self.display_page)

        self.page_entry = ttk.Entry(self.page_navigator, justify='center', width=3, textvariable=self.page_number).pack(side='left', fill=None)

        self.navigate_right = ttk.Button(self.page_navigator, text='>')
        self.navigate_right.pack(side='left')
        self.navigate_right.bind('<Button-1>', self.increment_page)

        self.page_view = ttk.Frame(self, style='TFrame', padding=10)
        self.page_view.pack(side='top', fill='both', expand=True)

        dummy_img = PIL.ImageTk.PhotoImage(PIL.Image.open('resources/img/pixel.png'))
        self.page_canvas = tk.Canvas(self.page_view)
        self.page_canvas.image = dummy_img
        self.canvas_image = self.page_canvas.create_image((0, 0), anchor='nw', image=dummy_img)
        self.canvas_bbox = self.page_canvas.create_rectangle((0, 0, 0, 0), state='hidden')
        self.page_canvas.pack(expand=True, fill='both')

    def decrement_page(self, event):
        if int(self.page_number.get()) > 1:
            self.page_number.set(str(int(self.page_number.get())-1))
            self.display_page()

    def increment_page(self, event):
        if hasattr(self, 'pdf') and (self.pdf != None):
            if int(self.page_number.get()) < len(self.pdf.pages):
                self.page_number.set(str(int(self.page_number.get())+1))
                self.display_page()

    def display_page(self, *args, **kwargs):
        if self.pdf != None:
            try: 
                pdf_img = self.pdf.pages[int(self.page_number.get())-1].to_image()
                img_tk = PIL.ImageTk.PhotoImage(pdf_img.original)
                self.page_canvas.image = img_tk
                self.page_canvas.config(width=img_tk.width(), height=img_tk.height())
                self.page_canvas.itemconfig(self.canvas_image, image=img_tk)
            except ValueError:
                pass
            self.bbox = {'x0': 0, 'y0': 0, 'x1':0, 'y1': 0}
            self.page_canvas.itemconfig(self.canvas_bbox, state='hidden')
            self.page_canvas.bind('<Button-1>', self.start_bbox)
            self.page_canvas.bind('<B1-Motion>', self.draw_bbox)
            self.page_canvas.bind('<ButtonRelease-1>', self.finish_bbox)

    def start_bbox(self, event):
        self.parent.processwindow.analyze_button.pack_forget()
        self.bbox['x0'] = event.x
        self.bbox['y0'] = event.y
        self.bbox['x1'] = event.x
        self.bbox['y1'] = event.y
        self.page_canvas.coords(self.canvas_bbox, (self.bbox['x0'], self.bbox['y0'], self.bbox['x1'], self.bbox['y1'],))
        self.page_canvas.itemconfig(self.canvas_bbox, state='normal')

    def draw_bbox(self, event):
        self.bbox['x1'] = event.x
        self.bbox['y1'] = event.y
        self.page_canvas.coords(self.canvas_bbox, (self.bbox['x0'], self.bbox['y0'], self.bbox['x1'], self.bbox['y1'],))

    def finish_bbox(self, event):
        self.parent.processwindow.analyze_button.pack(padx=5, pady=5)

class ProcessWindow(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.filemanager = FileManager()
        self.parameters = Parameters()
        self.database = Database()
        
        self.company = ttk.Menubutton(self, text='Select company', width=20, style='TMenubutton')
        self.selected_company = tk.StringVar(parent, None)
        self.selected_company.trace_add('write', self.company_changed)

        companymenu = tk.Menu(self.company)
        for company in list(Parameters.FILENAME_MASKS):
            companymenu.add_radiobutton(label=company, value=company, variable=self.selected_company)
        self.company['menu'] = companymenu
        self.company.pack(padx=5, pady=5)

        self.year = ttk.Menubutton(self, text='Select year', width=20, style='TMenubutton')
        self.selected_year = tk.StringVar(parent, None)
        self.selected_year.trace_add('write', self.year_changed)

        yearmenu = tk.Menu(self.year)
        for year in ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']:
            yearmenu.add_radiobutton(label=year, value=year, variable=self.selected_year)
        self.year['menu'] = yearmenu
        self.year.pack(padx=5, pady=5)

        self.loadreport_button = ttk.Button(self, text='Load SFCR report', style='outline.TButton')
        self.loadreport_button.pack(padx=5, pady=5)
        self.loadreport_button.bind('<Button-1>', self.loadReport)

        self.bbox_frame = ttk.Frame(self, style='secondary.TFrame')

        self.separator1 = ttk.Separator(self.bbox_frame, orient='horizontal', style='info.Horizontal.Separator')

        self.bboxexplanation = ttk.Label(self.bbox_frame, text='1. Select QRT model below\n2. Navigate to the correct page\n3. Draw a rectangle around the table\n4. Click on Analyze button', style='inverse.secondary.TLabel')
        self.qrt = ttk.Menubutton(self.bbox_frame, text='Select QRT', width=20, style='TMenubutton')
        self.selected_qrt = tk.StringVar(parent, None)
        self.selected_qrt.trace_add('write', self.QRTChanged)
        qrtmenu = tk.Menu(self.qrt)
        for QRT in self.parameters.AVAILABLE_QRTS:
            qrtmenu.add_radiobutton(label=QRT, value=QRT, variable=self.selected_qrt)
        self.qrt['menu'] = qrtmenu

        self.analyze_button = ttk.Button(self.bbox_frame, text='Analyze...', style='outline.TButton')
        self.analyze_button.bind('<Button-1>', lambda event: self.analyzeTable(event, self.parent.displaywindow.pdf, int(self.parent.displaywindow.page_number.get())-1, self.parent.displaywindow.bbox))

    def loadReport(self, event):
        self.update_statusbar('Loading report...')
        try:
            path = self.filemanager.getSFCRPath(self.selected_company.get(), self.selected_year.get())
            self.parent.displaywindow.pdf = pdfplumber.open(path)
            self.parent.displaywindow.display_page()
            self.update_statusbar('Ready...')
            self.bbox_frame.pack(side='top')
            self.separator1.pack(padx=5, pady=20, fill='x')
            self.bboxexplanation.pack(padx=5, pady=5)
            self.qrt.pack(padx=5, pady=5)
        except FileNotFoundError as e:
            self.update_statusbar(str(e) + '.   Ready...')

    def analyzeTable(self, event, pdf, pagenumber, bbox):
        self.update_statusbar('Ready...')
        self.parent.displaywindow.page_canvas.itemconfig(self.parent.displaywindow.canvas_bbox, state="hidden")
        try:
            cropped_page = pdf.pages[pagenumber].crop((bbox['x0'], bbox['y0'], bbox['x1'], bbox['y1']))
        except ValueError:
            self.update_statusbar('Please draw a rectangle on the page first.   Ready...')
            return

        try:
            table = cropped_page.find_table(self.parameters.company_tablestrategy(self.selected_company.get()))
            strategy = self.parameters.company_cellstrategy(self.selected_company.get(), table.bbox, cropped_page, self.selected_qrt.get())
        except Exception as e:
            if table == None:
                self.update_statusbar('No table found in selected area.   Ready...')
            else:
                self.update_statusbar(str(e) + '.   Ready...')
            return

        analyzed_img = cropped_page.to_image().debug_tablefinder(table_settings=strategy)
        analyzed_tk = PIL.ImageTk.PhotoImage(analyzed_img.annotated)
        
        parser = QRTParser()
        if self.selected_qrt.get() in self.parameters.AVAILABLE_QRTS:
            try:
                match self.selected_qrt.get():
                    case 'S.05.01.02.01 (part 1)':
                        qrt_output = parser.s05010201_part1(self.selected_company.get(), self.selected_year.get(), cropped_page.extract_table(strategy))
                        self.database.update_s05010201(qrt_output)
                    case 'S.05.01.02.01 (part 2)':
                        qrt_output = parser.s05010201_part2(self.selected_company.get(), self.selected_year.get(), cropped_page.extract_table(strategy))
                        self.database.update_s05010201(qrt_output)
                    case 'S.05.01.02.01 (single table)':
                        qrt_output = parser.s05010201_part1(self.selected_company.get(), self.selected_year.get(), cropped_page.extract_table(strategy))
                        self.database.update_s05010201(qrt_output)
                    case 'S.17.01.02.01 (part 1)':
                        qrt_output = parser.s17010201_part1(self.selected_company.get(), self.selected_year.get(), cropped_page.extract_table(strategy))
                        self.database.update_s17010201(qrt_output)
                    case 'S.17.01.02.01 (part 2)':
                        qrt_output = parser.s17010201_part2(self.selected_company.get(), self.selected_year.get(), cropped_page.extract_table(strategy))
                        self.database.update_s17010201(qrt_output)
                    case 'S.17.01.02.01 (single table)':
                        qrt_output = parser.s17010201_part1(self.selected_company.get(), self.selected_year.get(), cropped_page.extract_table(strategy))
                        self.database.update_s17010201(qrt_output)
                    case _:
                        self.update_statusbar('No parser for selected QRT.   Ready...')
            except Exception as e:
                self.update_statusbar(str(e) + '.   Ready...')
                return
            self.parent.displaywindow.page_canvas.image = analyzed_tk
            self.parent.displaywindow.page_canvas.config(width=analyzed_tk.width(), height=analyzed_tk.height())
            self.parent.displaywindow.page_canvas.itemconfig(self.parent.displaywindow.canvas_image, image=analyzed_tk)
        else:
            self.update_statusbar('Select QRT format to be analyzed.   Ready...')

    def company_changed(self, var, index, mode):
        if self.selected_company.get()!=None:
            self.company.configure(text=self.selected_company.get())

    def year_changed(self, var, index, mode):
        if self.selected_year.get()!=None:
            self.year.configure(text=self.selected_year.get())

    def QRTChanged(self, var, index, mode):
        if self.selected_qrt != None:
            self.qrt.configure(text=self.selected_qrt.get())

    def update_statusbar(self, message):
        self.parent.parent.statusbar.statustext.configure(text=message)


        