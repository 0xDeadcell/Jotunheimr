""" Just a program to practice pyqt while reading through the docs """
import sys
import os
# import winapi
import ctypes

import psutil
from PyQt5.QtCore import QT_VERSION_STR, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QHBoxLayout, QSpinBox, QCheckBox, QComboBox



class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        # super() allows us to access the methods of QWidget (or others args)
        self.title = 'Process Injector'
        self.x = 50
        self.y = 50
        self.width = 500
        self.height = 175
        self.font = 'Times New Roman'
        self.font_size = 10
        
        ''' Set window size, layout, font size, button press behavior, etc. '''
        self.initUI()
        
        self.listeners()
        
        self.show() # Show the widget
    
    
    def listeners(self):
        self.update_list_button.clicked.connect(lambda x: self.filtered_programs(source='combo_box'))
        self.list_programs.clicked.connect(lambda x: [ print(f'[+] {i}') for i in self.filtered_programs(source='filter_input') ])
        self.search_button.clicked.connect(self.button_click)
        self.kill_button.clicked.connect(lambda x: self.kill_pid(self.pid_dropdown.currentText()))
        
        # Update the pids while moving down the program list
        self.program_dropdown.currentIndexChanged.connect(self.get_pids)
        
        # Upon inject_button press attempt to inject into the PID
        self.inject_button.clicked.connect(self.inject_into_process)
        


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height) # Setting the size of the main window
        self.filter_input = QLineEdit() # Adding an edit field with a max char limit, and font.
        self.filter_input.setMaxLength(32)
        self.filter_input.setFont(QFont(self.font, self.font_size))
        
        
        self.search_button = QPushButton("Search") # A search button that takes input from filter_input
        self.pid_checkbox = QCheckBox("Filter by PID")
        self.list_programs = QPushButton("Print Running Programs")
        self.inject_button = QPushButton("Inject into Process")
        self.kill_button = QPushButton("Kill PID")
        
        
        self.program_dropdown = QComboBox() # Drop down of all programs
        self.filtered_programs(source='combo_box')
        self.pid_dropdown = QComboBox() # Drop down of PIDs associated with program currently selected
        self.get_pids()
        
        self.update_list_button = QPushButton("Refresh Program List")
        
        
        
        self.layout = QFormLayout()
        self.layout.addRow('Available Applications: ', self.program_dropdown)
        self.layout.addRow("PIDs: ", self.pid_dropdown) # Filter on a certain PID
        self.layout.addRow("Filter Apps By: ", self.filter_input) # Filtering out the list of apps
        self.layout.addRow('', self.update_list_button)
        self.layout.addRow('', self.pid_checkbox)
        self.layout.addRow('', self.list_programs)
        self.layout.addRow('', self.search_button)
        self.layout.addRow('', self.kill_button)
        self.layout.addRow('', self.inject_button)
        
        # self.layout.setAlignment(Qt.AlignCenter)
        # Put the widget in the center
        self.setLayout(self.layout)
        
    
    def inject_into_process(self):
        selected_pid = self.pid_dropdown.currentText()
        print(f"[*] Attempting to inject into {selected_pid}")
        dllofpid = GetDLL(selected_pid)
        self.process_handle = dllofpid.injection()
        if not self.process_handle:
            print(f"[!] Couldn't get handle to PID: {selected_pid}")
            print(f"[!] Are you sure {selected_pid} is a valid PID?")
        else:
            print("Successfully retrieved handle")     
                
        
    
    
    def get_pids(self):
        program = self.program_dropdown.currentText()
        matching_pids = GetPid().get_matching_pids(program)
        self.pid_dropdown.clear()
        
        if matching_pids:
            self.pid_dropdown.addItems(map(str, matching_pids))
            self.setWindowTitle(f'{self.title} - [{len(matching_pids)}] PIDs found')
        
    
    def update_combo_box(self, items):
        if items:
            os.system('cls')
            self.program_dropdown.clear()
            self.program_dropdown.addItems(items)
            print("[+] Program list refreshed!\n")
    
    
    def filtered_programs(self, source):
        # Filter if filter_input has text, otherwise send back all image names.            
        text = self.filter_input.text()
        nomatch = [f"No matches found for: '{text}'"]
        
        if text:
            print(f"[+] Finding programs matching: '{text}'")
        else:
            all_programs = sorted([ i for i in GetPid().get_image_names() ])
            
            if source != 'combo_box':
                return all_programs
            else:
                return self.update_combo_box(items=all_programs)
        
        
        if source == 'combo_box':
            match = [ i for i in GetPid().filter_procs_by_name(text) ]
            if match:
                self.update_combo_box(items=match)
            else:
                self.update_combo_box(items=nomatch)
        

        elif source != 'combo_box':
            match = [ i for i in GetPid().filter_procs_by_name(text) ]
            if match:
                self.update_combo_box(items=match)
                return match
            else:
                self.update_combo_box(items=nomatch)
                return nomatch
            
            
    
    def button_click(self):
        proc_search = self.program_dropdown.currentText()
        user_pid = self.pid_dropdown.currentText()
        check_pid = self.pid_checkbox.isChecked()
        
        if proc_search != "":
            print(f"[+] Searching for: {proc_search}")
            
            try:
                matching_procs = GetPid(proc_search)
                if user_pid and check_pid:
                    print(f"[+] Filtering for PID: {user_pid}")
                    for each_proc in matching_procs.proc_info():
                        if each_proc['pid'] == int(user_pid):
                            print(each_proc)
                
                elif all([user_pid, check_pid]) == False:
                    for each_proc in matching_procs.proc_info():
                        print(each_proc)
                    
                        
            except SyntaxError:
                print(f"[-] '{proc_search}' was not found.")
            
            print("\n")
            
        else:
            print("\n")
            return -1
    
    
    def kill_pid(self, pid):
        if pid != '':
            pid = int(pid)
            if pid in psutil.pids() and pid != 1:
                try:
                    psutil.Process(pid).kill()
                except Exception as err:
                    print(f"[-] Killing of PID: {pid} failed -> {err}.")
                    return -1
                
                self.filtered_programs(source='combo_box')
                print(f"[+] PID: {pid} killed successfully.")
                return 0
        print(f"[-] PID: {pid} not found.")


