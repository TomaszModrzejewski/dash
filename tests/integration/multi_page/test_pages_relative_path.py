import dash
from dash import Dash, dcc, html


def get_app(app):
    app = app

    dash.register_page(
        "multi_layout1",
        layout=html.Div("text for multi_layout1", id="text_multi_layout1"),
        path="/",
        title="Supplied Title",
        description="This is the supplied description",
        name="Supplied name",
        image="birds.jpeg",
        id="multi_layout1",
    )
    dash.register_page(
        "multi_layout2",
        layout=html.Div("text for multi_layout2", id="text_multi_layout2"),
        path="/layout2",
        id="multi_layout2",
    )

    app.layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Link(
                            f"{page['name']} - {page['path']}",
                            id=page["id"],
                            href=page["relative_path"],
                        )
                    )
                    for page in dash.page_registry.values()
                ]
            ),
            dash.page_container,
            dcc.Location(id="url", refresh=True),
        ]
    )
    return app


def test_pare001_relative_path(dash_duo):

    dash_duo.start_server(get_app(Dash(__name__, use_pages=True)))
    for page in dash.page_registry.values():
        dash_duo.find_element("#" + page["id"]).click()
        dash_duo.wait_for_text_to_equal("#text_" + page["id"], "text for " + page["id"])
        assert dash_duo.driver.title == page["title"], "check that page title updates"

    assert dash_duo.get_logs() == [], "browser console should contain no error"


def test_pare002_relative_path_with_url_base_pathname(dash_br, dash_thread_server):
    dash_thread_server(
        get_app(Dash(__name__, use_pages=True, url_base_pathname="/app1/"))
    )
    dash_br.server_url = f"http://localhost:{dash_thread_server.port}/app1/"

    for page in dash.page_registry.values():
        dash_br.find_element("#" + page["id"]).click()
        dash_br.wait_for_text_to_equal("#text_" + page["id"], "text for " + page["id"])
        assert dash_br.driver.title == page["title"], "check that page title updates"

    assert dash_br.get_logs() == [], "browser console should contain no error"
