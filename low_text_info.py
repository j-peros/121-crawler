def low_textual_content(tokenLst: list, tagLst: list, *, decimal_percentage:int = 0.95) -> bool:
    """ Low textual content can be described as 97% - 3% html-text ratio """
    len_tokens = len(tokenLst)
    len_html = len(tagLst)
    total_len = len(tokenLst) + len(tagLst)
    if (len_tokens / total_len) > decimal_percentage: # tokens make up > decimal_percentage (i.e. 0.97) of all text
        return False
    elif (len_html / total_len) > decimal_percentage: # html makes up > decimal_percentage (i.e. 0.97) of all text
        return False
    else: # can be considered non-low textual content
        return True