import os
import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator
from xml.dom import minidom

# Base strings.xml file (English)
INPUT_FILE = 'strings.xml'

# List of language codes to translate into
TARGET_LANGUAGES = ['hi' ]
#TARGET_LANGUAGES = ['ar', 'az', 'bg', 'ca', 'ckb', 'cs', 'da', 'de', 'el', 'eo', 'es', 'eu', 'fa', 'fi', 'fr', 'gl', 'hr', 'hu', 'hi', 'it', 'ja', 'km', 'ko', 'lt', 'nl', 'pl', 'pt', 'ro', 'ru', 'sk', 'sq', 'sr', 'sv', 'ta', 'te', 'tr', 'uk', 'vi']

# Output root directory (same level as script by default)
OUTPUT_DIR = os.getcwd()

# Parse input XML
tree = ET.parse(INPUT_FILE)
root = tree.getroot()

# Extract original strings
strings = [(elem.attrib['name'], elem.text) for elem in root.findall('string') if elem.text]

# Translate and write for each language
for lang in TARGET_LANGUAGES:
    translated_root = ET.Element("resources")

    for name, text in strings:
        translated_text = GoogleTranslator(source='auto', target=lang).translate(text)
        elem = ET.SubElement(translated_root, "string", {"name": name})
        elem.text = translated_text + '\n'  # Add newline after each translation

    # Pretty print XML with newlines
    rough_string = ET.tostring(translated_root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="    ")

    # Output directory for this language (e.g. "ar", "es", etc.)
    lang_dir = os.path.join(OUTPUT_DIR, f"values-{lang}")
    os.makedirs(lang_dir, exist_ok=True)

    # Write to strings.xml in respective language directory
    output_file = os.path.join(lang_dir, "strings.xml")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

    print(f"✔ Translated: {lang} -> {output_file}")

