"""
TODO:
    ✅ Build gui that will work with larger chartist workflow program
    - Add square brackets to represent chords in the LYRICS.txt file
"""

import csv
import os
import subprocess
from tkinter import *
import tkinter.filedialog as filedialog
import xml.etree.ElementTree as ET

def get_parent_directory(tk_root):

    project_path = filedialog.askdirectory(
    title='Select project location',
    message="Please choose the project's parent folder"
    )

    if project_path != '':
        create_lyric_window(tk_root, project_path)


def create_lyric_window(tk_root, project_path):
    # Project title
    title = os.path.basename(project_path)

    #  Build Gui
    width = 500
    height = 150

    lyric_window = Toplevel(tk_root)
    lyric_window.geometry(f'{width}x{height}')
    lyric_window.title(f'Process Lyrics {title}')
    lyric_window.grid_columnconfigure(0, weight=1)


    screen_width = lyric_window.winfo_screenwidth()
    screen_height = lyric_window.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/4) - (height/4)
    lyric_window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    # Frame
    main_frame = Frame(lyric_window, padx=5, pady=5)
    main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    main_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform='columns')

    markers_button = Button(main_frame, text="Write markers to xml", command=lambda: add_section_markers_to_lyric_xml(tk_root, project_path))
    markers_button.grid(row=0, column=0)

def add_section_markers_to_lyric_xml(tk_root, project_path):
    # Get lyric xml file
    title = os.path.basename(project_path)
    lyric_xml = os.path.join(project_path, 'Documents', 'Finale', 'Extractions', f'{title} LOGIC score asXML.xml')

    # Get guide sheet
    guide_sheet = os.path.join(project_path, 'Documents', 'Workflow Guide Sheet.csv')

    # Open csv and load information into a list of dictionaries
    with open(guide_sheet, newline='') as f:
        reader = csv.DictReader(f)
        sections = [row for row in reader]

    # Open xml file
    with open(lyric_xml, 'r', encoding='UTF-8') as original_file:
        # Read the declaration and doctype declaration lines
        declaration = original_file.readline()
        doctype = original_file.readline()

    # Parse xml file
    lyric_tree = ET.parse(lyric_xml)    
    lyric_root = lyric_tree.getroot()

    # Create a hash for measures
    measures = {}
    for m in lyric_root.findall('.//measure'):
        if m.get('number') is not None and int(m.get('number')) not in measures:
            measure_number = int(m.get('number'))
            measures[measure_number] = m

    # Iterate over sections and insert markers into xml
    for section in sections:
        measure_number = int(section['Measure'])
        measure = measures.get(measure_number)
        
        marker_text = section['Event']

    # Insert section marker to xml
        if '#' in section.get('Event'):
            insert_section_marker(measure, marker_text)

    # write the modified xml file
    filename = lyric_xml.replace('.xml', '') + '_w_section_markers.xml'
    root_string = ET.tostring(lyric_root, encoding='unicode')

    with open(filename, 'w') as output:
        output.write(declaration)
        output.write(doctype)
        output.write('\n')
        output.write(root_string)

    # Open the file in Finale
    subprocess.Popen(['open', '-a', 'Finale Demo', filename])


def write_brackets():
    ...


def insert_section_marker(measure, marker_text):
    # Add marker elements to measure
    new_marker_element = ET.Element('direction')
    new_marker_element.set('placement', 'above')
    marker_child = ET.Element('direction-type')
    marker_grandchild = ET.Element('words')
    marker_grandchild.set('default-y', '32')
    marker_grandchild.set('relative-x', '8')
    marker_grandchild.set('valign', 'top')
    marker_grandchild.text = marker_text
    marker_child.append(marker_grandchild)
    new_marker_element.append(marker_child)

    # Pretty print
    ET.indent(new_marker_element, space='\t', level=3)
    measure.insert(1, new_marker_element)
    if len(measure) > 2:
        measure[1].tail = '\n' + ('\t'*3)


if __name__ == '__main__':
    tk_root = Tk()
    go_button = Button(tk_root, text='Choose Project Folder', command= lambda: get_parent_directory(tk_root))
    go_button.pack()

    tk_root.mainloop()