def more(text, max, more="..."):
    return text if len(text) <= max else text[:max] + more