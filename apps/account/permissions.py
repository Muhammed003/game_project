# Define permissions for different roles
# ROLE_PERMISSIONS = {
#     "chef": ["can_access_report_notebook", "can_access_close_shift_waitress", ],
#     "administrator": ["can_access_all"],
#     "waitress": ["can_access_waitress_page"],
#     # Add more roles and permissions as needed
# }

# Define specific views permissions
VIEW_PERMISSIONS = {
    # CHEF PERMISSIONS
    "AdministrationPageView": ["administrator", "chef", "admin"],
    "AudioAddPageView": ["administrator", "chef", "admin"],
    "UserListView": ["administrator", "chef", "admin"],
    "UserCreateView": ["administrator", "chef", "admin"],
    "UserUpdateView": ["administrator", "chef", "admin"],
    "UserDeleteView": ["administrator", "chef", "admin"],

}
