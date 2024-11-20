"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""
    # The images to show.
    img: list[str]

    @rx.event
    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)


color = "rgb(107,99,246)"

def signup_default() -> rx.Component:
    return rx.container(
    rx.card(
        rx.vstack(
            rx.center(
                rx.image(
                    src="/logo.png",
                    width="29em",
                    height="8em",
                    border_radius="25%",
                ),
                rx.heading(
                    "Create an account",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Email address",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="user@reflex.dev",
                    type="email",
                    size="3",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Password",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.box(
                rx.checkbox(
                    "Agree to Terms and Conditions",
                    default_checked=True,
                    spacing="2",
                ),
                width="100%",
            ),
            rx.button("Register", size="3", width="100%"),
            rx.center(
                rx.text("Already registered?", size="3"),
                rx.link("Sign in", href="#", size="3"),
                opacity="0.8",
                spacing="2",
                direction="row",
            ),
            spacing="6",
            width="100%",
        ),
        size="4",
        width="100%",
    ),
    class_name="p-7"
)

def login_default() -> rx.Component:
    return rx.container(
        # rx.heading("Insightium", size="9",class_name="flex items-center justify-center bg-gradient-to-r from-[#4A00E0] to-[#8E2DE2] bg-clip-text text-transparent p-5 "),
        rx.card(
        rx.vstack(
            rx.center(
                rx.image(
                    src="/logo.png",
                    width="29em",
                    height="8em",
                    border_radius="25%",
                ),
                rx.heading(
                    "Sign in to your account",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Email address",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="user@reflex.dev",
                    type="email",
                    size="3",
                    width="100%",
                ),
                justify="center",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Password",
                        size="3",
                        weight="medium",
                    ),
                    rx.link(
                        "Forgot password?",
                        href="#",
                        size="3",
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.input(
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            rx.button("Sign in", size="3", width="100%"),
            rx.center(
                rx.text("New here?", size="3"),
                rx.link("Sign up", href="#", size="3"),
                opacity="0.8",
                spacing="2",
                direction="row",
            ),
            spacing="6",
            width="100%",
            
        ),
        size="4",
        
        width="100%",
        
    ),
    class_name="flex items-center justify-center "
    )

def about():
    return rx.container(
        
        rx.vstack(
            rx.image(
                    src="/logo.png",
                    width="29em",
                    height="8em",
                    border_radius="25%",
                ),
        rx.upload(
            
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                    
                ),
                rx.text(
                    "Drag and drop files here or click to select files"
                ),
            ),
            id="upload1",
            border=f"1px dotted {color}",
            padding="5em",
            border_radius="2em"
        ),
        rx.hstack(
            rx.foreach(
                rx.selected_files("upload1"), rx.text
            )
        ),
        rx.button(
            "Upload",
            on_click=State.handle_upload(
                rx.upload_files(upload_id="upload1")
            ),
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files("upload1"),
        ),
        rx.foreach(
            State.img,
            lambda img: rx.image(
                src=rx.get_upload_url(img)
            ),
        ),
        padding="5em",
    ),
        class_name="flex items-center justify-center "
                        )

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        #rx.color_mode.button(position="top-right"),
        rx.vstack( 
            rx.heading("INSIGHTIUM",class_name="flex items-center justify-center text-9xl p-0 m-0 font-bold bg-gradient-to-r from-[#4A00E0] to-[#8E2DE2] bg-clip-text text-transparent"),
            
            rx.text(
                "Don't Just Read, but rather chat with your documents",
                
                class_name="text-2xl font-bold bg-gradient-to-r from-blue-500 to-white bg-clip-text text-transparent"
            ),
            rx.flex(
            (rx.link(
                rx.button("SignUp"),
                href="/sign-up",
                is_external=True,
                class_name="hover:animate-pulse"
            ),
            rx.link(
                rx.button("Login"),
                href="/login",
                is_external=True,
                class_name="hover:animate-pulse "
            )),
            spacing="9",
            class_name=""
            ),
            spacing="5",
            class_name="flex items-center justify-center",
            min_height="85vh",
        ),
        
    )


app = rx.App(stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css",
    ],)
app.add_page(index)
app.add_page(about,route="/about")
app.add_page(login_default,route="/login")
app.add_page(signup_default,route="/sign-up")