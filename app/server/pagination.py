def get_announcements_pag(announcements, offset = 0, per_page = 10):
    return announcements[offset: offset + per_page]
