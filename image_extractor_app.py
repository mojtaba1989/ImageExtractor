import tkinter as tk
from tkinter import Tk, messagebox, Button, Canvas
import ttk
from PIL import Image, ImageTk
import tkFileDialog
import os
import rosbag
from cv_bridge import CvBridge
import numpy as np
import cv2
import subprocess
import yaml
import sys
import base64
from io import BytesIO

logo_base64 = (
    b'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'
)

class master:
    topics = []
    file_path = ""


class APSRC_IMG_EXP:
    def __init__(self, root):
        self.root = root
        self.root.title("Rosbag Image Extract")
        self.root.geometry("500x300")

        self.image_label = tk.Label(root)
        self.image_label.pack()

        logo_data = base64.b64decode(logo_base64)
        logo_photo = ImageTk.PhotoImage(Image.open(BytesIO(logo_data)))

        self.logo_label = tk.Label(root, image=logo_photo)
        self.logo_label.image = logo_photo
        self.logo_label.pack()
        self.text_label_top = tk.Label(root, text="APSRC ROSBAG IMAGE\n EXTRACT TOOL", 
                                       font=("TimeNewRomans", 24, 'normal'), justify='center')
        self.text_label_top.pack()

        button_font = ("TimeNewRomans", 16, 'bold')
        open_button = tk.Button(root, text="Open ROSBAG", command=self.open_rosbag,
                                 font=button_font)
        open_button.place(x=160, y=200)

        self.text_label_fn = tk.Label(root, text="Mojtaba Bahramgiri - APSRC 2024",
                                       anchor="s")
        self.text_label_fn.place(x=250, y=280)

    def open_rosbag(self):
        file_path = tkFileDialog.askopenfile(defaultextension=".bag", filetypes=[("rosbag files", "*.bag")])
        master.file_path = file_path.name
        if master.file_path:
            self.root.destroy()
            ropic_select_root = tk.Tk()
            imgSeg_app = TopicSel(ropic_select_root)
            ropic_select_root.mainloop()
            
class TopicSel:
    def __init__(self, root):
        self.root = root
        self.root.title("Select topic(s)")
        self.bag = rosbag.Bag(master.file_path)
        all = self.read_topics()
        self.topics = []
        for topic, msg_type in all.items():
            if msg_type == "sensor_msgs/Image":
                self.topics.append(topic)
        if not self.topics:
            messagebox.showwarning("Error", "No Image Found in BAG File")
            self.root.destroy()
            master.clear()
            root = tk.Tk()
            app = APSRC_IMG_EXP(root)
            root.mainloop()
        row = 2
        for item in self.topics:
            temp = topic_checkbox(self.root, item, row)
            master.topics.append(temp)
            row += 1
        extract_button = Button(self.root, text="Extract", command=self.extract)
        extract_button.grid(row=row, column=2, padx=5, pady=5)

        extract_button = Button(self.root, text="Back", command=self.back)
        extract_button.grid(row=row, column=3, padx=5, pady=5)

    def read_topics(self):
        command = "rosbag info --yaml {}".format(master.file_path)
        result = subprocess.check_output(command, shell=True)
        bag_info = yaml.safe_load(result)
        topics_and_types = {entry['topic']: entry['type'] for entry in bag_info['topics']}
        return topics_and_types
    
    def back(self):
        self.root.destroy()
        master.topics = []
        root = tk.Tk()
        app = APSRC_IMG_EXP(root)
        root.mainloop()

    def extract(self):
        count = len([topic.enable for topic in master.topics if topic.enable])
        if count == 0:
            messagebox.showwarning("Error", "No topic has been selected!")
        else:
            response = messagebox.askokcancel("Continue", "{} topic has been selected\nWish to continue?".format(count))
            if response:
                total = 0
                progress_window = tk.Toplevel(self.root)
                progress_window.title("Processing...")
                for topic in master.topics:
                    if topic.enable:
                        count = self.bag.get_message_count(topic.topic)
                        total += count
                        counter = progress(progress_window, topic.topic, count)
                        self.extract_topic(topic, counter)
                progress_window.destroy()
                exit = messagebox.showinfo("Done!", "{} images extracted".format(total))              
            else:
                pass
    
    def extract_topic(self, topic_obj, counter_obj):
        if not topic_obj.enable:
            return False
        DIRECTORY = os.path.splitext(master.file_path)[0] + topic_obj.topic 
        try:
            os.makedirs(DIRECTORY)
        except OSError:
            pass
        image_topic = self.bag.read_messages(topic_obj.topic)
        DESCRIPTION = topic_obj.topic[1:].replace('/','_') + '_'
        for k, b in enumerate(image_topic):
            bridge = CvBridge()
            try:
                cv_image = bridge.imgmsg_to_cv2(b.message, desired_encoding="bgr8")
            except:
                cv_image = bridge.imgmsg_to_cv2(b.message, desired_encoding="passthrough")

            img_name = DESCRIPTION + str(b.timestamp) + '.png'
            cv2.imwrite(os.path.join(DIRECTORY, img_name), cv2.resize(cv_image, (960, 720)))
            counter_obj.update(k)
        return True

class progress:
    def __init__(self, master, topic, length):
        self.master = master
        self.length = length
        text = tk.Label(self.master, text=topic)
        text.pack(pady=10)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.master, variable=self.progress_var, length=300, mode='determinate')
        self.progress_bar.pack(pady=10)

    def update(self, i):
        progress_percentage = int(float(i) / (self.length -1) * 100)
        self.progress_var.set(progress_percentage)
        self.master.update_idletasks()

class topic_checkbox:
    def __init__(self, master, topic, id):
        self.topic = topic
        self.var = tk.BooleanVar()
        self.var.set(False)
        self.cbox = tk.Checkbutton(master, variable=self.var, command=self.toggle)
        self.cbox.grid(row=id, column=1, padx=5, pady=5)
        text = tk.Label(master, text=topic)
        text.grid(row=id, column=2, padx=5, pady=5, columnspan=2)
        self.enable = False

    def toggle(self):
        self.enable = True if self.var.get() else False





if __name__ == "__main__":
    root = tk.Tk()
    app = APSRC_IMG_EXP(root)
    root.mainloop()
   
