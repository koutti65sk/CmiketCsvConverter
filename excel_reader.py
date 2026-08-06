def get_hyperlinks(ws, header_name):
    header = {c.value:i+1 for i,c in enumerate(ws[1])}
    if header_name not in header:
        return []
    col = header[header_name]
    links=[]
    for r in range(2, ws.max_row+1):
        cell = ws.cell(r,col)
        if cell.hyperlink:
            links.append(cell.hyperlink.target)
        else:
            links.append("")
    return links