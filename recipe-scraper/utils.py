import unicodedata

vulgar_fractions = {
    "\u00BC": 1 / 4,  # ¼
    "\u00BD": 1 / 2,  # ½
    "\u00BE": 3 / 4,  # ¾
    "\u2150": 1 / 7,  # ⅐
    "\u2151": 1 / 9,  # ⅑
    "\u2152": 1 / 10,  # ⅒
    "\u2153": 1 / 3,  # ⅓
    "\u2154": 2 / 3,  # ⅔
    "\u2155": 1 / 5,  # ⅕
    "\u2156": 2 / 5,  # ⅖
    "\u2157": 3 / 5,  # ⅗
    "\u2158": 4 / 5,  # ⅘
    "\u2159": 1 / 6,  # ⅙
    "\u215A": 5 / 6,  # ⅚
    "\u215B": 1 / 8,  # ⅛
    "\u215C": 3 / 8,  # ⅜
    "\u215D": 5 / 8,  # ⅝
    "\u215E": 7 / 8,  # ⅞
    "\u215F": 1,  # ⅟
}


# Converts string to flow and returns as a range
# Returns [lower, upper]
def covert_float(string):
    # String is null or empty so return None
    if not string:
        return None, None

    # Clean up the string
    string = "".join(
        [char for char in string if not unicodedata.category(char).startswith("L")]
    )  # Remove all letters from string
    string = string.strip()  # Remove leading and trailing whitespace
    string = string.replace("–", "-")  # Replace en dash with hyphen

    # Naive assumption that string is float
    try:
        return float(string), float(string)
    except ValueError:
        pass

    # String is just a singular vulgar fraction
    if string in vulgar_fractions:
        return vulgar_fractions[string], vulgar_fractions[string]

    # String is a range
    if len(string.split("-")) == 2:
        lower, upper = string.split("-")
        lower, upper = lower.strip(), upper.strip()
        # If bounds are singular vulgar fractions get the values
        if lower in vulgar_fractions:
            lower = vulgar_fractions[lower]
        if upper in vulgar_fractions:
            upper = vulgar_fractions[upper]
        # If bounds are mixed fractions get the values
        if (
            isinstance(lower, str)
            and lower[:1].isdigit()
            and lower[-1] in vulgar_fractions
        ):
            lower = float(lower[:1]) + vulgar_fractions[lower[-1]]
        if (
            isinstance(upper, str)
            and upper[:1].isdigit()
            and upper[-1] in vulgar_fractions
        ):
            upper = float(upper[:1]) + vulgar_fractions[upper[-1]]
        # Return bounds
        return float(lower), float(upper)

    # String is a number followed by a vulgar fraction with no spacing
    if string[:1].isdigit() and string[-1] in vulgar_fractions:
        return (
            float(string[:1]) + vulgar_fractions[string[-1]],
            float(string[:1]) + vulgar_fractions[string[-1]],
        )

    return float(string), float(string)
