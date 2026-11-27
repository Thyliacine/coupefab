# Three CoupeFab logo icon concepts (32x32 viewBox). Each fn(bg, fg, acc) -> inner SVG.
def arc(bg="#15191c", fg="#f4f2ec", acc="#ff5a1f"):
    # A — "Arc de coupe": a C traced by a torch; the spark is the cut finishing.
    return (f'<rect width="32" height="32" rx="8" fill="{bg}"/>'
            f'<path d="M22.6 10.1A8.6 8.6 0 1 0 22.6 21.9" fill="none" stroke="{fg}" stroke-width="3.4" stroke-linecap="round"/>'
            f'<circle cx="23.2" cy="22.4" r="2.5" fill="{acc}"/>'
            f'<path d="M26.3 23.6l2.1.9M25.4 25.6l1.3 1.9M24 26.4l.3 2.1" stroke="{acc}" stroke-width="1.3" stroke-linecap="round"/>')

def slash(bg="#15191c", fg="#f4f2ec", acc="#ff5a1f"):
    # B — "Tôle tranchée": a plate sliced by a glowing kerf; the two parts separate.
    return (f'<rect width="32" height="32" rx="8" fill="{bg}"/>'
            f'<path d="M7 7h15.2L9.4 24.6H7z" fill="{fg}"/>'
            f'<path d="M25 25H9.8L22.6 7.4H25z" fill="{fg}" opacity=".55"/>'
            f'<path d="M23.4 6.2L8.6 26" stroke="{acc}" stroke-width="1.8" stroke-linecap="round"/>'
            f'<circle cx="8.6" cy="26" r="2.1" fill="{acc}"/>')

def bend(bg="#15191c", fg="#f4f2ec", acc="#ff5a1f"):
    # C — "Pli CF": C and F drawn as one bent sheet-metal profile, laser dot at the end.
    return (f'<rect width="32" height="32" rx="8" fill="{bg}"/>'
            f'<path d="M14.5 8.5H10a2.5 2.5 0 0 0-2.5 2.5v10a2.5 2.5 0 0 0 2.5 2.5h4.5" fill="none" stroke="{fg}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M18 23.5V11a2.5 2.5 0 0 1 2.5-2.5H25M18 16h5" fill="none" stroke="{fg}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="25.4" cy="16" r="2.2" fill="{acc}"/>')

OPTS = [("A", "Arc de coupe", arc), ("B", "Tôle tranchée", slash), ("C", "Pli CF", bend)]

def svg(fn, size=None, **kw):
    s = f' width="{size}" height="{size}"' if size else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"{s}>{fn(**kw)}</svg>'
