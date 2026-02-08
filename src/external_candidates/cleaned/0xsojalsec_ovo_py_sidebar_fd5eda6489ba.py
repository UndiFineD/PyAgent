# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\app.py\components.py\sidebar_fd5eda6489ba.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\components\sidebar.py

import streamlit as st

from ovo import config, db, get_username

from ovo.app.utils.cached_db import get_cached_project_ids_and_names

from ovo.core.database.models import Project

from ovo.core.logic.project_logic import get_or_create_personal_project

from ovo.core.logic.user_settings_logic import get_or_create_user_settings


@st.fragment()
@st.dialog("Input new project name")
def create_project_dialog():
    author = get_username()

    project_name = st.text_input("Project name", placeholder="My Project")

    public = st.toggle(label="Public", value=True)

    st.caption(
        "Public projects are visible to all users with access to this app. "
        "Private projects are only visible to you"
        + (
            ", but are accessible by other users when shared via a link."
            if config.auth.allow_private_project_link_access
            else "."
        )
    )

    if st.button("Create project"):
        if project_name == "":
            st.error("Please provide a project name.")

            return

        if db.count(Project, name=project_name, public=True):
            st.error(f'Public project "{project_name}" already exists. Please choose another name.')

            return

        elif db.count(Project, name=project_name, author=author):
            st.error(f'You already have a private project named "{project_name}". Please choose another name.')

            return

        new_project = Project(name=project_name, author=author, public=public)

        db.save(new_project)

        st.session_state.new_project_name = project_name

        st.session_state.project = new_project

        st.rerun()

        return


def get_query_arg_project() -> Project | None:
    if project_id := st.query_params.get("project_id"):
        if not config.auth.allow_private_project_link_access and project_id not in get_cached_project_ids_and_names(
            username=get_username()
        ):
            st.error(f"Project URL **{project_id}** not accessible, redirecting to last project.")

            del st.query_params["project_id"]

            return None

        else:
            return db.get(Project, id=project_id)

    return None


def project_sidebar_component():
    dropdown_key = "project_dropdown"

    success_message = None

    if st.session_state.project is None:
        if project := get_query_arg_project():
            # Load project from URL query parameter

            success_message = f"Opened project from URL"

            st.session_state.project = project

        elif config.props.read_only:
            # In read-only mode, just select the first available project

            project_ids_and_names = get_cached_project_ids_and_names(username=get_username())

            if not project_ids_and_names:
                st.error(f"No projects available to user {get_username()} in read-only mode.")

                st.stop()

            st.session_state.project = db.get(Project, id=list(project_ids_and_names.keys())[0])

        else:
            # Restore last selected project or select personal project

            user_settings = get_or_create_user_settings()

            if user_settings.last_project_id and (project := db.get(Project, user_settings.last_project_id)):
                success_message = f"Resuming in project **{project.name}**"

                st.session_state.project = project

            else:
                st.session_state.project = get_or_create_personal_project()

    project_ids_and_names = get_cached_project_ids_and_names(
        username=get_username(), extra_project_ids=[st.session_state.project.id]
    )

    project_ids = sorted(project_ids_and_names.keys(), key=lambda x: project_ids_and_names[x].lower())

    # Get dropdown value from session ID directly (or from session_state.project when dropdown is not yet rendered)

    selected_project_id = st.session_state.get(dropdown_key, st.session_state.project.id)

    if st.session_state.new_project_name:
        # Select project if it was just created

        success_message = f'Project "**{st.session_state.new_project_name.strip()}**" created'

        st.session_state.new_project_name = None

        # force selecting the new project in the dropdown

        selected_project_id = st.session_state.project.id

    st.sidebar.selectbox(
        "**Project**",
        format_func=project_ids_and_names.get,
        key=dropdown_key,
        options=project_ids,
        index=project_ids.index(selected_project_id),
    )

    # Hack needed to hide tooltips because they disrupt clicking on the dropdown item (as of Dec 2024)

    dropdown_style = """

    <style>

    .stTooltipContent {

    pointer-events: none;

    }

    </style>

    """

    st.markdown(dropdown_style, unsafe_allow_html=True)

    if selected_project_id != st.session_state.project.id:
        # Update selected project when changed

        selected_project = db.get(Project, id=selected_project_id)

        success_message = f"Selected project **{selected_project.name}**"

        st.session_state.project = selected_project

        if not config.props.read_only:
            user_settings = get_or_create_user_settings()

            user_settings.last_project_id = selected_project.id

            db.save(user_settings)

    if selected_project_id != st.query_params.get("project_id"):
        st.query_params["project_id"] = selected_project_id

    if config.props.read_only:
        st.sidebar.info("Read-only mode")

    elif st.sidebar.button(":material/add: Create new project"):
        create_project_dialog()

    if success_message:
        st.sidebar.success(success_message)
