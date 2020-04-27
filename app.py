from flask import Flask, render_template, request
import sqlite3
import plotly.graph_objects as go
import final
from final import clean_tweets, compile_tweets, generate_word_cloud, make_request_with_cache, open_cache
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from io import BytesIO
import base64


app = Flask(__name__)

def generate_word_cloud(list_of_tweets):
    ''' creates a word cloud from a string of tweets

    Parameters
    ----------
    list_of_tweets: list
        list of tweets that are tokenized

    Returns
    -------
    a word cloud
        a word cloud of the 50 most-frequently used tokens in the list of tweets

    '''
    img = BytesIO()
    wordcloud_spam = WordCloud(font_path=None, width = 800, height=800,  
            max_words=100,  stopwords=None, background_color='whitesmoke', max_font_size=None, font_step=1, mode='RGB', 
            collocations=True, colormap=None, normalize_plurals=True).generate(list_of_tweets)
    plt.figure(figsize = (15,15))
    plt.imshow(wordcloud_spam, interpolation="nearest", aspect="equal")
    plt.axis("off")
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    word_cloud_url = base64.b64encode(img.getvalue()).decode('utf8')
    return word_cloud_url

def get_results(sort_by, sort_order, source_city, source_industry):
    conn = sqlite3.connect('mi_foot_traffic.db')
    cur = conn.cursor()

    where_clause = ''
    if (source_city == 'All'):
        if (source_industry != "All"):
            where_clause = f'where sub_category = "{source_industry}"'
    if (source_city != 'All'):
        if (source_industry == "All"):
            where_clause = f'where city = "{source_city}"'
    if (source_city != 'All'):
        if (source_industry != "All"):
            where_clause = f'where city = "{source_city}" and sub_category = "{source_industry}"'

    
    if sort_by == 'March Visits':
        sort_column = 'mvd.raw_visit_counts'
        q = f'''
        select places_of_interest.safegraph_place_id as "Unique ID", places_of_interest.location_name, 
        category.sub_category, places_of_interest.city,  
        dvd.raw_visit_counts, jvd.raw_visit_counts, fvd.raw_visit_counts, 
        {sort_column} from places_of_interest 
        inner join category on places_of_interest.naics_code=category.naics_code 
        inner join december_visitor_data dvd on places_of_interest.safegraph_place_id=dvd.safegraph_place_id 
        inner join january_visitor_data jvd on dvd.safegraph_place_id=jvd.safegraph_place_id 
        inner join february_visitor_data fvd on jvd.safegraph_place_id=fvd.safegraph_place_id
        inner join march_visitor_data mvd on fvd.safegraph_place_id=mvd.safegraph_place_id
        {where_clause}
        ORDER BY {sort_column} {sort_order}
        '''
        print(q)
        results = cur.execute(q).fetchall()
        conn.close()
        print(results)
        return results
    if sort_by == 'February Visits':
        sort_column= "fvd.raw_visit_counts"
        q = f'''
        select places_of_interest.safegraph_place_id as "Unique ID", places_of_interest.location_name, 
        category.sub_category, places_of_interest.city, 
        dvd.raw_visit_counts, jvd.raw_visit_counts, {sort_column}, 
        mvd.raw_visit_counts from places_of_interest 
        inner join category on places_of_interest.naics_code=category.naics_code 
        inner join december_visitor_data dvd on places_of_interest.safegraph_place_id=dvd.safegraph_place_id 
        inner join january_visitor_data jvd on dvd.safegraph_place_id=jvd.safegraph_place_id 
        inner join february_visitor_data fvd on jvd.safegraph_place_id=fvd.safegraph_place_id
        inner join march_visitor_data mvd on fvd.safegraph_place_id=mvd.safegraph_place_id
        {where_clause}
        ORDER BY {sort_column} {sort_order}
        '''
        print(q)
        results = cur.execute(q).fetchall()
        conn.close()
        print(results)
        return results
    if sort_by== "January Visits":
        sort_column= "jvd.raw_visit_counts"
        q = f'''
        select places_of_interest.safegraph_place_id as "Unique ID", places_of_interest.location_name, 
        category.sub_category, places_of_interest.city,  
        dvd.raw_visit_counts, {sort_column}, fvd.raw_visit_counts, 
        mvd.raw_visit_counts from places_of_interest 
        inner join category on places_of_interest.naics_code=category.naics_code 
        inner join december_visitor_data dvd on places_of_interest.safegraph_place_id=dvd.safegraph_place_id 
        inner join january_visitor_data jvd on dvd.safegraph_place_id=jvd.safegraph_place_id 
        inner join february_visitor_data fvd on jvd.safegraph_place_id=fvd.safegraph_place_id
        inner join march_visitor_data mvd on fvd.safegraph_place_id=mvd.safegraph_place_id
        {where_clause}
        ORDER BY {sort_column} {sort_order}
        '''
        print(q)
        results = cur.execute(q).fetchall()
        conn.close()
        print(results)
        return results

    if sort_by== "December Visits":
        sort_column = 'dvd.raw_visit_counts'
        q = f'''
        select places_of_interest.safegraph_place_id as "Unique ID", places_of_interest.location_name, 
        category.sub_category, places_of_interest.city,  
        {sort_column}, jvd.raw_visit_counts, fvd.raw_visit_counts, 
        mvd.raw_visit_counts from places_of_interest 
        inner join category on places_of_interest.naics_code=category.naics_code 
        inner join december_visitor_data dvd on places_of_interest.safegraph_place_id=dvd.safegraph_place_id 
        inner join january_visitor_data jvd on dvd.safegraph_place_id=jvd.safegraph_place_id 
        inner join february_visitor_data fvd on jvd.safegraph_place_id=fvd.safegraph_place_id
        inner join march_visitor_data mvd on fvd.safegraph_place_id=mvd.safegraph_place_id
        {where_clause}
        ORDER BY {sort_column} {sort_order}
        '''
        print(q)
        results = cur.execute(q).fetchall()
        conn.close()
        print(results)
        return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def bars():
        sort_by = request.form['sort']
        sort_order = request.form['dir']
        source_city = request.form['City']
        source_industry=request.form["Industry"]
        results = get_results(sort_by, sort_order, source_city, source_industry)
        plot_results = request.form.get('plot', False)
        if (plot_results):
            if sort_by == 'December Visits':
                y_vals = [r[4] for r in results]
            if sort_by == 'January Visits':
                y_vals = [r[5] for r in results]
            if sort_by == 'February Visits':
                y_vals = [r[6] for r in results]
            if sort_by == 'March Visits':
                y_vals = [r[7] for r in results]

            x_vals = [r[1] for r in results]
            bars_data = go.Bar(
                x=x_vals,
                y=y_vals
            )
            fig = go.Figure(data=bars_data)
            fig.update_layout(
                title=f"Michigan Foot Traffic for {sort_by}",
                xaxis_title="Business Name",
                yaxis_title="# of Visits",
                font=dict(
                    family="Lato, monospace",
                    size=12,
                    color="#7f7f7f"
                )
            )
            div = fig.to_html(full_html=False)
            return render_template("plot.html", plot_div=div)
        elif request.form.get('table',False):
            return render_template('results.html', 
            sort=sort_by, results=results,
            city=source_city, industry=source_industry)
        else:
            baseurl = "https://api.twitter.com/1.1/search/tweets.json"
            hashtag="#COVID19"
            cached=make_request_with_cache(baseurl,hashtag)
            compiled=compile_tweets(cached)
            cleaned=clean_tweets(compiled)
            return render_template('wordcloud.html', word_cloud_url=generate_word_cloud(cleaned))
    


@app.route('/wordcloud', methods=['POST'])
def word_cloud():
    return render_template("wordcloud.html")

if __name__ == '__main__':
    app.run(debug=True)

    