class GetPid():
    """ Locates a running processes PID, PPID and path by imagename """
    
    def __init__(self, image_name=''):
        self.image_name = image_name.lower()
        self.image_exists = self.image_name in self.get_image_names()
        if not self.image_exists and self.image_name != '':
            raise SyntaxError
            
        
    def __bool__(self):
        return self.image_exists
        
    
    def get_image_names(self):
        image_names = set([ i.info['name'].lower() for i in psutil.process_iter(['name']) ])
        return image_names
        
    
    def filter_procs_by_name(self, s_match):
        ''' Filters out processes that match a string'''
        return [ i for i in self.get_image_names() if s_match in i] 


    def proc_info(self):
        l = [ p.info for p in psutil.process_iter(['name', 'exe', 'cmdline', 'pid', 'ppid']) if p.info['name'].lower() == self.image_name ]
        return l
        
        
    def get_matching_pids(self, s_match):
        ''' returns a list of PIDs '''
        p = [ p.info['pid'] for p in psutil.process_iter(['name', 'pid']) if p.info['name'].lower() == s_match.lower() ]
        return p
        

    def get_pids(self):
        return [ i['pid'] for i in self.proc_info() ]


class GetDLL():
    """ Locates the DLLs for a PID """

    def __init__(self, pid):
        self.pid = pid
        self.PAGE_READWRITE = 0x04
        self.PROCESS_ALL_ACCESS = ( 0x00F0000 | 0x00100000 | 0xFFF )
        self.VIRTUAL_MEM = ( 0x1000 | 0x2000 )
        self.kernel32 = ctypes.windll.kernel32
        
    
    
    def injection(self):
        # Get handle to process being injected...
        process_handle = self.kernel32.OpenProcess( self.PROCESS_ALL_ACCESS, False, int(self.pid) )

        if not process_handle:
            return False
            
        return True
        



if __name__ == "__main__":
    app = QApplication(sys.argv) # argv here so we can pass CLI arguments to the app
    os.system('cls')
    window = MainWindow()
    sys.exit(app.exec_()) # When run loop is finished exit the program



