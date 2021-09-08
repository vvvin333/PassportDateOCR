import pytesseract
import re

from utils import rescale_image, threshold, crop_img, find_bbox, remove_noise_and_smooth


def find_date(text, regex=r"(19|20)\d{2}"):
    """
    default regex: for year 1900-2099
    regex samples for date:
    regex = r"((19|20)?\d{1,2}\s?[-/]\s?\d{1,2}\s?[-/]\s?(19|20)?\d{2})|"\
            r"((Jan|Feb|Mar|Apr|May|Jun|June|Jul|Aug|Sept|Sep|Oct|Nov|Dec)"\
            r"\s?\d{1,2}\s?[,']?\s?(19|20)?\d{2})|(\d{1,2}\s?[-/]?\s?"\
            r"(Jan|Feb|Mar|Apr|May|Jun|June|Jul|Aug|Sept|Sep|Oct|Nov|Dec)"\
            r"\s?[',-/]?\s?(19|20)?\d{1,2})"
    regex = r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)"\
            r"(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|"\
            r"^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]"\
            r"|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]"\
            r"|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]"\
            r"|[2-9]\d)?\d{2})"
    regex = r"(19|20)\d{2}"
    """
    pattern = re.compile(regex, flags=re.IGNORECASE)
    matches = list(re.finditer(pattern, text))
    if len(matches) == 0:
        return None
    result = [int(match.group()) for match in matches]
    return result


def find_date_from_image(img):
    # preprocessing image
    img = rescale_image(img)
    thresh = threshold(img)
    _, bbox = find_bbox(thresh)
    img = crop_img(img, bbox)
    final_img = remove_noise_and_smooth(img)

    # finding text in image
    text = pytesseract.image_to_string(final_img)

    # searching for dates
    date = find_date(text)
    return date
