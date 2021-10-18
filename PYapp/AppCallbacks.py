from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash


def register_callbacks(app):
    ''' Manipulate Plot button clicked '''

    @app.callback(
        Output("manipulate_plot_contents", "is_open"),
        [Input("manipulate_plot_dropdown", "n_clicks")],
        [State("manipulate_plot_contents", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    ''' Select Data button clicked '''

    @app.callback(
        Output("select_data_contents", "is_open"),
        [Input("select_data_dropdown", "n_clicks")],
        [State("select_data_contents", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    ''' Loading of Data File - shows file name '''

    @app.callback(
        Output("data_file_name", "children"),
        [Input("selectDataBtn", "filename")],
    )
    def openDataFile(fname):
        """Load the selected file and return the name of file."""
        if fname is None:
            return [html.P("---")]

        print('emitting hdf5FileReadRequested(' + fname + ')')

        return [html.P(fname)]
