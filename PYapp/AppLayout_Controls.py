import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


class AppLayout_Controls:
    def __init__(self, *args, **kwargs):
        super(AppLayout_Controls, self).__init__(*args, **kwargs)

    def build_interior(self):
        # Control Panel
        layout = dbc.Col([
            # Load Required Data
            self.create_load_data(),

            html.Br(),

            self.create_manipulate_plot(),          

        ], width=3)

        return layout

    @staticmethod
    def create_load_data():
        return html.Div(
            [
                dbc.Button(
                    html.Span([html.I(className="fas fa-chevron-right ml-2"), '\t\bSelect Data']),
                    className="dropdown_btn",
                    id='select_data_dropdown',
                    color="light",
                    n_clicks=0,
                    block=True
                ),
                dbc.Collapse(

                    dbc.Container(
                        [
                            dbc.Row([
                                html.P("Select Data",
                                    className="header")
                            ], justify="center", align="center"),
                            dbc.Row([
                                dcc.Upload(id="selectDataBtn",
                                        children=dbc.Button("Select Data File", id="load_data", color="primary",
                                                            style={"margin": "5px"},
                                                            n_clicks_timestamp='0'))
                            ], justify="center", align="center"),
                            dbc.Row([
                                html.P(id="data_file_name")
                            ], justify="center", align="center"),

                            html.Hr(),

                            # Buttons: Project and export
                            dbc.Row([

                                dbc.Button("Project Data", id="project_data", color="primary", style={"margin": "5px"},
                                            n_clicks_timestamp='0')
                            ], justify="center", align="center")
                        ]),
                        
                    id='select_data_contents',
                    is_open=True
                    
                )                    
            ]
        )

    @staticmethod
    def create_manipulate_plot():
        # we use this function to make the example items to avoid code duplication
        return html.Div(
            [
                dbc.Button(
                    html.Span([html.I(className="fas fa-chevron-right ml-2"), '\t\bManipulate Plot']),
                    className="dropdown_btn",
                    id='manipulate_plot_dropdown',
                    color="light",
                    n_clicks=0,
                    block=True
                ),
                dbc.Collapse(

                    dbc.Container(
                        [
                            html.Br(),

                            # Sliders for Sphere size and alpha value
                            dbc.Row([
                                dbc.Col([
                                    html.P("Sphere Size"),
                                    dcc.Slider(
                                        id='sphere_size',
                                        min=1,
                                        max=50,
                                        step=1,
                                        value=5
                                    ),
                                ], className='column_left'),

                                dbc.Col([
                                    html.P("Alpha Value"),
                                    dcc.Slider(
                                        id='alpha_value',
                                        min=1,
                                        max=100,
                                        step=1,
                                        value=15
                                    ),
                                ]),
                            ])
                        ]
                    ),
                    id='manipulate_plot_contents',
                    is_open=True
                )
            ]
        )