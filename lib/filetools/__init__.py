def get_file_types(format):
    if format == "jpeg":
        return "*.jpg", "*.jpeg", "*.JPG", "*.JPEG"
    elif format == "data":
        return "*xls", "*.xlsx"
    else:
        return None