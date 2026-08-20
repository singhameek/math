import reflex as rx


config = rx.Config(
    app_name="math_solver",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)