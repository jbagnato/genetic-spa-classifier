from enum import IntEnum


class Component(IntEnum):
#    OTHER = 1
    BLANK = 2
#    NONE = 3

    HEADER = 100  # could include search bar and logo
#    MENU_HORIZONTAL = 101
#    SIDE_MENU = 102
#    FILTERS_MENU = 103
    BANNER = 104 # news or promotion


    # BODY 200
    BIG_TITLE = 201
    ABOUT = 202 # How it works, main text
    PRODUCT_FEATURES = 203  # Main feature, can be 2-4 images with text
#    PRODUCT_SCREENSHOTS = 204  # images inside screen, tablet or mobile
#    TEXT_PARAGRAPH = 205
#    BIG_BUTTONS = 206  # may be to redirect to categories or other sections
#    QUOTE = 207  #

#    VIDEO = 301
    BIG_IMAGE = 302  # and/or slider
    IMAGE_GALLERY = 303  # may be recomended items, related, popular, trending
#    BADGES = 304

#    SUBSCRIPTION_FORM = 401
#    CONTACT_FORM = 402

#    TESTIMONIAL = 501  # and Reviews, Ratings
#    PRESS_OR_MEDIA = 502

#    CALL_TO_ACTION = 601

#    ABOUT_US = 701  # TEAM, who we are

#    PRICES = 801
#    PLANS = 802
#    FAQS = 803
#    TAGS = 804

    FOOTER = 900
#   SOCIAL_MEDIA_ICONS = 901
