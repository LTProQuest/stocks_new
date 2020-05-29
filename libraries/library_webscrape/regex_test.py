import re
text = """NameRichard Taylor

    AddressEaling, London, tw20 8jn

    15 lqtimer Hill
    """

postcode_regex = re.compile(r'[\d]{1,2} +[a-zA-Z]{1,15} +(?:Park|Road|Hill|Lane|London|Green|Avenue|Green|Way)')


#re.compile(r'[A-Za-z]{1,2}[0-9][0-9A-Za-z]? [0-9][A-Za-z]{2}')
#re.compile("\+? {0,2}\d+ {0,2}[(-]?\d(?:[ \d]*\d)?[)-]? {0,2}\d+[/ -]?\d+[/ -]?\d+(?: *- *\d+)?")

#"Park,|Road,|Hill,|Lane,|London,|Avenue,|Essex,|Green,|Way|Bristol,|Manchester,"
print(re.findall(postcode_regex, text))

