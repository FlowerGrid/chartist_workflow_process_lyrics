import csv
import xml.etree.ElementTree as ET


def add_section_markers_to_lyric_xml(lyric_xml, guide_sheet):
    # Open csv and load information into a list of dictionaries
    with open(guide_sheet, newline='') as f:
        reader = csv.DictReader(f)
        sections = [row for row in reader]

    # Open xml file

    # Copy header
    with open(lyric_xml, 'r', encoding='UTF-8') as original_file:
        # Read the declaration and doctype declaration lines
        declaration = original_file.readline()
        doctype = original_file.readline()

    # Parse xml file
    lyric_tree = ET.parse(lyric_xml)    
    lyric_root = lyric_tree.getroot()

    #  Create a hash for measures
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
    lyric_tree.write(filename)


def insert_section_marker(measure, marker_text):
    # print(measure.get('number'))
    new_marker_element = ET.Element('direction')
    new_marker_element.set('placement', 'above')
    marker_child = ET.Element('direction-type')
    marker_grandchild = ET.Element('words')
    marker_grandchild.set('default-y', '76')
    marker_grandchild.set('relative-x', '-27')
    marker_grandchild.set('valign', 'top')
    marker_grandchild.text = marker_text
    marker_child.append(marker_grandchild)
    new_marker_element.append(marker_child)
    ET.indent(new_marker_element, space='\t', level=3)
    measure.insert(1, new_marker_element)
    if len(measure) > 2:
        measure[1].tail = '\n' + ('\t'*3)


    

if __name__ == '__main__':
    lyric_xml = 'I Will Rejoice (#34961) LOGIC score asXML.xml'
    guide_sheet = './Workflow Guide Sheet.csv'
    add_section_markers_to_lyric_xml(lyric_xml, guide_sheet)