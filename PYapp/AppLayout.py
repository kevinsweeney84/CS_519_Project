from PYapp.AppLayout_Controls import *


class AppLayout:
    def __init__(self, *args, **kwargs):
        super(AppLayout, self).__init__(*args, **kwargs)

        self.controls = AppLayout_Controls()

    def build_layout(self):
        layout = dbc.Container(
            [
                # Header of Dashboard
                self.create_header(),

                html.Hr(),

                # Body of Dashboard
                dbc.Row([
                    # VTK Widget
                    dbc.Col([
                        dbc.Spinner(
                            dcc.Graph(id='display', style={'height': '80vh'}),
                            color="primary"
                        )],
                        width=True,
                        className="column_left"),

                    # Control Panel
                    self.controls.build_interior(),
                ]),

                html.Hr(),

                # Footer of Dashboard
                self.create_footer(),
            ],
            fluid=True
        )

        return layout

    @staticmethod
    def create_header():
        return dbc.Row([
            dbc.Col([
                html.H2("Visualising Delaunay Triangulation"),
                html.H5("CS519"),
            ], width=True)
        ], align="end")

    @staticmethod
    def create_footer():
        return html.P([
            "Built by Kevin Sweeney & Saurabh Sharma "
        ])
