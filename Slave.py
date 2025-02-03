import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QLabel, QGroupBox, QLineEdit, QFileDialog, QCheckBox
from PyQt5 import QtCore, QtGui, QtWidgets

global old_variable_name, fraction_lbl_size_main, output_options, order_table, units, variable_name, variable_unit, custom_updated, stop_var
stop_var = 0
custom_updated = 0
fraction_lbl_size_main = 8
color_list = ["blue", "green", "red", "magenta", "cyan", "yellow", "Custom"]
style_list = ["-", "--", "-.", ":"]
output_options = ['-@b', '-@g', '-@r', '-@m', '-@c', '-@k', 'Arial', '10', '10', 'UV', 'pH', 'Conductivity', 'System Pressure', 'Gradient', 'Flow rate', 'Fraction', 'Injection', 'Pre-column Pressure', ' (mAU)', '', ' (mS/cm)', ' (MPa)', '%', ' (mL/min)', 'Fraction', ' (mL/min)', ' (MPa)', 'False', 'False', 'True']

variable_name = ['UV', 'pH', 'Conductivity', 'System Pressure', 'Gradient', 'Flow rate', 'Fraction', 'Injection', 'Pre-column Pressure']
variable_unit = [' (mAU)', ' ', ' (mS/cm)', ' (MPa)', ' %', ' (mL/min)', ' Fraction', ' (mL/min)', ' (MPa)']
order_table = [variable_name[0], variable_name[1]]
units = dict([[y, variable_unit[x]] for x, y in enumerate(variable_name)])


