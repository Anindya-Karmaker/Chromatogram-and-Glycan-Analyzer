
#Initially based on code by Kevin Yates
#Copyrighted Anindya Karmaker 
#Contact akarmaker@ucdavis.edu or anindyakarmaker1996@gmail.com
#Feel free to modify the code here
#NOT AUTHORIZED TO PUBLISH THIS CODE ANYWHERE WITHOUT PRIOR PERMISSION

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTabWidget, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import pandas as pd
import matplotlib.pyplot as plt
import re
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from datetime import datetime
import numpy as np
# from second_window import *
from Slave import *
global ps1,ps2,ps3,ps4,ps5,ps6
import scipy.signal as signal

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)


global bug_lock,init_val,xmin_val,xmax_val,save_figure,fraction_var, UV_var, sysflow_var, preC_var, gradient_var, ph_var, conductivity_var, syspres_var, order_table, filename, data_file_load, units
init_val=0
bug_lock=0
UV_var=1
sysflow_var=0
gradient_var=0
ph_var=1
conductivity_var=0
syspres_var=0;
preC_var=0
fraction_var=0


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.filepath = None
        self.df = None
        self.sheet_names = []
        self.glycan_column = None
        self.relative_percentage_column = None

        # Create a Matplotlib figure
        self.figure = Figure(figsize=(8, 5))
        self.canvas = FigureCanvas(self.figure)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(942, 820)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create tab widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 942, 800))
        self.tabWidget.setObjectName("tabWidget")
        
        # Original Tab
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")

        # Original content from existing code
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView = QtWidgets.QGraphicsView(self.tab1)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 921, 611))
        self.graphicsView.setObjectName("graphicsView")
        
        self.UV = QtWidgets.QCheckBox(self.tab1)
        self.UV.setGeometry(QtCore.QRect(10, 630, 61, 20))
        self.UV.setChecked(True)
        self.UV.setObjectName(variable_name[0])
        self.pH = QtWidgets.QCheckBox(self.tab1)
        self.pH.setGeometry(QtCore.QRect(80, 630, 71, 20))
        self.pH.setChecked(True)
        self.pH.setObjectName(variable_name[1])
        self.Conductivity = QtWidgets.QCheckBox(self.tab1)
        self.Conductivity.setGeometry(QtCore.QRect(139, 630, 131, 20))
        self.Conductivity.setChecked(False)
        self.Conductivity.setObjectName(variable_name[2])
        self.FlowRate = QtWidgets.QCheckBox(self.tab1)
        self.FlowRate.setGeometry(QtCore.QRect(250, 630, 119, 20))
        self.FlowRate.setChecked(False)
        self.FlowRate.setObjectName(variable_name[5])
        self.SystemPressure = QtWidgets.QCheckBox(self.tab1)
        self.SystemPressure.setGeometry(QtCore.QRect(580, 630, 128, 20))
        self.SystemPressure.setObjectName(variable_name[3])
        self.Open = QtWidgets.QPushButton(self.tab1)
        self.Open.setGeometry(QtCore.QRect(10, 670, 231, 50))
        self.Open.setObjectName("Open")
        self.Gradient = QtWidgets.QCheckBox(self.tab1)
        self.Gradient.setGeometry(QtCore.QRect(340, 630, 78, 20))
        self.Gradient.setChecked(False)
        self.Gradient.setObjectName(variable_name[4])
        self.Plot = QtWidgets.QPushButton(self.tab1)
        self.Plot.setGeometry(QtCore.QRect(240, 670, 231, 50))
        self.Plot.setObjectName("Plot")
        self.Export_Data = QtWidgets.QPushButton(self.tab1)
        self.Export_Data.setGeometry(QtCore.QRect(470, 670, 231, 50))
        self.Export_Data.setObjectName("Export_Data")
        self.Save_Image = QtWidgets.QPushButton(self.tab1)
        self.Save_Image.setGeometry(QtCore.QRect(700, 670, 231, 50))
        self.Save_Image.setObjectName("Save_Image")
        self.Precolumn_pressure = QtWidgets.QCheckBox(self.tab1)
        self.Precolumn_pressure.setGeometry(QtCore.QRect(420, 630, 161, 20))
        self.Precolumn_pressure.setObjectName("Precolumn_pressure")
        self.Fractions = QtWidgets.QCheckBox(self.tab1)
        self.Fractions.setGeometry(QtCore.QRect(720, 630, 128, 20))
        self.Fractions.setObjectName(variable_name[6])
        self.PlotOpt = QtWidgets.QPushButton(self.tab1)
        self.PlotOpt.setGeometry(QtCore.QRect(800, 625, 128, 25))
        self.PlotOpt.setObjectName("Options")
        self.xNumber = QtWidgets.QLineEdit(self.tab1)
        self.xNumber.setEnabled(False)
        self.xNumber.setGeometry(QtCore.QRect(360, 725, 101, 21))
        self.xNumber.setObjectName("xNumber")
        self.xSlider = QtWidgets.QSlider(self.tab1)
        self.xSlider.setEnabled(False)
        self.xSlider.setGeometry(QtCore.QRect(140, 725, 211, 22))
        self.xSlider.setMinimum(0)
        self.xSlider.setMaximum(100)
        # self.xSlider.setProperty("value", 100)
        self.xSlider.setOrientation(QtCore.Qt.Horizontal)
        self.xSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.xSlider.setSingleStep(1)
        self.xSlider.setObjectName("xSlider")
        self.xaxis_max = QtWidgets.QLineEdit(self.tab1)
        self.xaxis_max.setEnabled(False)
        self.xaxis_max.setGeometry(QtCore.QRect(20, 725, 111, 21))
        self.xaxis_max.setReadOnly(True)
        self.xaxis_max.setObjectName("xaxis_max")
        self.ySlider = QtWidgets.QSlider(self.tab1)
        self.ySlider.setEnabled(False)
        self.ySlider.setGeometry(QtCore.QRect(600, 725, 211, 22))
        self.ySlider.setMinimum(0)
        self.ySlider.setMaximum(100)
        # self.ySlider.setProperty("value", 0)
        self.ySlider.setOrientation(QtCore.Qt.Horizontal)
        self.ySlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.ySlider.setSingleStep(1)
        self.ySlider.setObjectName("ySlider")
        self.yNumber = QtWidgets.QLineEdit(self.tab1)
        self.yNumber.setEnabled(False)
        self.yNumber.setGeometry(QtCore.QRect(820, 725, 101, 21))
        self.yNumber.setObjectName("yNumber")
        self.xaxis_min = QtWidgets.QLineEdit(self.tab1)
        self.xaxis_min.setEnabled(False)
        self.xaxis_min.setGeometry(QtCore.QRect(480, 725, 111, 21))
        self.xaxis_min.setMouseTracking(False)
        self.xaxis_min.setReadOnly(True)
        self.xaxis_min.setClearButtonEnabled(False)
        self.xaxis_min.setObjectName("xaxis_min")
        
        # Add tab1 to tabWidget
        self.tabWidget.addTab(self.tab1, "Chromatogram Analyzer")

        # Dummy Tab
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
    
        # Add QLabel, QTextEdit, QPushButton, and another QTextEdit for tab2
        self.sequence_label = QtWidgets.QLabel('Enter Protein Sequence:', self.tab2)
        self.sequence_entry = QtWidgets.QTextEdit(self.tab2)
        self.process_button = QtWidgets.QPushButton('Process', self.tab2)
        self.result_text = QtWidgets.QTextEdit(self.tab2)
    
    
        # Always show scrollbars
        self.sequence_entry.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.result_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    
        # Set read-only for the result text
        self.result_text.setReadOnly(True)

        # Dummy widgets in new tab
        self.tab2_layout = QtWidgets.QVBoxLayout(self.tab2)
        self.tab2_layout.addWidget(self.sequence_label)
        self.tab2_layout.addWidget(self.sequence_entry)
        self.tab2_layout.addWidget(self.process_button)
        self.tab2_layout.addWidget(self.result_text)
    
        self.tab2.setLayout(self.tab2_layout)
    
        # Add tab2 to the tabWidget
        self.tabWidget.addTab(self.tab2, "Glycosylation Site Finder")

        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab3")
    
        # Add QLabel, QTextEdit, QPushButton, and another QTextEdit for tab2
        self.tab3_layout = QVBoxLayout()

        # Open File Button
        self.load_button = QPushButton("Open Excel File", self.tab3)
        self.load_button.clicked.connect(self.open_file)
        self.tab3_layout.addWidget(self.load_button)

        # Sheet Dropdown Menu
        self.sheet_label = QLabel("Select Sheet:", self.tab3)
        self.tab3_layout.addWidget(self.sheet_label)
        self.sheet_menu = QComboBox(self.tab3)
        self.tab3_layout.addWidget(self.sheet_menu)

        # Load Sheet Button
        self.load_sheet_button = QPushButton("Load Sheet", self.tab3)
        self.load_sheet_button.clicked.connect(self.load_sheet)
        self.tab3_layout.addWidget(self.load_sheet_button)

        # Dropdown for Glycan Column
        self.glycan_label = QLabel("Select Glycans Column:", self.tab3)
        self.tab3_layout.addWidget(self.glycan_label)
        self.glycan_menu = QComboBox(self.tab3)
        self.tab3_layout.addWidget(self.glycan_menu)

        # Dropdown for Relative Percentage Column
        self.relative_percentage_label = QLabel("Select Relative Percentage Column:", self.tab3)
        self.tab3_layout.addWidget(self.relative_percentage_label)
        self.relative_percentage_menu = QComboBox(self.tab3)
        self.tab3_layout.addWidget(self.relative_percentage_menu)

        # Text box for Relative Percentage Cutoff
        self.cutoff_label = QLabel("Relative Percentage Cutoff (%):",self.tab3)
        self.tab3_layout.addWidget(self.cutoff_label)
        self.cutoff_entry = QLineEdit(self.tab3)
        self.tab3_layout.addWidget(self.cutoff_entry)
        self.cutoff_entry.setText("0.0")

        # Plot Button
        self.plot_button = QPushButton("Plot and Calculate Mass Per Glycan Site",self.tab3)
        self.plot_button.clicked.connect(self.plot_data)
        self.tab3_layout.addWidget(self.plot_button)

        # Calculate Mass Button
        # self.mass_button = QPushButton("Calculate Mass", self.tab3)
        # self.mass_button.clicked.connect(self.calculate_mass)
        # self.tab3_layout.addWidget(self.mass_button)

        # Output box for displaying calculated mass
        self.mass_output_label = QLabel("Total Mass (kDa):", self.tab3)
        self.tab3_layout.addWidget(self.mass_output_label)
        self.mass_output = QLineEdit(self.tab3)
        self.mass_output.setReadOnly(True)
        self.tab3_layout.addWidget(self.mass_output)

        # Add Matplotlib canvas
        self.tab3_layout.addWidget(self.canvas)
        # Dummy widgets in new tab
    
        self.tab3.setLayout(self.tab3_layout)
    
        # Add tab2 to the tabWidget
        self.tabWidget.addTab(self.tab3, "Glycan Mass Finder")
        # Menubar and other main window elements
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 942, 37))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout_Info = QtWidgets.QMenu(self.menubar)
        self.menuAbout_Info.setObjectName("menuAbout_Info")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setEnabled(True)
        self.actionOpen.setVisible(True)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        # self.actionExit = QtWidgets.QAction(MainWindow)
        # self.actionExit.setObjectName("actionExit")
        self.actionExport_Data = QtWidgets.QAction(MainWindow)
        self.actionExport_Data.setObjectName("actionExport_Data")
        self.actionInstructions = QtWidgets.QAction(MainWindow)
        self.actionInstructions.setObjectName("actionInstructions")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExport_Data)
        self.menuFile.addAction(self.actionSave)
        # self.menuFile.addAction(self.actionExit)
        self.menuAbout_Info.addAction(self.actionInstructions)
        self.menuAbout_Info.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout_Info.menuAction())
        
        self.Plot.clicked.connect(lambda: self.plot_graph())
        self.Plot.setEnabled(False)
        self.Save_Image.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.actionExport_Data.setEnabled(False)
        self.Export_Data.setEnabled(False)
        self.UV.stateChanged.connect(lambda: self.check_clicked(self.UV))  ###ADD THIS LINE 
        self.Gradient.stateChanged.connect(lambda: self.check_clicked(self.Gradient))  ###ADD THIS LINE 
        self.pH.stateChanged.connect(lambda: self.check_clicked(self.pH))  ###ADD THIS LINE 
        self.Fractions.stateChanged.connect(lambda: self.check_clicked(self.Fractions))
        self.Precolumn_pressure.stateChanged.connect(lambda: self.check_clicked(self.Precolumn_pressure))
        self.Conductivity.stateChanged.connect(lambda: self.check_clicked(self.Conductivity))  ###ADD THIS LINE 
        self.SystemPressure.stateChanged.connect(lambda: self.check_clicked(self.SystemPressure))  ###ADD THIS LINE 
        self.FlowRate.stateChanged.connect(lambda: self.check_clicked(self.FlowRate))  ###ADD THIS LINE 
        self.Open.clicked.connect(lambda: self.select_file())
        self.actionOpen.triggered.connect(lambda: self.select_file())
        self.Save_Image.clicked.connect(lambda: self.save_image())
        self.actionSave.triggered.connect(lambda: self.save_image())
        self.ySlider.valueChanged.connect(lambda: self.slider_value_change())
        self.xSlider.valueChanged.connect(lambda: self.slider_value_change())
        self.xNumber.textChanged.connect(lambda: self.text_value_change())
        self.yNumber.textChanged.connect(lambda: self.text_value_change())
        self.actionAbout.triggered.connect(lambda: self.license_info())
        self.actionInstructions.triggered.connect(lambda: self.instruction_page())
        # self.actionExit.triggered.connect(lambda: self.close())
        self.actionExport_Data.triggered.connect(lambda: self.save_data())
        self.Export_Data.clicked.connect(lambda: self.save_data())
        self.PlotOpt.clicked.connect(lambda: self.open_plot_options())
        self.process_button.clicked.connect(lambda: self.process_sequence())
        self.retranslateUi(MainWindow)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AktaPure Chromatogram Analyzer V3.00"))
        self.UV.setText(_translate("MainWindow", variable_name[0]))
        self.pH.setText(_translate("MainWindow", variable_name[1]))
        self.Conductivity.setText(_translate("MainWindow", variable_name[2]))
        self.FlowRate.setText(_translate("MainWindow", variable_name[5]))
        self.SystemPressure.setText(_translate("MainWindow", variable_name[3]))
        self.Open.setText(_translate("MainWindow", "Open"))
        self.Gradient.setText(_translate("MainWindow", variable_name[4]))
        self.Plot.setText(_translate("MainWindow", "Plot"))
        self.Export_Data.setText(_translate("MainWindow", "Export Data"))
        self.Save_Image.setText(_translate("MainWindow", "Save Image"))
        self.Precolumn_pressure.setText(_translate("MainWindow", variable_name[8]))
        self.Fractions.setText(_translate("MainWindow", variable_name[6]))
        self.xaxis_max.setText(_translate("MainWindow", "X-axis Maximum"))
        self.xaxis_min.setText(_translate("MainWindow", "X-axis Minimum"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout_Info.setTitle(_translate("MainWindow", "Information"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save Image"))
        # self.actionExit.setText(_translate("MainWindow", "Close"))
        self.actionExport_Data.setText(_translate("MainWindow", "Export Data"))
        self.actionInstructions.setText(_translate("MainWindow", "Instructions"))
        self.actionAbout.setText(_translate("MainWindow", "License"))
        self.PlotOpt.setText(_translate("MainWindow", "Plot Options"))
        
        self.sequence_label.setText(_translate("MainWindow", "Enter Protein Sequence:"))
        self.process_button.setText(_translate("MainWindow", "Process"))
        
    def open_file(self):
        # Open file dialog to select an Excel file
        self.filepath, _ = QFileDialog.getOpenFileName(MainWindow, "Open Excel File", "", "Excel files (*.xls *.xlsx)")
        if self.filepath:
            # Read the sheet names
            try:
                self.sheet_names = pd.ExcelFile(self.filepath).sheet_names
                self.sheet_menu.clear()
                self.sheet_menu.addItems(self.sheet_names)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read Excel file: {e}")

    def load_sheet(self):
        if not self.filepath or not self.sheet_menu.currentText():
            QMessageBox.warning(self, "Warning", "Please select a file and a sheet!")
            return

        # Load the selected sheet
        try:
            self.df = pd.read_excel(self.filepath, sheet_name=self.sheet_menu.currentText())
            columns = list(self.df.columns)
            self.glycan_menu.clear()
            self.glycan_menu.addItems(columns)
            self.relative_percentage_menu.clear()
            self.relative_percentage_menu.addItems(columns)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load sheet: {e}")

    def plot_data(self):
        if self.df is None:
            QMessageBox.warning(self, "Warning", "No sheet loaded!")
            return
    
        glycan_col = self.glycan_menu.currentText()
        relative_percentage_col = self.relative_percentage_menu.currentText()
    
        if not glycan_col or not relative_percentage_col:
            QMessageBox.warning(self, "Warning", "Please select both Glycans and Relative Percentage columns!")
            return
    
        try:
            cutoff = float(self.cutoff_entry.text())
    
            # Filter the dataframe based on the cutoff value
            filtered_df = self.df[self.df[relative_percentage_col] >= cutoff]
    
            if filtered_df.empty:
                QMessageBox.warning(self, "Warning", f"No data found above the cutoff of {cutoff}%.")
                return
    
            # Convert glycan column to strings for plotting
            filtered_df[glycan_col] = filtered_df[glycan_col].astype(str)
    
            # Clear previous plot
            self.figure.clear()
    
            # Create an axis
            ax = self.figure.add_subplot(111)
    
            # Plot data with custom color
            bars = ax.bar(filtered_df[glycan_col], filtered_df[relative_percentage_col], color='royalblue', edgecolor='black')
    
            # Add labels to the axes with improved formatting
            ax.set_xlabel('Glycan Structures', fontsize=12, labelpad=10)
            ax.set_ylabel('Relative Percentage (%)', fontsize=12, labelpad=10)
            ax.set_title(f'Glycan vs. Relative Percentage (Cutoff: {cutoff}%)', fontsize=14, pad=15)
    
            # Rotate x-axis labels and add some spacing between them for better readability
            ax.tick_params(axis='x', rotation=90, labelsize=8)
            ax.tick_params(axis='y', labelsize=10)
    
            # Display gridlines for y-axis
            ax.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7, alpha=0.7)
    
            # Annotate each bar with its height value
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.1f}%',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=10, color='black')
    
            # Make the layout tight to prevent overlap of elements
            self.figure.tight_layout()
    
            # Redraw the canvas
            self.canvas.draw()
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot data: {e}")
            
        if self.df is None:
            QMessageBox.warning(self, "Warning", "No sheet loaded!")
            return

        glycan_col = self.glycan_menu.currentText()
        relative_percentage_col = self.relative_percentage_menu.currentText()

        if not glycan_col or not relative_percentage_col:
            QMessageBox.warning(self, "Warning", "Please select both Glycans and Relative Percentage columns!")
            return

        try:
            input_glycans = self.df[glycan_col].dropna().tolist()
            input_percentage = self.df[relative_percentage_col].dropna().tolist()

            total_weighted_mass = 0.0

            # Function to count HEX, FUC, PENT in the input text and calculate the mass
            def calculate_mass_from_glycan(text):
                pattern = r'(Hex|HexNAc|Hex|Fuc|NeuAc|Pent)\((\d+)\)'
                molecular_weights = {
                    "HexNAc": 221.21,
                    "Hex": 180.156,
                    "Fuc": 164.156,
                    "Pent": 150.13,
                    "NeuAc": 309.270,
                }
                matches = re.findall(pattern, text)
                total_mass = 0.0
                for match in matches:
                    key, value = match
                    total_mass += int(value) * molecular_weights[key]
                return total_mass

            for glycan, percentage in zip(input_glycans, input_percentage):
                mass = calculate_mass_from_glycan(glycan)
                weighted_mass = (mass * percentage) / sum(input_percentage)
                total_weighted_mass += weighted_mass

            # Calculate total glycan and protein mass
            total_glycan_mass_kDa = total_weighted_mass / 1000

            # Display the result in the output box
            self.mass_output.setText(f"{total_glycan_mass_kDa:.2f} kDa")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to calculate mass: {e}")  

    # def calculate_mass(self):
    #     if self.df is None:
    #         QMessageBox.warning(self, "Warning", "No sheet loaded!")
    #         return

    #     glycan_col = self.glycan_menu.currentText()
    #     relative_percentage_col = self.relative_percentage_menu.currentText()

    #     if not glycan_col or not relative_percentage_col:
    #         QMessageBox.warning(self, "Warning", "Please select both Glycans and Relative Percentage columns!")
    #         return

    #     try:
    #         input_glycans = self.df[glycan_col].dropna().tolist()
    #         input_percentage = self.df[relative_percentage_col].dropna().tolist()

    #         total_weighted_mass = 0.0

    #         # Function to count HEX, FUC, PENT in the input text and calculate the mass
    #         def calculate_mass_from_glycan(text):
    #             pattern = r'(Hex|HexNAc|Hex|Fuc|NeuAc|Pent)\((\d+)\)'
    #             molecular_weights = {
    #                 "HexNAc": 221.21,
    #                 "Hex": 180.156,
    #                 "Fuc": 164.156,
    #                 "Pent": 150.13,
    #                 "NeuAc": 309.270,
    #             }
    #             matches = re.findall(pattern, text)
    #             total_mass = 0.0
    #             for match in matches:
    #                 key, value = match
    #                 total_mass += int(value) * molecular_weights[key]
    #             return total_mass

    #         for glycan, percentage in zip(input_glycans, input_percentage):
    #             mass = calculate_mass_from_glycan(glycan)
    #             weighted_mass = (mass * percentage) / sum(input_percentage)
    #             total_weighted_mass += weighted_mass

    #         # Calculate total glycan and protein mass
    #         total_glycan_mass_kDa = total_weighted_mass / 1000

    #         # Display the result in the output box
    #         self.mass_output.setText(f"{total_glycan_mass_kDa:.2f} kDa")

    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to calculate mass: {e}")  
            
    def process_sequence(self):
        self.result_text.clear()
        

    # Get input text
        sequence = self.sequence_entry.toPlainText().strip()
    
        if sequence:
            # Align the sequence text
            line_length = 10  # Number of characters per line
            aligned_lines = []
    
            # Process the input text in chunks for alignment
            for line_number in range(0, len(sequence), line_length):
                # Extract the substring for the current line
                line = sequence[line_number:line_number + line_length]
                # Calculate the line number incrementing by 10 each time
                current_line_number = (line_number // line_length) * 10 + 1
                aligned_lines.append(f" {current_line_number} : {line}")
    
            # Glycosylation site detection
            pattern = re.compile(r'N[^P](T|S)')
            matches = pattern.finditer(sequence)
            locations = [(match.start(), match.group()) for match in matches]
    
            glycosylation_info = "\n".join(
                [f"Site: {loc[0]+1}, Sequence: {loc[1]}" for loc in locations]
            )
            glycosylation_info += f"\nTOTAL GLYCOSYLATION SITES: {len(locations)}"
    
            # Combine both results
            combined_result = '\n'.join(aligned_lines) + "\n\n" + glycosylation_info
            self.result_text.setPlainText(combined_result)
        else:
            self.result_text.setPlainText("Please enter a sequence.")   
    
        
    def check_clicked(self, name):
        self.update_variable_data()    
        global bug_lock,init_val,UV_var, sysflow_var, gradient_var, ph_var, conductivity_var, syspres_var, order_table,preC_var,fraction_var
        if name.isChecked()==True:
            if name.text()==variable_name[0]:
                UV_var=1 
            elif name.text()==variable_name[2]:
                conductivity_var=1
            elif name.text()==variable_name[5]:
                sysflow_var=1
            elif name.text()==variable_name[3]:
                syspres_var=1
            elif name.text()==variable_name[1]:
                ph_var=1
            elif name.text()==variable_name[4]:
                gradient_var=1
            elif name.text()==variable_name[8]:
                preC_var=1
            elif name.text()==variable_name[6]:
                fraction_var=1
                init_val=0
                bug_lock=1
            else:
                print("NAMING ERROR!")
                print(name.text())
            if name.text()!=variable_name[6]:                
                order_table.append(name.text())            
        else:
            if name.text()==variable_name[0]:
                UV_var=0
            elif name.text()==variable_name[2]:
                conductivity_var=0
            elif name.text()==variable_name[5]:
                sysflow_var=0
            elif name.text()==variable_name[3]:
                syspres_var=0
            elif name.text()==variable_name[1]:
                ph_var=0
            elif name.text()==variable_name[4]:
                gradient_var=0
            elif name.text()==variable_name[8]:
                preC_var=0
            elif name.text()==variable_name[6]:
                fraction_var=0
                bug_lock=0
            else:
                print("NAMING ERROR!")
                print(name.text())
            try:
                if name.text()!=variable_name[6]:                
                    order_table.remove(name.text())
            except:
                order_table=[]
        print(order_table)  
    def update_variable_data(self):       
        global variable_name, variable_unit, order_table, units
        from Slave import output_options, stop_var
        for i in range(len(output_options)):
            if i>=9 and i<=17:
                variable_name[i-9]=output_options[i]
            elif i>=18 and i<=26:
                variable_unit[i-18]=output_options[i]
        units=dict([[y,variable_unit[x]] for x,y in enumerate(variable_name)]) 

        self.retranslateUi(MainWindow)
        print("order_table:",order_table)
        print("units:",units)
        
        

           
            
            
        
    def slider_value_change(self):
        self.update_variable_data()
        val_min=self.ySlider.value()
        val_max=self.xSlider.value()
        self.xNumber.setText(str(val_max))
        self.yNumber.setText(str(val_min))
        
    def text_value_change(self):
        self.update_variable_data()
        try:
            val_min=int(self.yNumber.text())
            val_max=int(self.xNumber.text())
        except:
            val_min=0
            val_max=0
        self.ySlider.setProperty("value", int(val_min))
        self.ySlider.setProperty("position", int(val_min))
        self.xSlider.setProperty("value", int(val_max))
        self.xSlider.setProperty("position", int(val_max))
        
    def plot_graph(self):
        self.update_variable_data()
        figure= Figure(figsize=[12,8],dpi=70,tight_layout=True)
        canvas = FigureCanvas(figure)
        figure.clear()
        proxy_widget = self.scene.addWidget(canvas)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.scene().clear()
        
        num_graphs=0
        global save_figure, filename, data_file_load,xmin_val, xmax_val, init_val
        global UV_var, sysflow_var, gradient_var, ph_var, conductivity_var, syspres_var,fraction_var
        num_graphs=sum([UV_var, sysflow_var, gradient_var, ph_var, conductivity_var, syspres_var,preC_var])
        print("NUMBER OF GRAPHS: ", num_graphs)

        self.ySlider.setEnabled(True)
        self.xNumber.setEnabled(True)
        self.yNumber.setEnabled(True)
        self.xSlider.setEnabled(True)
        self.xaxis_max.setEnabled(True)
        self.xaxis_min.setEnabled(True)
        self.Save_Image.setEnabled(True)
        self.actionSave.setEnabled(True)
        self.actionExport_Data.setEnabled(True)
        self.Export_Data.setEnabled(True)

        df = pd.read_csv(filename, encoding='utf-16', sep='\t', skiprows=1)
        #rename columns based on Unicorn titles
        for x_1 in range(0,len(df.columns)):
            if "Unnamed" not in df.columns[x_1]:
                df.iloc[0,x_1] = "ml." + df.columns[x_1]
            if "UV_CUT" in df.columns[x_1]:
                drops = [x_1,x_1+1]
        
        df.drop(df.columns[drops], axis=1, inplace=True)

        # copy 1st row to column headers, then drop it
        UV=pd.DataFrame(columns=["mL","unit"])
        Conductivity=pd.DataFrame(columns=["mL","unit"])
        Gradient_val=pd.DataFrame(columns=["mL","unit"])
        injection=pd.DataFrame(columns=["mL","unit"])
        pH=pd.DataFrame(columns=["mL","unit"])
        preC_press=pd.DataFrame(columns=["mL","unit"])
        sys_pres=pd.DataFrame(columns=["mL","unit"])
        sys_flow=pd.DataFrame(columns=["mL","unit"])
        fraction=pd.DataFrame(columns=["ml.Fraction","Fraction"])
        
        
        try:
            df.columns = df.iloc[0]
            df = df[1:]
            data_file_load=df
            # Just put things in their own df's for simplicity
            UV=df[["ml.UV","mAU"]].apply(pd.to_numeric).rename({"ml.UV":"mL","mAU":"unit"},axis=1)
            # min_mAU = UV["unit"].min()
            # UV_modified = UV.copy()
            # UV_modified["unit"] = UV["unit"] + abs(min_mAU)
            from Slave import output_options
            if output_options[27]=='True':
                min_mAU = UV["unit"].min()
                UV["unit"] = UV["unit"] + abs(min_mAU)
            UV = UV.dropna(how='all')
            pH=df[["ml.pH","pH"]].dropna().apply(pd.to_numeric).rename({"ml.pH":"mL","pH":"unit"},axis=1)
            pH = pH.dropna(how='all')
            Conductivity=df[["ml.Cond","mS/cm"]].dropna().apply(pd.to_numeric).rename({"ml.Cond":"mL","mS/cm":"unit"},axis=1)
            Conductivity=Conductivity[(Conductivity>=0).all(1)]
            gval=df.columns.get_loc("ml.Conc B")
            Gradient_val=df.iloc[:,gval:gval+2].dropna().apply(pd.to_numeric).rename({"ml.Conc B":"mL","%":"unit"},axis=1)
            Gradient_val=Gradient_val[(Gradient_val>=0).all(1)]
            fraction = df[["ml.Fraction","Fraction"]].dropna()
            fraction.loc[-1] = ['0','1']  # adding a row
            fraction.index = fraction.index + 1  # shifting index
            fraction.sort_index(inplace=True)
            fraction.loc[len(fraction)+1]=[str(UV.iloc[-1].tolist()[0]),'Waste']
            fraction["ml.Fraction"]=fraction["ml.Fraction"].apply(pd.to_numeric)
            pval=df.columns.get_loc("ml.PreC pressure")
            preC_press=df.iloc[:,pval:pval+2].dropna().apply(pd.to_numeric).rename({"ml.PreC pressure":"mL","MPa":"unit"},axis=1)
            preC_press=preC_press[(preC_press>=0).all(1)]
            spval=df.columns.get_loc("ml.System pressure")
            sys_pres= df.iloc[:,spval:spval+2].dropna().apply(pd.to_numeric).rename({"ml.System pressure":"mL","MPa":"unit"},axis=1)
            sys_pres=sys_pres[(sys_pres>=0).all(1)]
            sys_flow= df[["ml.System flow","ml/min"]].dropna().apply(pd.to_numeric).rename({"ml.System flow":"mL","ml/min":"unit"},axis=1)
            sys_flow=sys_flow[(sys_flow>=0).all(1)]
            injection = df[["ml.Injection","Injection"]].dropna().apply(pd.to_numeric).rename({"ml.Injection":"mL","Injection":"unit"},axis=1)
            injection=injection[(injection>=0).all(1)]
        except:
            QMessageBox(QMessageBox.Information,"Data Error", "Incomplete data! Please unselect some plotting options or follow the instructions. Thank you")
        final_df={variable_name[0]:UV,variable_name[2]:Conductivity,variable_name[4]:Gradient_val,variable_name[1]:pH, variable_name[7]:injection,variable_name[8]:preC_press,variable_name[5]:sys_flow,variable_name[3]:sys_pres,variable_name[6]:fraction}

        if init_val==0:# or bug_lock==1:
            xmin_val=0
            xmax_val=max(final_df[order_table[0]]['mL'])
            init_val=1
            self.ySlider.setMinimum(0)
            self.ySlider.setMaximum(int(xmax_val))
            self.ySlider.setProperty("value", int(xmin_val))
            self.ySlider.setProperty("position", int(xmin_val))
            self.xSlider.setMinimum(0)
            self.xSlider.setMaximum(int(xmax_val))
            self.xSlider.setProperty("value", int(xmax_val))
            self.xSlider.setProperty("position", int(xmax_val))
            self.xNumber.setText(str(round(xmax_val)))
            self.yNumber.setText(str(round(xmin_val)))

        elif init_val==1:
            xmin_val=float(self.ySlider.value())
            xmax_val=float(self.xSlider.value())
            self.xNumber.setText(str(round(xmax_val)))
            self.yNumber.setText(str(round(xmin_val)))
            self.ySlider.setProperty("position", int(xmin_val))
            self.ySlider.setProperty("value", int(xmin_val))
            self.xSlider.setProperty("position", int(xmax_val))
            self.xSlider.setProperty("value", int(xmax_val))
        print("XMIN: ",xmin_val)
        print("XMAX: ",xmax_val)
        
        def autoscale_y(figure, y_margin=0.1):
            self.update_variable_data() 
            def calculate_y_limits(line):
                x_data = line.get_xdata()
                y_data = line.get_ydata()
                x_min, x_max = figure.get_xlim()
                y_displayed = y_data[((x_data > x_min) & (x_data < x_max))]
                y_range = max(y_displayed) - min(y_displayed)
                y_min = min(y_displayed) - y_margin * y_range
                y_max = max(y_displayed) + y_margin * y_range
                return y_min, y_max
        
            lines = figure.get_lines()
            y_min, y_max = float('inf'), float('-inf')
        
            for line in lines:
                new_y_min, new_y_max = calculate_y_limits(line)
                if new_y_min < y_min:
                    y_min = new_y_min
                if new_y_max > y_max:
                    y_max = new_y_max
            if y_min<0:
                y_min=0
            figure.set_ylim(y_min, y_max)
        size_y=8
        from Slave import output_options
        figure = Figure(figsize=[12,8],tight_layout=True, dpi=70)

        if num_graphs==0:
            pass
        elif num_graphs==1:
            size_x=12
            # figure = Figure(figsize=[size_x,size_y],tight_layout=True)
            ax0 = figure.gca()
            ax0.set_xlabel("Volume (mL)",)   
            ax0.set_ylabel(order_table[0]+units[order_table[0]])
            peak_indices, _ = signal.find_peaks(final_df[order_table[0]]['unit'], prominence=10, distance=10)
            p0, =ax0.plot(final_df[order_table[0]]['mL'], final_df[order_table[0]]['unit'], ls=output_options[0].split("@")[0],color=output_options[0].split("@")[1])
            ax0.yaxis.label.set_color(p0.get_color()) 
            from Slave import output_options
            if output_options[28] == 'True':
                # Find peaks with prominence and distance filtering
                peak_indices, _ = signal.find_peaks(final_df[order_table[0]]['unit'], prominence=10, distance=10)
                
                # Plot the identified peaks with a "*" marker
                ax0.plot(final_df[order_table[0]]['mL'].iloc[peak_indices], 
                         final_df[order_table[0]]['unit'].iloc[peak_indices], 
                         "*", color=p0.get_color(), markersize=10)
            
                # Add graded shaded lines around each peak
                for peak_index in peak_indices:
                    peak_x = final_df[order_table[0]]['mL'].iloc[peak_index]
                    peak_y = final_df[order_table[0]]['unit'].iloc[peak_index]
                    
                    # Define the shading range around each peak (adjust as necessary)
                    shading_width = 0.2  # width around the peak for the shading area
                    
                    # Shade a region around each peak
                    ax0.fill_betweenx([0, peak_y], peak_x - shading_width, peak_x + shading_width, 
                                      color=p0.get_color(), alpha=0.2, linestyle="--")
            
            plt.show()
            
        elif num_graphs==2:
            size_x=12
            # figure = Figure(figsize=[size_x,size_y],tight_layout=True)
            ax0 = figure.gca()
            ax0.set_xlabel("Volume (mL)")
            ax1=ax0.twinx()
            ax1.spines.right.set_position(("axes", 1.0))
            ax0.set_ylabel(order_table[0]+units[order_table[0]])
            ax1.set_ylabel(order_table[1]+units[order_table[1]])
            p0, =ax0.plot(final_df[order_table[0]]['mL'], final_df[order_table[0]]['unit'], ls=output_options[0].split("@")[0],color=output_options[0].split("@")[1])
            p1, =ax1.plot(final_df[order_table[1]]['mL'], final_df[order_table[1]]['unit'], ls=output_options[1].split("@")[0],color=output_options[1].split("@")[1])
            ax0.yaxis.label.set_color(p0.get_color())
            ax1.yaxis.label.set_color(p1.get_color())
        elif num_graphs==3:
            size_x=12.8
            figure = Figure(figsize=[size_x,size_y],tight_layout=True,dpi=70)
            ax0 = figure.gca()
            ax0.set_xlabel("Volume (mL)")
            ax1=ax0.twinx()
            ax2=ax0.twinx()
            ax1.spines.right.set_position(("axes", 1.0))
            ax2.spines.right.set_position(("axes", 1.15))
            ax0.set_ylabel(order_table[0]+units[order_table[0]])
            ax1.set_ylabel(order_table[1]+units[order_table[1]])
            ax2.set_ylabel(order_table[2]+units[order_table[2]])

            p0, =ax0.plot(final_df[order_table[0]]['mL'], final_df[order_table[0]]['unit'], ls=output_options[0].split("@")[0],color=output_options[0].split("@")[1])
            p1, =ax1.plot(final_df[order_table[1]]['mL'], final_df[order_table[1]]['unit'], ls=output_options[1].split("@")[0],color=output_options[1].split("@")[1])
            p2, =ax2.plot(final_df[order_table[2]]['mL'], final_df[order_table[2]]['unit'], ls=output_options[2].split("@")[0],color=output_options[2].split("@")[1])
            ax0.yaxis.label.set_color(p0.get_color())
            ax1.yaxis.label.set_color(p1.get_color())
            ax2.yaxis.label.set_color(p2.get_color())
        elif num_graphs==4:
            size_x=13.2
            figure = Figure(figsize=[size_x,size_y],tight_layout=True,dpi=70)
            ax0 = figure.gca()
            ax0.set_xlabel("Volume (mL)")
            ax1=ax0.twinx()
            ax2=ax0.twinx()
            ax3=ax0.twinx()
            ax1.spines.right.set_position(("axes", 1.0))
            ax2.spines.right.set_position(("axes", 1.15))
            ax3.spines.right.set_position(("axes", 1.30))
            ax0.set_ylabel(order_table[0]+units[order_table[0]])
            ax1.set_ylabel(order_table[1]+units[order_table[1]])
            ax2.set_ylabel(order_table[2]+units[order_table[2]])
            ax3.set_ylabel(order_table[3]+units[order_table[3]])

            p0, =ax0.plot(final_df[order_table[0]]['mL'], final_df[order_table[0]]['unit'], ls=output_options[0].split("@")[0],color=output_options[0].split("@")[1])
            p1, =ax1.plot(final_df[order_table[1]]['mL'], final_df[order_table[1]]['unit'], ls=output_options[1].split("@")[0],color=output_options[1].split("@")[1])
            p2, =ax2.plot(final_df[order_table[2]]['mL'], final_df[order_table[2]]['unit'], ls=output_options[2].split("@")[0],color=output_options[2].split("@")[1])
            p3, =ax3.plot(final_df[order_table[3]]['mL'], final_df[order_table[3]]['unit'], ls=output_options[3].split("@")[0],color=output_options[3].split("@")[1])
            ax0.yaxis.label.set_color(p0.get_color())
            ax1.yaxis.label.set_color(p1.get_color())
            ax2.yaxis.label.set_color(p2.get_color())
            ax3.yaxis.label.set_color(p3.get_color())
        elif num_graphs==5:
            size_x=14.2
            figure = Figure(figsize=[size_x,size_y],tight_layout=True,dpi=70)
            ax0 = figure.gca()
            ax0.set_xlabel("Volume (mL)")
            ax1=ax0.twinx()
            ax2=ax0.twinx()
            ax3=ax0.twinx()
            ax4=ax0.twinx()
            ax1.spines.right.set_position(("axes", 1.0))
            ax2.spines.right.set_position(("axes", 1.15))
            ax3.spines.right.set_position(("axes", 1.30))
            ax4.spines.right.set_position(("axes", 1.45))
            ax0.set_ylabel(order_table[0]+units[order_table[0]])
            ax1.set_ylabel(order_table[1]+units[order_table[1]])
            ax2.set_ylabel(order_table[2]+units[order_table[2]])
            ax3.set_ylabel(order_table[3]+units[order_table[3]])
            ax4.set_ylabel(order_table[4]+units[order_table[4]])

            p0, =ax0.plot(final_df[order_table[0]]['mL'], final_df[order_table[0]]['unit'], ls=output_options[0].split("@")[0],color=output_options[0].split("@")[1])
            p1, =ax1.plot(final_df[order_table[1]]['mL'], final_df[order_table[1]]['unit'], ls=output_options[1].split("@")[0],color=output_options[1].split("@")[1])
            p2, =ax2.plot(final_df[order_table[2]]['mL'], final_df[order_table[2]]['unit'], ls=output_options[2].split("@")[0],color=output_options[2].split("@")[1])
            p3, =ax3.plot(final_df[order_table[3]]['mL'], final_df[order_table[3]]['unit'], ls=output_options[3].split("@")[0],color=output_options[3].split("@")[1])
            p4, =ax4.plot(final_df[order_table[4]]['mL'], final_df[order_table[4]]['unit'], ls=output_options[4].split("@")[0],color=output_options[4].split("@")[1])
            ax0.yaxis.label.set_color(p0.get_color())
            ax1.yaxis.label.set_color(p1.get_color())
            ax2.yaxis.label.set_color(p2.get_color())
            ax3.yaxis.label.set_color(p3.get_color())
            ax4.yaxis.label.set_color(p4.get_color())
        elif num_graphs==6:
            size_x=15.8
            figure = Figure(figsize=[size_x,size_y],tight_layout=True,dpi=70)
            ax0 = figure.gca()
            ax0.set_xlabel("Volume (mL)")
            ax1=ax0.twinx()
            ax2=ax0.twinx()
            ax3=ax0.twinx()
            ax4=ax0.twinx()
            ax5=ax0.twinx()
            ax1.spines.right.set_position(("axes", 1.0))
            ax2.spines.right.set_position(("axes", 1.15))
            ax3.spines.right.set_position(("axes", 1.30))
            ax4.spines.right.set_position(("axes", 1.45))
            ax5.spines.right.set_position(("axes", 1.60))
            ax0.set_ylabel(order_table[0]+units[order_table[0]])
            ax1.set_ylabel(order_table[1]+units[order_table[1]])
            ax2.set_ylabel(order_table[2]+units[order_table[2]])
            ax3.set_ylabel(order_table[3]+units[order_table[3]])
            ax4.set_ylabel(order_table[4]+units[order_table[4]])
            ax5.set_ylabel(order_table[5]+units[order_table[5]])

            p0, =ax0.plot(final_df[order_table[0]]['mL'], final_df[order_table[0]]['unit'], ls=output_options[0].split("@")[0],color=output_options[0].split("@")[1])
            p1, =ax1.plot(final_df[order_table[1]]['mL'], final_df[order_table[1]]['unit'], ls=output_options[1].split("@")[0],color=output_options[1].split("@")[1])
            p2, =ax2.plot(final_df[order_table[2]]['mL'], final_df[order_table[2]]['unit'], ls=output_options[2].split("@")[0],color=output_options[2].split("@")[1])
            p3, =ax3.plot(final_df[order_table[3]]['mL'], final_df[order_table[3]]['unit'], ls=output_options[3].split("@")[0],color=output_options[3].split("@")[1])
            p4, =ax4.plot(final_df[order_table[4]]['mL'], final_df[order_table[4]]['unit'], ls=output_options[4].split("@")[0],color=output_options[4].split("@")[1])
            p5, =ax5.plot(final_df[order_table[5]]['mL'], final_df[order_table[5]]['unit'], ls=output_options[5].split("@")[0],color=output_options[5].split("@")[1])
            ax0.yaxis.label.set_color(p0.get_color())
            ax1.yaxis.label.set_color(p1.get_color())
            ax2.yaxis.label.set_color(p2.get_color())
            ax3.yaxis.label.set_color(p3.get_color())
            ax4.yaxis.label.set_color(p4.get_color())
            ax5.yaxis.label.set_color(p5.get_color())
        else:
            msg=QMessageBox(QMessageBox.Information,"Plotting Limitation", "Cannot plot more than 6 plots at a time!")
            msg.exec_()
        if fraction_var==1:
            from Slave import output_options
            # print("FIX: ",fraction_lbl_size_main)
            ax6=ax0.twiny()
            ax6.set_xlabel("Fractions")
            final_df['Fraction']
            tick_sets=[]
            temp_tick_labels=final_df['Fraction']['Fraction'].tolist()
            temp_tick_sets=final_df['Fraction']['ml.Fraction'].apply(pd.to_numeric).tolist()
            count_j=0
            tick_sets=[]
            tick_labels=[]
            for i in range(len(temp_tick_sets)):
                if (temp_tick_sets[i]>=xmin_val and temp_tick_sets[i]<=xmax_val):
                    tick_sets.append(temp_tick_sets[i])
                    if temp_tick_labels[i]=="Waste":
                        tick_labels.append(" ")
                    else:
                        tick_labels.append(temp_tick_labels[i])
                    count_j+=1
            # count=0
            # temp=final_df['Fraction']['Fraction'].tolist()
            # for i in range(len(tick_sets)):
            #     if (tick_sets[i]>=xmin_val and tick_sets[i]<=xmax_val):
            #         if temp[i]=="Waste":
            #             tick_labels.append(" ")
            #         else:
            #             count+=1
            #             tick_labels.append(count)

            ax6.set_xticks(tick_sets)
            
            print("LABEL FONT SIZE: ",fraction_lbl_size_main)
            ax6.xaxis.set_tick_params(labelsize=output_options[8])
            ax6.spines["bottom"].set_position(("axes", -0.12))
            ax6.xaxis.set_ticks_position("bottom")
            ax6.xaxis.set_label_position("bottom")
            ax6.set_xticklabels(tick_labels, rotation=0)
            ax6.tick_params(which='both', length=6)
            ax6.set_xlim(left=xmin_val,right=xmax_val)
            for i in range(len(tick_sets)):
                ax6.axvline(tick_sets[i],0,1,alpha=0.2,color='k',linewidth='1',ls='--')
            # for i in range(len(final_df['Fraction']['ml.Fraction'])):
            #     if (final_df['Fraction']['ml.Fraction'][i] >= ax0.get_xlim()[0] and final_df['Fraction']['ml.Fraction'] <= ax0.get_xlim()[1]):
            #         ax6.axvline(final_df['Fraction']['ml.Fraction'][i], ls='--', alpha = 0.1)
            
        try:
            ax0.set_xlim(left=xmin_val,right=xmax_val)
            autoscale_y(ax0)
            ax0.minorticks_on()
            ax0.tick_params(which='minor', length=4)
            # ax0.set_ylim(0)
            # start, end = ax0.get_xlim()
            # ax0.xaxis.set_ticks(np.arange(start, end, 5))
            ax1.set_xlim(left=xmin_val,right=xmax_val)
            ax1.set_ylim(min(final_df[order_table[1]]['mL']),max(final_df[order_table[1]]['mL']))
            autoscale_y(ax1)
            ax1.minorticks_on()
            ax2.set_xlim(left=xmin_val,right=xmax_val)
            ax2.set_ylim(min(final_df[order_table[2]]['mL']),max(final_df[order_table[2]]['mL']))
            autoscale_y(ax2)
            ax2.minorticks_on()
            ax3.set_xlim(left=xmin_val,right=xmax_val)
            ax3.set_ylim(min(final_df[order_table[3]]['mL']),max(final_df[order_table[3]]['mL']))
            autoscale_y(ax3)
            ax3.minorticks_on()
            ax4.set_xlim(left=xmin_val,right=xmax_val)
            ax4.set_ylim(min(final_df[order_table[4]]['mL']),max(final_df[order_table[4]]['mL']))
            autoscale_y(ax4)
            ax4.minorticks_on()
            ax5.set_xlim(left=xmin_val,right=xmax_val)
            ax5.set_ylim(min(final_df[order_table[5]]['mL']),max(final_df[order_table[5]]['mL']))
            autoscale_y(ax5)
            ax5.minorticks_on()
            ax6.set_xlim(left=xmin_val,right=xmax_val)
            autoscale_y(ax6)
            ax6.minorticks_on()
        except:
            pass
        canvas = FigureCanvas(figure)
        save_figure=figure
        proxy_widget = self.scene.addWidget(canvas)
        self.graphicsView.setScene(self.scene)

    def closeEvent(self, event):
        event.accept()
        
    def select_file(self):
        global filename,init_val
        self.update_variable_data()
        filename,_ = QFileDialog.getOpenFileName(MainWindow, "Open Data File", "","All Files (*);;Text Files (*.txt);;CSV Files (*.csv)")
        print(filename)
        self.Plot.setEnabled(True)
        init_val=0

        
    def save_image(self):
        global save_figure
        img_save_loc=""
        img_save_loc= QFileDialog.getExistingDirectory(MainWindow, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        now = datetime.now()
        try:
            output_file=img_save_loc+"/"+"Figure_"+str(now.strftime("%d_%m_%Y_%S_%M_%H"))+".png"
            save_figure.savefig(output_file,dpi=300,bbox_inches='tight')
        except:
            pass   
    def license_info(self):
        msg=QMessageBox(QMessageBox.Information,"Developer Information", "Software developed by Anindya Karmaker. Based on initial coding by Kevin Yates . Checkout the <a href='http://google.com/'>GitHub</a> link for more updates.  Disclaimer: The software cannot guarantee the accuracy of the data and the developer claims no responsiblity. Please verify the data before publishing the output data from this software.")
        msg.exec_()
    def instruction_page(self):
        msg=QMessageBox(QMessageBox.Information,"Instructions", "The software can read the txt output file from the Unicorn software. Tested with Unicorn v7.0. On the Unicorn Software, select all of the data that you want to export and the output will be a text file. Load the text file into the software. Press the plot button and the checked graphs will appear magically. Choose the graphs that you are interested by checking the check-boxes and press plot. You can zoom in the graph by choosing the X-axis maximum and minimum values. To see the fractions, check the fraction check-box. Fractions check-box will reset the x-axis minimum and maximum. The export data option will export the data in Excel format and the save image option will save the image graph at 300 DPI for direct use.")
        msg.exec_()
    def save_data(self):
        global data_file_load
        data_save_loc=""
        data_save_loc= QFileDialog.getExistingDirectory(MainWindow, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        now = datetime.now()
        # try:
        output_file=data_save_loc+"/"+"DATA_"+str(now.strftime("%d_%m_%Y_%S_%M_%H"))+".xlsx"
        data_file_load.to_excel(output_file)
    def open_plot_options(self):
        self.ui = Ui_SecondWindow()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
