import re

def string_numeric_extractor(text):
    try:
        time_pattern = r"\d+:\d+"
        other_pattern = r".*"

        time_part = re.findall(time_pattern, text)
        other_part = re.findall(other_pattern, text)

        other_part = re.sub(time_pattern, "", other_part[0])

        formatted_time = ":".join(time_part)
        formatted_other = other_part.strip()
        if ' ()' in formatted_other:
            formatted_other = formatted_other.replace(' ()', '')
        if '()' in formatted_other:
            formatted_other = formatted_other.replace('()', '')
        return formatted_time, formatted_other
    except:
        return text, text