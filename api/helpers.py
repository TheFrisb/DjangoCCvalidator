def get_card_type(pan):
    if pan.startswith("34") or pan.startswith("37"):
        return "American Express"
    return "Unknown"


def is_valid_pan_length(pan):
    pan = clean_pan(pan)
    if not pan.isdigit():
        return False
    
    if not 16 <= len(pan) <=19:
        return False
    
    return True
    
def is_valid_pan_luhn(pan):
    digits = [int(digit) for digit in clean_pan(pan)]
    checksum = 0    
    
    for i in range(len(digits) - 2, -1, -2):
        double_digit = digits[i] * 2
        if double_digit > 9:
            double_digit -= 9
        checksum += double_digit

    for i in range(len(digits) - 1, -1, -2):
        checksum += digits[i]   
        
    return checksum % 10 == 0

def clean_pan(pan):
    pan = pan.replace(" ", "")
    pan = pan.replace("-", "")
    return pan