import os
import streamlit as st

def display_tree_images(trees_needed):
    #Tree Image: https://www.flaticon.com/free-icon/tree_7534964
    tree_image_path = "tree.png"
    #
    if os.path.exists(tree_image_path):
        num_rows = (trees_needed // 6) + (1 if trees_needed % 6 != 0 else 0)
        for i in range(num_rows):
            cols = st.columns(6)
            for j in range(6):
                tree_index = i * 6 + j
                if tree_index < trees_needed:
                    cols[j].image(tree_image_path, width=100)
                else:
                    break
    else:
        st.warning("Tree image not found.")
