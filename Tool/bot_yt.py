import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from sqlalchemy import null
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW
import tkinter as tk
from tkinter import ttk
import os
import threading
from tkinter import messagebox

link = ""
filename = "output.csv"

def get_link():
    global link
    link = text.get("1.0", tk.END).replace(' ','')

def main_task():
    get_link()
    list_in = link.split("\n")
    if link == "":
        return messagebox.showinfo("Information", "Not Link !!!")
    else:

        
        if not os.path.exists(filename):
            with open(filename, "w", encoding='utf-8') as file_output:
                headers = ['YT Channel', 'Subscribers', 'Views', 'Videos']
                writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n', fieldnames=headers)
                writer.writeheader()
        
        alpha = ""
        i = 0
        # try:
        for item in list_in :
            item = item + "/videos"
            # print("item", item)
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            serv = Service(ChromeDriverManager().install())
            serv.creationflags = CREATE_NO_WINDOW

            driver = webdriver.Chrome(service=serv, options=options)
            driver.get(item)

            channel = driver.find_element(By.ID, "channel-name")
            channel_Youtube = channel.text
            # print(channel_Youtube)

            subscribers = driver.find_element(By.ID, "subscriber-count")
            subscribers_Youtube = subscribers.text.replace('subscribers', '')
            if str(subscribers_Youtube).find("M") != -1:
                subscribers_Youtube = subscribers_Youtube.replace('M', '')
                subscribers_Youtube = 1000000 * float(subscribers_Youtube)
            if str(subscribers_Youtube).find("K") != -1:
                subscribers_Youtube = subscribers_Youtube.replace('K', '')
                subscribers_Youtube = 1000 * float(subscribers_Youtube)
            # print(subscribers_Youtube)
            mix_views_title = ""
            video_list = driver.find_elements(By.ID, 'dismissible')
            for video in video_list:
                video_name = video.find_element(By.ID, 'video-title-link')
                video_name_Youtube = video_name.text.replace(',', '')
                # print(video_name_Youtube)
                views = video.find_element(By.ID, "metadata-line")
                views = views.text.split(" ")
                views_Youtube = views[0]
                if str(views_Youtube).find("M") != -1:
                    views_Youtube = views_Youtube.replace('M', '')
                    views_Youtube = 1000000 * float(views_Youtube)
                if str(views_Youtube).find("K") != -1:
                    views_Youtube = views_Youtube.replace('K', '')
                    views_Youtube = 1000 * float(views_Youtube)
                views_Youtube = str(views_Youtube)
                # print(views_Youtube)
                link_video = video.find_element(By.TAG_NAME, 'a').get_attribute('href')
                # print(link_video)
                mix_views_title = mix_views_title + views_Youtube + ',' + video_name_Youtube + ',' + link_video + '\n' + ' ,' + ' ,'

            csvData = '{channel_Youtube},{subscribers_Youtube},{mix_views_title}'.format(
                channel_Youtube=channel_Youtube,
                subscribers_Youtube=subscribers_Youtube,
                mix_views_title=mix_views_title,
            )

            # print(csvData)
            with open("output.csv", "a", encoding='utf-8') as file_output:
                file_output.write(csvData + '\n')
            driver.close()
            if item != alpha:
                progress = 100 * (i + 1) / (len(list_in) -1)
                progress_var.set(int(progress))
                root.update()
                alpha = item
                i = i + 1
                if progress == 100:
                    return messagebox.showinfo("Information", "The process is completed successfully!")
            else:
                messagebox.showinfo("Information", "The process is completed successfully!")
                break
            if str(item).replace(' ', '') == '':
                messagebox.showinfo("Information", "The process is completed successfully!")
                break
    # except:
    #     messagebox.showinfo("Information", "The process is ERROR!")

def start_task():
    thread = threading.Thread(target=main_task)
    thread.start()


root = tk.Tk()
root.title("Youtube Crawler")
height = 20
width = 65

text = tk.Text(root, height=height, width=width)
text.grid()





main_frame = ttk.Frame(root, padding=(30, 30))
main_frame.grid()


progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=200, mode="determinate", variable=progress_var)
progress_bar.grid(row=0, column=0)

start_button = ttk.Button(main_frame, text="Start", command=start_task)
start_button.grid(row=1, column=0)

root.mainloop()
