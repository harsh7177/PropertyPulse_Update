from scrap import scrap_city,sub_scrap,get_href_pages
import matplotlib.pyplot as plt
import streamlit as st
import json
from streamlit import session_state
from sql_href import create_href,href_tables,insert_href_table,get_href_data
from sql_details import detail_tables,get_detail_data,insert_detail_table,create_detail
from streamlit_lottie import st_lottie_spinner
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)

def load_lot(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)  
    
    

def city_page(loc1):
        
        if len(loc1)>0:
            try:
                tables=href_tables()
                table_names = [name.strip('"') for name in tables]
                loc1_table=f'{loc1}_href'
                if loc1_table in table_names:
                    df=get_href_data(loc1_table)
                    if len(df)==0:
                        df=scrap_city(loc1) 
                        insert_href_table(df,loc1)
                    else:
                        st.write("Data from AWS RDS")
                    df=df.rename(columns={'ProjectC':'ProjectCount'}) 
                    if True:
                        sort_df = df[['Area', 'ProjectCount']].sort_values('ProjectCount', ascending=False).head(10)
                        fig, ax = plt.subplots(figsize=(10,6))  # Adjust the size as needed
                        ax.bar(sort_df['Area'], sort_df['ProjectCount'])
                        ax.set_xlabel('Area')
                        ax.set_ylabel('Listed Properties')
                        ax.set_title('Top 10 Areas by Properties Count')
                        ax.tick_params(axis='x', rotation=90) 
                        plt.style.use('ggplot')     
                        st.pyplot(fig)
                        st.divider()
                else:
                    df=scrap_city(loc1) 
                    if len(df)>0:
                        create_href(loc1)
                    st.write("Data From AWS LAMBDA")
                    insert_href_table(df,loc1)
                    df=df.rename(columns={'ProjectC':'ProjectCount'}) 
                    if True:
                        sort_df = df[['Area', 'ProjectCount']].sort_values('ProjectCount', ascending=False).head(10)
                        fig, ax = plt.subplots(figsize=(10,6))  # Adjust the size as needed
                        ax.bar(sort_df['Area'], sort_df['ProjectCount'])
                        ax.set_xlabel('Area')
                        ax.set_ylabel('Listed Properties')
                        ax.set_title('Top 10 Areas by Properties Count')
                        ax.tick_params(axis='x', rotation=90) 
                        plt.style.use('ggplot')     
                        st.pyplot(fig)
                        st.divider()
            except Exception as e:
                st.write(e)



