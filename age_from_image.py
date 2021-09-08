import argparse
import cv2
import datetime
from PIL import Image

from get_date_from_image import find_date_from_image


def age_recognition(img_name):
    path = f'./photo/{img_name}'  # img_name
    try:
        img = Image.open(path)
    except ValueError:
        return ValueError
    years_from_image = find_date_from_image(img)
    birth_year = min(years_from_image)
    # print(birth_year)
    now = datetime.datetime.now()
    # print(now.year)
    return now.year - birth_year


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_name", type=str, required=True)
    parser.add_argument("--path", type=str, default="./photo")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    image_name = args.image_name
    result = age_recognition(image_name)
    print(result, "years old")
    full_image_name = f'./photo/{image_name}'
    image = cv2.imread(full_image_name)
    cv2.imshow("result: " + str(result) + " years old", image)
    cv2.waitKey(0)
