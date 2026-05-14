# ==========================================
# ROUTING
# ==========================================
if st.session_state.logged_in:

    main_app()

else:

    if st.session_state.show_register:

        show_register()

    else:

        show_login()
