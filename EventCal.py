import json
import os.path
import calendar
import tkinter as tk
import datetime as dt
from time import strftime  # @UnusedImport
from tkinter import messagebox  # @UnusedImport


class MintApp(tk.Frame):


    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.pack()
        self.parent = parent
        self.parent.geometry("1100x650")
        self.parent.bind("<Configure>", self.move_me)
        
        self.current_day = dt.datetime.now().day
        self.current_month_number = dt.datetime.now().month
        self.current_year = dt.datetime.now().year
        self.current_weekday_number = dt.datetime.today().weekday()
        self.todays_date = dt.datetime.today()
        self.current_selected_year = self.current_year
        self.current_selected_month = self.current_month_number
        self.appmanager = None
        self.appointment_manager_exist = None
        
        self.previous_month_num = self.current_month_number
        
        self.readout = tk.StringVar()
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row = 0, column = 0)
        self.north_frame = tk.Frame(self)
        self.north_frame.grid(row = 0, column = 1)
        self.center_frame = tk.Frame(self)
        self.center_frame.grid(row = 1, column = 1)
        self.south_frame = tk.Frame(self)
        self.south_frame.grid(row = 2, column = 1)
        self.cal_frame_list = []
        self.cal_text_list = []
        self.emp_list = ["Michael McDonnal", "Sean Ruhs", "Heidi Kloth", "Joe Shmo"]
        self.prompt_to_save = False

        self.previous_month_btn = tk.Button(self.north_frame, text = "Previous Month", command = lambda: self.get_pre_or_next_month_cal("pre"))
        self.previous_month_btn.grid(row = 0, column = 0)
        self.next_month_btn = tk.Button(self.north_frame, text = "Next Month", command = lambda: self.get_pre_or_next_month_cal("next"))
        self.next_month_btn.grid(row = 0, column = 1)
        self.month_label = tk.Label(self.north_frame, text = "")
        self.month_label.grid(row = 1, column = 0, columnspan = 2)

        self.save_notes_btn = tk.Button(self.left_frame, text = "Save", command = self.save_notes)
        self.save_notes_btn.grid(row = 0, column = 0)
        self.enable_disable_btn = tk.Button(self.left_frame, text = "Enable/Disable Notes", command = self.enable_disable_edit_of_day_notes)
        self.enable_disable_btn.grid(row = 1, column = 0)

        self.date_label = tk.Label(self.south_frame, textvariable = self.readout, padx = 10, pady = 10, anchor = "w")
        self.date_label.grid(row = 0, column = 0, sticky = "nsew")

        self.readout.set("Today is {} the {}, {} {}.".format(self.get_weekday(self.current_weekday_number),
                                            self.get_day_suffix(self.current_day),
                                            self.get_month(self.current_month_number),
                                            self.current_year,
                                            self.current_day))
        
        self.check_if_file_exist_for_year(self.current_year, self.current_month_number)

    def get_day_suffix(self, x):
        if x in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30]:
            return "{}{}".format(x, "th")
        if x in [1,21,31]:
            return "{}{}".format(x, "st")
        if x in [2,22]:
            return "{}{}".format(x, "nd")
        if x in [3,23]:
            return "{}{}".format(x, "rd")

    def get_pre_or_next_month_cal(self, pn):

        if self.prompt_to_save == True:
            answer = messagebox.askquestion("Save manager", "You are attempting to move to a different calendar month without saving. Would you like to save before moving on?")
            if answer =="yes":
                self.save_notes()
                self.prompt_to_save = False
            else:
                self.prompt_to_save = False

        self.center_frame.destroy()
        self.center_frame = tk.Frame(self)
        self.center_frame.grid(row = 1, column = 1)
        self.cal_frame_list = []
        self.cal_text_list = []

        if pn == "pre":
            self.current_selected_month -= 1
        else:
            self.current_selected_month += 1

        if self.current_selected_month == 0:
            self.current_selected_month = 12
            self.current_selected_year -= 1
        if self.current_selected_month == 13:
            self.current_selected_month = 1
            self.current_selected_year += 1

        self.check_if_file_exist_for_year(self.current_selected_year, self.current_selected_month)

    def check_if_file_exist_for_year(self, year_choice, month_choice):
        if os.path.exists("./DateData/{}records".format(year_choice)):
            self.create_calendar_interface(year_choice, month_choice)
        else:
            working_year = str(self.current_selected_year)
            with open("./DateData/RecordsTemplet","r") as data:
                jdata = json.load(data)
                jdata["{}".format(working_year)] = jdata.pop("0000")
                
            with open("./DateData/{}records".format(working_year),"w") as data:
                json.dump(jdata, data, indent = 4, separators = (',', ': '))
            self.prompt_to_save = False
            self.create_calendar_interface(year_choice, month_choice)
                
                
    def create_calendar_interface(self, year_choice, month_choice):
        self.center_frame.destroy()
        self.center_frame = tk.Frame(self)
        self.center_frame.grid(row = 1, column = 1)
        self.month_label.config(text = self.get_month(month_choice))
        days_in_month = calendar.monthrange(year_choice, month_choice)[1]
        for i in range(7):
            if i == 6:
                tk.Label(self.center_frame, text = self.get_weekday(i)).grid(row = 0, column = 0)
            else:
                tk.Label(self.center_frame, text = self.get_weekday(i)).grid(row = 0, column = i+1)
        rw = 1

        with open("./DateData/{}records".format(year_choice),"r") as data:
            jdata = json.load(data)
            for i in range(days_in_month):
                weekday_column = (dt.date(year_choice, month_choice, i+1).weekday())
                if weekday_column == 6:
                    rw += 1
                    weekday_column = 0
                else:
                    weekday_column += 1
                self.cal_frame_list.append(tk.Frame(self.center_frame))
                self.cal_frame_list[i].grid(row = rw, column = weekday_column)
                tk.Button(self.cal_frame_list[i], text = self.get_day_suffix((i+1)),
                          command = lambda x = year_choice, y = month_choice, z = (i+1): self.appointment_manager(x, y, z)).grid(sticky = "ew")
                self.cal_text_list.append(tk.Text(self.cal_frame_list[i], width = 15, height = 4, background = "#{:02x}{:02x}{:02x}".format(200, 200, 200)))
                self.cal_text_list[i].grid()
                self.cal_text_list[i].bind('<Key>', self.is_text_edited)
                self.cal_text_list[i].bind('<Control-s>', self.save_notes)

                if str(year_choice) in jdata:
                    year_notes = jdata[str(year_choice)]
                    if (self.get_month(month_choice)) in year_notes:
                            day_notes = year_notes[self.get_month(month_choice)]
                            for x in day_notes:
                                if x == str(i+1):
                                    self.cal_text_list[i].delete(1.0, "end-1c")
                                    self.cal_text_list[i].insert("end-1c", day_notes[x])
                                    self.cal_text_list[i].see("end-1c")
                                    self.cal_text_list[i].config(state="disabled")
    
    def enable_disable_edit_of_day_notes(self):
        for text in self.cal_text_list:
            if text["state"] == "disabled":
                text["state"] = "normal"
            else:
                text["state"] = "disabled"
    
    def appointment_manager(self, year, month, day):
        if self.appointment_manager_exist == None:
            self.appmanager = tk.Toplevel(self)
            self.appmanager.geometry('+{}+{}'.format(self.parent.winfo_x()+10, self.parent.winfo_y()+30))
            tk.Label(self.appmanager, text = "{}  {}  {}".format(year, month, day)).grid()
            self.dropval = tk.StringVar()
            self.dropval.set(self.emp_list[0])
            self.dropmenu = tk.OptionMenu(self.appmanager, self.dropval,*self.emp_list)
            self.dropmenu.grid()
            tk.Button(self.appmanager, text = "Close", command = self.close_appointment_manager).grid()
            self.appointment_manager_exist = "active"
            self.appmanager.attributes("-topmost", True)
            self.appmanager.protocol("WM_DELETE_WINDOW", self.close_appointment_manager)
            
    def move_me(self, event):
        if self.appointment_manager_exist != None:
            self.appmanager.geometry('+{}+{}'.format(self.parent.winfo_x()+10, self.parent.winfo_y()+30))
            
    def close_appointment_manager(self):
        self.appmanager.destroy()
        self.appmanager = None
        self.appointment_manager_exist = None

    def save_notes(self, event = None):
        working_year = str(self.current_selected_year)
        with open("./DateData/{}records".format(working_year),"r") as data:
            jdata = json.load(data)
            if working_year in jdata:
                sub_dict = jdata[working_year]
                sub_sub_dict = sub_dict[self.get_month(self.current_selected_month)]
                for i in self.cal_text_list:
                    sub_sub_dict[str((self.cal_text_list.index(i)+1))] = i.get(1.0, "end-1c")
                
        with open("./DateData/{}records".format(working_year),"w") as data:
            json.dump(jdata, data, indent = 4, separators = (',', ': '))
        self.prompt_to_save = False

        messagebox.showinfo("Notice Box", "Save complete!")

    def is_text_edited(self, event):
        if self.prompt_to_save == False:
            self.prompt_to_save = True
            
    def get_month(self,month):
        month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        return month_names[month-1]

    def get_weekday(self, day):
        weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        return weekdays[day]

    def status_clock(self):
        self.status_e.config(text ="{}".format(strftime("%H:%M:%S")))
        self.status_e.after(200, lambda: self.status_clock())


if __name__ == "__main__":
    root = tk.Tk()
    MyApp = MintApp(root)
    tk.mainloop()
