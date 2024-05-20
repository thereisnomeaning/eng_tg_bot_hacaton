def get_markdownv2_text(input_text):
    output_text = ''
    for i in input_text:
        if i in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
            output_text += "\\" + i
        else:
            output_text += i
    return output_text