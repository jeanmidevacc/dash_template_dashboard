
import os
import datetime
import random
import json


import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_auth
import plotly.graph_objs as go
import plotly.figure_factory as ff

import pandas as pd
import numpy as np

import external as ext

# Get the name of the tabs, and their assciated id
dict_tabs={
    "Tabulation_1":"tab1",
    "Tabulation_2":"tab2"
}

# Prepare the Authentification
allowed_users= json.load(open('config.json'))
VALID_USERNAME_PASSWORD_PAIRS = []
for user in allowed_users:
    VALID_USERNAME_PASSWORD_PAIRS.append([user,allowed_users[user]])

# Setup the app
app = dash.Dash('JMDashboard')
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server

#Load the css
for source in ["https://codepen.io/jeanmidevacc/pen/paxKzB.css","https://codepen.io/pixinema/pen/XZvJyX.css"]:
    app.css.append_css({"external_url": source})


app.config['suppress_callback_exceptions']=True

#Setup the layout of the app
app.layout = html.Div([
    html.H1('Personal dashboard'),
    html.Div(
            id='div_tabs',
            children=[
                dcc.Tabs(
                    tabs=[{'label':i , 'value': dict_tabs[i]} for i in dict_tabs],
                    value="tab1",
                    id='tabs',
                    vertical=False
                )
            ],
            ),
    html.Div(id="tab_output")
])

#Setttings the callback for a new tab selection
@app.callback(dash.dependencies.Output('tab_output', 'children'),
              [dash.dependencies.Input('tabs', 'value')])
def display_tab(value):
    print(value)
    if value=="tab1":
        return display_tab1()
    elif value=="tab2":
        return display_tab2()
    else:
        return dcc.Graph(id="tab-default",figure={'layout':go.Layout(title="NO DATA")})

# Function to display the content of the first tab
def display_tab1():
    # Setup the key figures
    list_value=[]
    for param in ["Param 1","Param 2"]:
        # Create the data to display
        list_elt=ext.get_kf(param)
        # Create the html object
        index=ext.get_keyindex("#86c0e3","kg",list_elt)
        elt_value=html.Div(className="col-xs-6 card",children=[index])
        # Store the html object
        list_value.append(elt_value)
    # Display the key figures
    kf=html.Div(className="row cards index",children=list_value)

    # Create a random dataframe
    random_df=pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

    # Create the html table that withe dataframe inside
    table=html.Div(className="table table-bordered table-striped",children=[ext.generate_table(random_df)])

    # Setup all the html objects to display
    list_childrens=[html.H2("Test index"),kf,html.H2("Random table"),table]

    return html.Div(id="tab1",children=list_childrens)

# Function to display the second tab
def display_tab2():
    # Create a data picker
    date_range=dcc.DatePickerRange(
        id='date-picker-range',
        start_date=(datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d"),
        end_date=datetime.datetime.now().strftime("%Y-%m-%d"),
        min_date_allowed='2014-01-01',
        max_date_allowed=datetime.datetime.now().strftime("%Y-%m-%d")
    )
    # Create a dropdown menu
    dropdown_parameter=dcc.Dropdown(
            id='dropdown-param',
            className="dropdown",
            options=[{'label':i , 'value': i} for i in range(1,10,2)],
            value=2)

    # Store all my dcc component in a html object
    input_date=html.Div(className='col-xs-6 card',children=[html.Ul(children=[html.Span('Period')]),html.Ul(children=[date_range])])
    input_parameter=html.Div(className='col-xs-6 card',children=[html.Ul(children=[html.Span('Factor')]),html.Ul(children=[dropdown_parameter])])

    # Settings the input panel in a html object
    input_settings=html.Div(className='row cards inputs',children=[html.H3("Inputs"),input_parameter,input_date])

    # Create a random plot
    list_plot=[html.H2(id="title-fig"),dcc.Graph(id='graph-figure')]

    # Setup all the html objects to display
    list_childrens=[input_settings]+list_plot

    print(list_childrens)

    return html.Div(id="tab2",children=list_childrens)


# First callback to get a dynamic title in function of the date selected and the fector in the dropdown menu
@app.callback(dash.dependencies.Output('title-fig', 'children'),
              [dash.dependencies.Input('date-picker-range', 'start_date'),
              dash.dependencies.Input('date-picker-range', 'end_date'),
              dash.dependencies.Input('dropdown-param', 'value')])
def display_title(start_date,end_date,param):
    print(start_date,end_date,param)
    start_date=datetime.datetime.strptime(start_date,"%Y-%m-%d")
    end_date=datetime.datetime.strptime(end_date,"%Y-%m-%d")
    title=html.Div("Impact of factor {} ({} to {})".format(param,start_date.strftime("%Y-%m-%d"),end_date.strftime("%Y-%m-%d")))
    print(title)
    return [title]


# Second callback to get the random plot based on the inputs
@app.callback(dash.dependencies.Output('graph-figure', 'figure'),
              [dash.dependencies.Input('date-picker-range', 'start_date'),
              dash.dependencies.Input('date-picker-range', 'end_date'),
              dash.dependencies.Input('dropdown-param', 'value')])
def display_graph(start_date,end_date,param):
    print(start_date,end_date,param)
    start_date=datetime.datetime.strptime(start_date,"%Y-%m-%d")
    end_date=datetime.datetime.strptime(end_date,"%Y-%m-%d")


    date_range=pd.date_range(start_date,end_date)

    random_df=pd.DataFrame(np.random.randint(0,10*param,size=(len(date_range), 3)),index=date_range, columns=list('ABC'))

    data=[]
    for col in random_df.columns:
        data.append({
            "x":random_df.index,
            "y":random_df[col],
            'name':col
        })


    figure1= {
        'data':data,
        'layout':{
            'autosize':True,
            'yaxis':{
                'title':"Random value"
            },
            'legend':{
                'orientation':'h'
            }

            }
    }

    return figure1



# Launch the app
if __name__ == '__main__':
    app.run_server(debug=True)