def suburbs_page(loc1):
    sns.set_style("whitegrid")
    sns.set_palette("colorblind")
    lottie_cod=load_lot("anime/Animation.json")
    df_href=get_href_data(loc1+'_href')
    df_href=df_href.dropna()
    suburb = st.selectbox("Select Suburbs/Area", ["None"]+df_href['Area'].to_list())
    session_state.suburb=suburb
    
    if suburb in df_href['Area'].to_list() :
        st.info("Every Time User Search for a Suburb AWS LAMBDA check  new data and insert it into Database,it may take a little time.")
        href_sub=df_href.loc[df_href['Area'] == suburb, 'href'].iloc[0]
        total_len=get_href_pages(href_sub)
        suburb=suburb.lower().replace(" ","_")
        table_name=loc1+"_"+suburb
        with st_lottie_spinner(lottie_cod):
            if table_name in detail_tables():
                df=get_detail_data(table_name)
                rds_len=len(df)
                
                if (rds_len+20) < total_len:
                    
                    start_page=int(rds_len/20) + 1
                    try:  
                        df1=sub_scrap(href_sub,start_page)
                        insert_detail_table(df1,table_name)
                        df = get_detail_data(loc1 +"_"+ suburb)
                        st.write(df)
                    except:
                        df=get_detail_data(loc1 +"_"+ suburb)
                        st.write(df)    
                else:
                    st.info('Data Powered By AWS RDS.')
                    df=get_detail_data(loc1+"_"+suburb)
                    st.write(df)
                    
            else:
                try:
                    df=sub_scrap(href_sub,pages='None')
                    if len(df)>20:
                        create_detail(table_name)
                        insert_detail_table(df,table_name)
                    st.write(df)
                    
                except Exception as e:
                    st.warning(e)
        if len(df)>0:
            sfig, axs = plt.subplots(1, 2, figsize=(12, 6))
            status_counts = df['Status'].value_counts()
            axs[0].bar(status_counts.index, status_counts.values)
            axs[0].set_xlabel('Status')
            axs[0].set_ylabel('Count')
            axs[0].set_title('Status Counts')
            bhk_counts = df['BHK'].value_counts()
            axs[1].bar(bhk_counts.index, bhk_counts.values)
            axs[1].set_xlabel('BHK')
            axs[1].set_ylabel('Count')
            axs[1].set_title('BHK Counts')
            plt.tight_layout()
            st.pyplot()
            st.caption(f"<b>This graph displays the distribution of 'Ready to Move' and 'Under Construction' properties across different BHK categories in {suburb}.</b>", unsafe_allow_html=True)
            st.divider()
            average_price_by_bhk = df.groupby('BHK')['Price'].mean()
            plt.bar(average_price_by_bhk.index, average_price_by_bhk.values)
            plt.xlabel('BHK')
            plt.ylabel('Average Price')
            plt.title('Average Price by BHK')
            st.pyplot()
            st.caption("Insights from the bar graph:")
            for i in range(len(average_price_by_bhk)):
                average_price_formatted = "{:,.2f}".format(average_price_by_bhk.values[i])
                st.caption(f"<b>Average Price of <b>{average_price_by_bhk.index[i]} BHK</b> in <b>{suburb}</b> is <b>₹{average_price_formatted}</b></b>", unsafe_allow_html=True)
            average_price = df.groupby(['BHK', 'Status'])['Price'].mean().unstack()
            st.divider()
            average_price.plot(kind='bar')
            plt.xlabel('BHK')
            plt.ylabel('Average Price')
            plt.title('Average Price by BHK and Status')
            plt.xticks(rotation=0)
            plt.legend(title='Status')
            st.pyplot()
            st.caption(f"<b>This graph illustrates the average  prices categorized by BHK configuration and status. It provides insights into the pricing dynamics based on the number of bedrooms (BHK) and the property's current status (Ready to Move or Under Construction) within the {suburb} area.</b>", unsafe_allow_html=True)
            st.divider()
            try:
                avg_price_per_project_bhk = df.groupby(['project', 'BHK'])['Price_Sqft'].mean().reset_index()
            except:
                df=df.rename(columns={'Price/Sqft'})
                avg_price_per_project_bhk = df.groupby(['project', 'BHK'])['Price_Sqft'].mean().reset_index()
            avg_price_per_project_bhk = avg_price_per_project_bhk.sort_values(by='Price_Sqft', ascending=False)
            top_10_projects_bhk = avg_price_per_project_bhk.head(10)
            bottom_10_projects_bhk = avg_price_per_project_bhk.tail(10)
            fig, ax = plt.subplots()
            ax.bar(top_10_projects_bhk['project'] + ' (' + top_10_projects_bhk['BHK'].astype(str) + ' BHK)',
                top_10_projects_bhk['Price_Sqft'], color='skyblue')
            ax.set_ylabel('Average Price')
            ax.set_xlabel('Project (BHK)')
            ax.set_title('Average Price of Top 10 Expensive Projects by BHK')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
            st.caption(f'Most Expensive Projects in {loc1.capitalize()} by Price/SqFt')
            st.divider()
            fig, ax = plt.subplots()
            ax.bar(bottom_10_projects_bhk['project'] + ' (' + bottom_10_projects_bhk['BHK'].astype(str) + ' BHK)',
                bottom_10_projects_bhk['Price_Sqft'], color='skyblue')
            ax.set_ylabel('Average Price')
            ax.set_xlabel('Project (BHK)')
            ax.set_title('Average Price of Top 10 Affordable Projects by BHK')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
            st.caption(f'Most Affordable Projects in {loc1.capitalize()} by Price/SqFt')
        elif suburb=="None":
            st.info('Select Suburb/Area of your city')
    
def about_page():
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='font-size: 36px; color: #333;'>Welcome to PropertyPulse</h1>
        <p style='font-size: 18px; color: #666; line-height: 1.6;'>
            PropertyPulse revolutionizes real estate insights with the seamless integration of AWS Lambda technology. No longer do users need to sift through countless listings or navigate confusing interfaces—PropertyPulse streamlines the real estate hunt by leveraging AWS Lambda for web scraping, delivering the latest property data tailored to your location with unparalleled efficiency.
        </p>
        <p style='font-size: 18px; color: #666; line-height: 1.6;'>
            With PropertyPulse, gaining access to a comprehensive overview of your local real estate landscape is as simple as a few clicks. From market trends to property listings, our app empowers users with a wealth of information at their fingertips, all thanks to the robust capabilities of AWS Lambda.
        </p>
        <p style='font-size: 18px; color: #666; line-height: 1.6;'>
            But the benefits don't end there. By harnessing the power of AWS Lambda, we go beyond mere data presentation. Through the integration of Exploratory Data Analysis (EDA), PropertyPulse provides users with insightful visualizations and analytics, enabling them to make informed decisions about buying, selling, or investing in real estate like never before.
        </p>
        <p style='font-size: 18px; color: #666; line-height: 1.6;'>
            And the future holds even greater promise. With AWS Lambda at the helm, PropertyPulse is poised to roll out cutting-edge predictive models, forecasting property prices, rental trends, and much more. Our vision is clear—to redefine the real estate landscape, one innovative feature at a time, all powered by the unparalleled capabilities of AWS Lambda.
        </p>
    </div>
    """, unsafe_allow_html=True)
