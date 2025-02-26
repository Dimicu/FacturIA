import streamlit as st

def side_bar_button_style(text):
    EstiloBoton = """<style>
                .my-sidebar-button {
                    background-color: #F0F2F6;
                    color: black;
                    text-align: left;
                    font-size: 16px;
                    border: none;
                    border-radius: 8px;
                    width: 100%;
                    transition: background-color 0.3s ease;
                }
                .my-sidebar-button:hover {
                    background-color: #dcdde0;
                }
            </style>"""
    button_html = f'''
            {EstiloBoton}
            <button class="my-sidebar-button">{text}</button>
        '''
    return button_html

def side_bar_user_style(username):
    EstiloSideBarUser = f"""<style>
            .sidebar-title {{
                text-align: left;
                font-size: calc(44px - {len(username) * 0.5}px);
                font-weight: bold;
                margin-bottom: 20px;
                word-wrap: break-word;
                transition: font-size 0.3s ease;
            }}
        </style>"""
    sidebar_title_html = f'''
        {EstiloSideBarUser}
        <div class="sidebar-title">{username}</div>
    '''
    return sidebar_title_html

def render_sidebar():
    user = "User"
    user_picture = "https://imgs.search.brave.com/JAHeWxUYEwHB7KV6V1IbI9oL7wxJwIQ4Sbp8dHQL09A/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMjAx/MzkxNTc2NC9waG90/by91c2VyLWljb24t/aW4tZmxhdC1zdHls/ZS5qcGc_cz02MTJ4/NjEyJnc9MCZrPTIw/JmM9UEotMnZvUWZh/Q3hhZUNsdzZYYlVz/QkNaT3NTTjlIVWVC/SUg1Qk82VmRScz0"

    with st.sidebar:
        col1, col2 = st.columns(2)
        col1.image(user_picture, width=100)
        col2.markdown(side_bar_user_style(user), unsafe_allow_html=True)
        st.divider()

