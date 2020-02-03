"""
Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.
It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.
"""
from flask import Flask #Flask is a class in the flask library
from flask import render_template #render_template accesses html files stored in the templates directory by the given url

app =Flask(__name__) #variable containing name of flask object instance

@app.route('/') #url to view website (decorater), http://localhost:5000/ is hosting the Website
def home():
    return render_template("home.html")

@app.route('/plot')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure,show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start=datetime.datetime(2019,10,8)
    end=datetime.datetime(2019,12,8)

    df=data.DataReader(name="AAPL",data_source="yahoo",start=start,end=end)#AAPL - Stock Symbol for Apple
    #Output of DataReader method is a Data frame

    #date_increase=df.index[df.Close < df.Open]
    #date_decrease=df.index[df.Close > df.Open]
    def inc_dec(c,o):
        if c>o:
            value="Increase"
        elif c<o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)
    df

    p=figure(x_axis_type='datetime',width=1000, height=300, sizing_mode='scale_width')
    p.title.text="Candlestick Chart"
    p.grid.grid_line_alpha=0.3

    hours_12=12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color="Black") #Params=xhigh,yhigh,xlow,ylow,color
    #Segments have to be added first if we want them to hide behind the rectangles

    p.rect(df.index[df.Status=="Increase"],df.Middle[df.Status=="Increase"], hours_12, df.Height[df.Status=="Increase"],fill_color="#50C878",line_color="black")
    #Param1=x_axis Values, Param2=y_axis Values, Param3=Rectangle_width(in ms),Param 4=Rect_height, Param5=Rect_color, Param6=line_color

    p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"], hours_12, df.Height[df.Status=="Decrease"],fill_color="#c41e3a",line_color="black")

    script1, div1 = components(p) #Gives a tuple of source code for JavaScript, second element is html

    cdn_js ="https://cdn.pydata.org/bokeh/release/bokeh-1.2.0.min.js"#CDN.js_files[0] # Gives Bokeh JS requirements
    cdn_css="https://cdn.pydata.org/bokeh/release/bokeh-1.2.0.min.css"#CDN.css_files[0]
    #These 4 are requirements to put Bokeh chart in Flask App
    return render_template("plot.html",script1=script1, div1=div1,cdn_css=cdn_css,cdn_js=cdn_js)

@app.route('/about/')
def about():
    return render_template("about.html")
    #return "About Page here!"

if __name__=="__main__":
    app.run(debug=True) # case 1: Script executed: __name__="__main__" case 2: Script imported" __name__="script" (name of this python file)
