from pathlib import Path
import streamlit as st
from streamlit.source_util import (
    page_icon_and_name, 
    calc_md5, 
    get_pages,
    _on_pages_changed
)

def delete_page(main_script_path_str, page_name):
    """
    delete page from app

    Args:
        main_script_path_str: main page (e-g app)
        page_name: Page want to delete (e-g Analyze)

    Returns:
        None
    """
    #get all pages
    current_pages = get_pages(main_script_path_str)

    #iterate over all pages and del if desire page found
    for key, value in current_pages.items():
        if value['page_name'] == page_name:
            del current_pages[key]
            break
        else:
            pass

    #refresh the pages config
    _on_pages_changed.send()
    
def add_page(main_script_path_str, page_name):
    """
    add page in app

    Args:
        main_script_path_str: main page (e-g app)
        page_name: Page want to delete (e-g Analyze)

    Returns:
        None
    """
    #get all pages
    pages = get_pages(main_script_path_str)

    main_script_path = Path(main_script_path_str)
    pages_dir = main_script_path.parent / "pages"
    script_path = [f for f in pages_dir.glob("*.py") if f.name.find(page_name) != -1][0]
    script_path_str = str(script_path.resolve())
    pi, pn = page_icon_and_name(script_path)

    psh = calc_md5(script_path_str)
    #add new page config
    pages[psh] = {
        "page_script_hash": psh,
        "page_name": pn,
        "icon": pi,
        "script_path": script_path_str,
    }
    #refresh the page config
    _on_pages_changed.send()