class Ui_SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        global custom_updated
        if custom_updated == 0:
            global old_variable_name
            old_variable_name = []
            for i in range(len(variable_name)):
                old_variable_name.append(variable_name[i])
            custom_updated = 1

    def initUI(self):
        self.color_combos = []
        self.style_combos = []
        self.combined_list = []
        self.plot_color_list = []

        # Create a horizontal layout for the color and style comboboxes
        h_box = QHBoxLayout()

        for i in range(6):
            group_box = QGroupBox("Plot {}".format(i+1))
            group_layout = QVBoxLayout()

            color_combo = QComboBox()
            color_combo.addItems(color_list)
            color_combo.setCurrentText(color_list[i])
            self.color_combos.append(color_combo)

            style_combo = QComboBox()
            style_combo.addItems(style_list)
            self.style_combos.append(style_combo)

            plot_color_style = QLineEdit()
            self.plot_color_list.append(plot_color_style)

            group_layout.addWidget(QLabel("Color"))
            group_layout.addWidget(color_combo)
            group_layout.addWidget(QLabel("Style"))
            group_layout.addWidget(style_combo)
            group_layout.addWidget(QLabel("Custom Color(#HEX)"))
            group_layout.addWidget(plot_color_style)

            group_box.setLayout(group_layout)
            h_box.addWidget(group_box)

        variable_h_boxes = []
        self.variable_name_line_edits = []
        self.variable_unit_line_edits = []

        for i in range(9):
            variable_h_box = QHBoxLayout()
            variable_name_edit = QLineEdit(variable_name[i])
            variable_unit_edit = QLineEdit(variable_unit[i])
            self.variable_name_line_edits.append(variable_name_edit)
            self.variable_unit_line_edits.append(variable_unit_edit)
            variable_h_box.addWidget(QLabel(f"Variable {i+1} Name"))
            variable_h_box.addWidget(variable_name_edit)
            variable_h_box.addWidget(QLabel(f"Variable {i+1} Unit"))
            variable_h_box.addWidget(variable_unit_edit)
            variable_h_boxes.append(variable_h_box)

        v_box = QVBoxLayout()
        v_box.addLayout(h_box)
        variable_v_box = QVBoxLayout()

        for variable_h_box in variable_h_boxes:
            v_box.addLayout(variable_h_box)

        self.update_variable_lists()
        self.font_combo = QComboBox()
        self.font_combo.addItems(['Arial', 'Helvetica', 'Times New Roman', 'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'])

        self.font_size = QLineEdit()
        self.font_size.setFixedWidth(100)
        self.fraction_size = QLineEdit()
        self.fraction_size.setFixedWidth(100)
        self.font_size.setText('10')
        self.fraction_size.setText('10')
        
        v_box.addWidget(QLabel("Font Format"))
        v_box.addWidget(self.font_combo)
        v_box.addWidget(QLabel("Font Size"))
        v_box.addWidget(self.font_size)
        v_box.addWidget(QLabel("Fraction Size"))
        v_box.addWidget(self.fraction_size)
        v_box.addLayout(variable_v_box)

        # Add checkboxes for additional options
        self.offset_negative_values_checkbox = QCheckBox("Offset Negative UV Values")
        self.highlight_peak_checkbox = QCheckBox("Highlight Peak")
        self.show_relative_protein_amount_checkbox = QCheckBox("Show Relative Protein Amount")

        v_box.addWidget(self.offset_negative_values_checkbox)
        v_box.addWidget(self.highlight_peak_checkbox)
        v_box.addWidget(self.show_relative_protein_amount_checkbox)

        output_button = QPushButton("Save Options", self)
        output_button.clicked.connect(self.output_list)
        
        load_button = QPushButton("Load Options", self)
        load_button.clicked.connect(self.load_options)
        
        v_box.addWidget(output_button)
        v_box.addWidget(load_button)
        v_box.addStretch()
        self.setLayout(v_box)
        self.setWindowTitle("Plot Options")
        self.show()

    def update_variable_lists(self):
        for i in range(9):
            variable_name[i] = self.variable_name_line_edits[i].text()
            variable_unit[i] = self.variable_unit_line_edits[i].text()

    def combine_values(self):
        global custom_updated, variable_name, old_variable_name
        self.combined_list = []
        
        # Collect color and style options
        for i in range(6):
            color = self.color_combos[i].currentText()
            style = self.style_combos[i].currentText()
            font = self.font_combo.currentText()
            font_size = self.font_size.text()
            fraction_size = self.fraction_size.text()
            if color == 'Custom':
                color = self.plot_color_list[i].text()
                self.combined_list.append(f"{style}@{color}")
            else:
                self.combined_list.append(f"{style}@{color[0]}")
        
        # Add font and size details
        self.combined_list.append(font)
        self.combined_list.append(font_size)
        self.combined_list.append(fraction_size)

        # Add variable names and units
        self.combined_list.extend(variable_name)
        self.combined_list.extend(variable_unit)

        # Add checkbox states
        self.combined_list.append(str(self.offset_negative_values_checkbox.isChecked()))
        self.combined_list.append(str(self.highlight_peak_checkbox.isChecked()))
        self.combined_list.append(str(self.show_relative_protein_amount_checkbox.isChecked()))

        global output_options
        output_options = self.combined_list

        if old_variable_name != variable_name:
            custom_updated = 1
            global stop_var
            stop_var = 1
            global order_table
            order_table = []
        elif old_variable_name == variable_name:
            stop_var = 0
            custom_updated = 0

    def output_list(self):
        # Update the variable_name and variable_unit lists
        self.update_variable_lists()

        import matplotlib.pylab as pylab
        global output_options

        try:
            global fraction_lbl_size_main
            fp_size = int(self.font_size.text())
            pylab.rcParams.update({'font.size': fp_size, 'font.family': str(self.font_combo.currentText())})
            fraction_lbl_size_main = int(self.fraction_size.text())
        except:
            fp_size = 10
            pylab.rcParams.update({'font.size': fp_size, 'font.family': str(self.font_combo.currentText())})
            fraction_lbl_size_main = 8

        self.combine_values()
        global order_table
        order_table = [variable_name[0], variable_name[1]]
        options_file = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text files (*.txt)')[0]
        if options_file:
            with open(options_file, 'w') as f:
                f.writelines("%s\n" % item for item in output_options)

    def load_options(self):
        options_file = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text files (*.txt)')[0]
        global output_options, custom_updated, variable_name
        output_options = []
        
        if options_file:
            with open(options_file, 'r') as f:
                lines = f.readlines()
                output_options = [line.strip() for line in lines]

            # Extract variable_name and variable_unit
            variable_name = output_options[-21:-12]
            variable_unit = output_options[-12:-3]

            # Update the UI with loaded values for each field
            for i, line_edit in enumerate(self.variable_name_line_edits):
                line_edit.setText(variable_name[i])
            for i, line_edit in enumerate(self.variable_unit_line_edits):
                line_edit.setText(variable_unit[i])

            # Update checkbox states based on the loaded file
            self.offset_negative_values_checkbox.setChecked(output_options[-3] == 'True')
            self.highlight_peak_checkbox.setChecked(output_options[-2] == 'True')
            self.show_relative_protein_amount_checkbox.setChecked(output_options[-1] == 'True')
            
            custom_updated = 1
            print("SECOND GUI OUTPUT OPTIONS ARE: ")
            print(output_options)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_SecondWindow()
    sys.exit(app.exec_())
    # Add remaining methods here (update_variable_lists, combine_values, output_list, load_options)
