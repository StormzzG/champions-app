import json
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

st.set_page_config(page_icon=':soccer:', page_title='Champions League-StormzzG',layout='wide')

st.title(":soccer: UEFA Champions League 2021/22 EDA")
st.markdown('<style>div.block-container{padding-top:2rem; margin-bottom:2rem}<style>',unsafe_allow_html=True)

home = option_menu(
    menu_icon=None,
    menu_title=None,
    options=['Developer Intro','Data Analysis'],
    icons=['person-fill','bar-chart-fill'],
    default_index=0,
    orientation='horizontal'
)

if home == 'Developer Intro':
    with open('Animation 1.json', 'r') as f:
        animation = json.load(f)
    col1,col2 = st.columns((2))
    with col1:
        st_lottie(
            animation,
            loop=True,
            quality='high',
            width=500,
            height=500,
            key='hello1'
        )
    with col2:
        st.markdown("<p style='text-align: center; font-family: Cursive; font-size: 20px; padding-top: 250px; margin-left: -350px;'>Hi there! My name is Stormy Ndonga, a Data Science Student at Moringa School Kenya.This is my Final Project Exploratory Data Analysis for the UEFA Champions League 2021/22. Click on the Data Analysis tab to have a look at it!</p>", unsafe_allow_html=True)
        st.write("<p style='margin-left: -215px; font-family: Cursive; font-size: 20px; margin-top:-20px; margin-bottom: -10px'> Another version of this project exists on my Github Profile, have a look at it here:</p>",unsafe_allow_html=True)
        st.write('https://github.com/StormzzG/Netflix-analysis')

if home == 'Data Analysis':
    with st.sidebar:
        selected = option_menu(
            menu_icon='house',
            menu_title='Home',
            options=['Attacking','Attempts','Defending','Distribution','Goals','Combined','UCL 1980'],
            icons=['circle','circle','circle','circle','circle','circle','circle'],
            default_index=0,
        )



    #--------------OPTION A-----------------#
    if selected == 'Attacking':
        attacking = pd.read_csv('attacking.csv')
        team = st.sidebar.multiselect('Pick Your Attacking Team', attacking['club'].unique())
        position = st.sidebar.multiselect('Pick Your Attacking Position', attacking['position'].unique())
        if team:
            a = attacking[attacking['club'].isin(team)]
        else:
            a = attacking.copy()
        
        if position:
            a1 = a[a['position'].isin(position)]
        else:
            a1= a.copy()

    
        #------------ATTACKING DATAFRAME------------------#
        st.subheader('Attacking Dataframe')
        st.dataframe(a1.style.background_gradient(cmap='Reds'),use_container_width=True)
        csv = a1.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, mime='csv', file_name='Attacking csv')
        
        #--------------ATTACKING CLUBS-----------------------#
        st.subheader('Attacking Points for Clubs')
        a1['points'] = a1['dribbles'] + a1['assists']
        attacking_clubs = a1.groupby(['club'],as_index=False)[['dribbles','assists','points']].sum().sort_values(by='points',ascending=False)
        mean = int(np.mean(attacking_clubs['points']))
        median = int(attacking_clubs['points'].median())
        fig1 = px.bar(attacking_clubs, x='club',y='points',hover_data=['dribbles','assists'])
        fig1.add_hline(y=mean, annotation_text='Mean', line_color='red')
        fig1.add_hline(y=median, annotation_text='Median', line_color='blue',annotation_position='bottom right')
        st.plotly_chart(fig1,use_container_width=True)
        st.write(f"{attacking_clubs.iloc[0]['club']} was the best attacking team")
        
        #--------------------ATTACKING PLAYERS----------------------------#
        st.subheader('Attacking Points for The Top Players')
        attacking_players = a1.groupby(['player_name'],as_index=False)[['points','dribbles','assists']].sum().sort_values(by='points',ascending=False)
        fig2 = px.bar(attacking_players.head(32),x='player_name',y='points',hover_data=['dribbles','assists'])
        mean2 = int(np.mean(attacking_players.head(32)['points']))
        median2 = int(attacking_players.head(32)['points'].median())
        fig2.add_hline(y=mean2, annotation_text='Mean', line_color='red')
        fig2.add_hline(y=median2, annotation_text='Median', line_color='blue',annotation_position='bottom right')
        st.plotly_chart(fig2,use_container_width=True)
        st.write(f"{attacking_players.iloc[0]['player_name']} was the best attacker")
        
        #--------------------------ATTACKING POSITIONS----------------------#    
        st.subheader('Attacking Points for Player Positions')
        attacking_positions = a1.groupby(['position'],as_index=False)[['points','dribbles','assists']].sum()
        fig3 = px.bar(attacking_positions,x='position',y='points',hover_data=['dribbles','assists'])
        st.plotly_chart(fig3,use_container_width=True)

        #------------PLAYER POSITION WORK RATE-----------------#
        st.subheader('Player Position Work Rate: Attacking Points vs Matches Played')
        fig4 = px.box(a1, x='match_played',y='points',color='position')
        st.plotly_chart(fig4,use_container_width=True)



    #--------------OPTION B-----------------#
    elif selected == 'Attempts':
        attempts = pd.read_csv('attempts.csv')
        team2 = st.sidebar.multiselect('Pick Your Attempts Team', attempts['club'].unique())
        position2 = st.sidebar.multiselect('Pick Your Attempts Position', attempts['position'].unique())
        if team2:
            b = attempts[attempts['club'].isin(team2)]
        else:
            b = attempts.copy()

        if position2:
            a2 = b[b['position'].isin(position2)]
        else:
            a2 = b.copy()
        
        #------------ATTEMPTS DATAFRAME-----------------------#
        st.header('Attempts Dataframe')
        st.dataframe(a2.style.background_gradient(cmap='Oranges'),use_container_width=True)
        csv = a2.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data',data=csv, mime='csv', file_name='Attempts csv')
        
        #----------ATTEMPTS PER CLUB-------------------------#
        st.subheader('Attempts Per Club')
        attempts_clubs = a2.groupby(['club'],as_index=False)[['on_target','off_target','blocked','total_attempts']].sum().sort_values(by='total_attempts',ascending=False)
        fig4 = px.bar(attempts_clubs, x='club',y='total_attempts',hover_data=['on_target','off_target','blocked'])
        mean = int(attempts_clubs['total_attempts'].mean())
        median = int(attempts_clubs['total_attempts'].median())
        fig4.add_hline(y=mean, annotation_text='Mean', line_color='red')
        fig4.add_hline(y=median, annotation_text='Median', line_color='blue',annotation_position='bottom right')
        st.plotly_chart(fig4,use_container_width=True)
        st.write(f"{attempts_clubs.iloc[0]['club']} Dominated Attempts")
        
        #------------ATTEMPTS PER PLAYER-------------------#
        st.subheader('Attempts Per Top Players')
        attempts_players = a2.groupby(['player_name'],as_index=False)[['on_target','off_target','blocked','total_attempts']].sum().sort_values(by='total_attempts',ascending=False)
        fig5 = px.bar(attempts_players.head(32), x='player_name',y='total_attempts',hover_data=['on_target','off_target','blocked'])
        mean2 = int(attempts_players.head(32)['total_attempts'].mean())
        median2 = int(attempts_players.head(32)['total_attempts'].median())
        fig5.add_hline(y=mean2, annotation_text='Mean', line_color='red')
        fig5.add_hline(y=median2, annotation_text='Median', line_color='blue',annotation_position='bottom right')
        st.plotly_chart(fig5,use_container_width=True)
        st.write(f"{attempts_players.iloc[0]['player_name']} Dominated Attempts")
        
        #------------PLAYER POSITION WORK RATE---------------#
        st.subheader('Player Position Work Rate: Total Attempts vs Matches Played')
        fig6 = px.box(a2, x='match_played', y='total_attempts',color='position')
        st.plotly_chart(fig6,use_container_width=True)



    #----------OPTION C------------#
    elif selected == 'Defending':
        defending = pd.read_csv('defending.csv')
        team3 = st.sidebar.multiselect('Pick Your Defending Team', defending['club'].unique())
        position3 = st.sidebar.multiselect('Pick Your Defending Position', defending['position'].unique())
        if team3:
            d = defending[defending['club'].isin(team3)]
        else:
            d = defending.copy()

        if position3:
            d1 = d[d['position'].isin(position3)]
        else:
            d1=d.copy()

        #----------DEFENDING DATAFRAME---------------#
        st.header('Defending Dataframe')
        st.dataframe(d1.style.background_gradient(cmap='Blues'),use_container_width=True)
        csv = d1.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, mime='csv', file_name='Defending csv')

        #-----------DEFENDING TEAM------------------#
        st.subheader('Defending Clubs')
        d1['points'] = d1['balls_recoverd'] + d1['t_won']
        defending_clubs = d1.groupby(['club'],as_index=False)[['balls_recoverd','t_won','points']].sum().sort_values(by='points',ascending=False)
        fig1 = px.bar(defending_clubs,x='club',y='points',hover_data=['balls_recoverd','t_won'])
        mean = int(np.mean(defending_clubs['points']))
        median = int(defending_clubs['points'].median())
        fig1.add_hline(y=mean, annotation_text='Mean', line_color='red')
        fig1.add_hline(y=median, annotation_text='Median', line_color='blue',annotation_position='bottom right')
        st.plotly_chart(fig1,use_container_width=True)
        st.write(f"{defending_clubs.iloc[0]['club']} was the best defending team")

        #-----------DEFENDING PLAYERS------------------#
        st.subheader('Defending Points For Top Players')
        defending_players = d1.groupby(['player_name'],as_index=False)[['balls_recoverd','t_won','points']].sum().sort_values(by='points',ascending=False)
        fig2 = px.bar(defending_players.head(32),x='player_name',y='points',hover_data=['balls_recoverd','t_won'])
        mean2 = int(np.mean(defending_players.head(32)['points']))
        median2 = int(defending_players.head(32)['points'].median())
        fig2.add_hline(y=mean2, annotation_text='Mean', line_color='red')
        fig2.add_hline(y=median2, annotation_text='Median', line_color='blue',annotation_position='bottom right')
        st.plotly_chart(fig2,use_container_width=True)
        st.write(f"{defending_players.iloc[0]['player_name']} was the best defending player")

        #------------PLAYER POSITION WORK RATE-------------#
        st.subheader('Player Position Work Rate: Matches Played vs Defending Points')
        fig3 = px.box(d1,x='match_played',y='points',color='position')
        st.plotly_chart(fig3,use_container_width=True)



    #-------------OPTION D-----------------#
    elif selected == 'Distribution':
        distribution = pd.read_csv('distributon.csv')
        team = st.sidebar.multiselect('Pick Your Distribution Team', distribution['club'].unique())
        position = st.sidebar.multiselect('Pick Your Distribution Position', distribution['position'].unique())
        if team:
            d = distribution[distribution['club'].isin(team)]
        else:
            d = distribution.copy()

        if position:
            d2 = d[d['position'].isin(position)]
        else:
            d2 = d.copy()

        #--------------DISTRIBUTION DATAFRAME------------#
        st.header('Distribution Dataframe')
        st.dataframe(d2.style.background_gradient(cmap='Greens'),use_container_width=True)
        csv = d2.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, mime='csv',file_name='Distribution csv')

        #-------------DISTRIBUTION TEAM----------------#
        st.subheader('Distribution Points Per Team')
        d2['points'] = d2['pass_completed'] + d2['cross_accuracy'] + d2['cross_complted']
        distribution_clubs = d2.groupby(['club'],as_index=False)[['points','pass_completed','cross_accuracy','cross_complted']].sum().sort_values(by='points',ascending=False)
        fig1 = px.treemap(distribution_clubs,path=[px.Constant('All Teams'), 'club'],values='points',hover_data=['pass_completed','cross_accuracy','cross_complted'])
        fig1.update_layout(height=600)
        fig1.update_traces(root_color='darkorange')
        st.plotly_chart(fig1,use_container_width=True)
        st.write(f"{distribution_clubs.iloc[0]['club']} was the best at distribution")

        #-------------DISTRIBUTION PLAYERS------------#
        st.markdown('Highest Pass Accuracy')
        st.write(d2[d2['pass_accuracy']==d2['pass_accuracy'].max()].style.background_gradient(cmap='Greens'))
        #Most passes Completed
        st.markdown('Most Passes Completed')
        st.write(d2[d2['pass_completed']==d2['pass_completed'].max()].style.background_gradient(cmap='Greens'))
        #Highest Cross Accuracy
        st.markdown('Highest Cross Accuracy')
        st.write(d2[d2['cross_accuracy']==d2['cross_accuracy'].max()].style.background_gradient(cmap='Greens'))

        #------------PLAYER WORK RATE------------------#
        st.subheader('Player Position Work Rate: Matches Played vs Distribution Points')
        fig2 = px.box(d2, x='match_played',y='points',color='position')
        st.plotly_chart(fig2,use_container_width=True)
        


    #---------------OPTION E-------------------#
    elif selected == 'Goals':
        goals = pd.read_csv('goals.csv')
        team = st.sidebar.multiselect("Pick Your Goals' Team",goals['club'].unique())
        position = st.sidebar.multiselect("Pick Your Goals' Position", goals['position'].unique())
        if team:
            g = goals[goals['club'].isin(team)]
        else:
            g = goals.copy()
        
        if position:
            g1 = g[g['position'].isin(position)]
        else:
            g1 = g.copy()

        #----------GOALS DATAFRAME-------------#
        st.header('Goals Dataframe')
        st.dataframe(g1.style.background_gradient(cmap='YlOrRd'),use_container_width=True)
        csv = g1.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, mime='csv', file_name='Goals csv')

        #------------GOALS CLUBS---------------------#
        st.subheader('Goals Per Club')
        goals_clubs = g1.groupby(['club'],as_index=False)[['inside_area','outside_areas','goals']].sum().sort_values(by='goals',ascending=False)
        fig1 = px.treemap(goals_clubs, path=[px.Constant('All Teams'), 'club'], values='goals',hover_data=['inside_area','outside_areas'])
        fig1.update_layout(height=600)
        fig1.update_traces(root_color='darkorange')
        st.plotly_chart(fig1,use_container_width=True)
        st.write(f"{goals_clubs.iloc[0]['club']} had the most goals")

        #--------------GOALS PLAYERS-----------------#
        st.subheader('Goals Per Player')
        goals_players = g1.sort_values(by=['goals'],ascending=False)
        fig2 = px.bar(goals_players.head(32),x='player_name',y='goals',hover_data=['inside_area','outside_areas'])
        mean = int(np.mean(goals_players.head(32)['goals']))
        median = int(goals_players.head(32)['goals'].median())
        fig2.add_hline(y=mean, annotation_text='Mean', line_color='red')
        fig2.add_hline(y=median, annotation_text='Median', line_color='blue',annotation_position='bottom right')
        st.plotly_chart(fig2,use_container_width=True)
        st.write(f"{goals_players.iloc[0]['player_name']} was a menace")

        #-------------POSITIONAL GOALS---------------------#
        st.subheader('Player Position Goals')
        goals_position = g1.groupby(['position'],as_index=False)[['inside_area','outside_areas','goals']].sum().sort_values(by='goals',ascending=False)    
        fig3 = px.bar(goals_position,x='position',y='goals',hover_data=['inside_area','outside_areas'])
        mean3 = int(np.mean(goals_position['goals']))
        median3 = int(goals_position['goals'].median())
        fig3.add_hline(y=mean3, annotation_text='Mean', line_color='red')
        fig3.add_hline(y=median3, annotation_text='Median', line_color='blue')
        st.plotly_chart(fig3,use_container_width=True)
        st.write(f"{goals_position.iloc[0]['position']}s scored the most goals")

        #----------------PLAYER POSITION WORK RATE-----------------#
        st.subheader('Player Position Work Rate: Matches Played vs Goals')
        fig4 = px.box(g1, x='match_played',y='goals',color='position')
        st.plotly_chart(fig4,use_container_width=True)
    
    #---------------OPTION F-------------#
    elif selected == 'Combined':
        disciplinary = pd.read_csv('disciplinary.csv')
        goalkeeping = pd.read_csv('goalkeeping.csv')

        dteam = st.sidebar.multiselect('Pick Your Disciplinary Team', disciplinary['club'].unique())
        dposition = st.sidebar.multiselect('Pick Your Disciplinary Position', disciplinary['position'].unique())
        if dteam:
            df = disciplinary[disciplinary['club'].isin(dteam)]
        else:
            df = disciplinary.copy()
        
        if dposition:
            df1 = df[df['position'].isin(dposition)]
        else:
            df1 = df.copy()
        
        gteam = st.sidebar.multiselect('Pick Your Goalkeeping Team',goalkeeping['club'].unique())
        if gteam:
            gf1 = goalkeeping[goalkeeping['club'].isin(gteam)]
        else:
            gf1 = goalkeeping.copy()

        #---------------DISCIPLINARY DATAFRAME------------------#
        st.header('Disciplinary Dataframe')
        st.dataframe(df1.style.background_gradient(cmap='winter'),use_container_width=True)
        csv = df1.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, mime='csv', file_name='Disciplinary csv')

        #-----------DISCIPLINARY PLAYERS------------#
        st.subheader('Discipline Among Players')
        df1['total'] = df1['fouls_committed'] + df1['red'] + df1['yellow']
        df1.sort_values(by=['total'],ascending=False)
        fig1 = px.bar(df1.head(32),x='player_name',y='total',hover_data=['fouls_committed','red','yellow'])
        st.plotly_chart(fig1,use_container_width=True)
        st.write(f"{df1.iloc[0]['player_name']} was the most notorious")

        #----------DISCIPLINARY CLUBS----------------#
        st.subheader('Discipline Among Clubs')
        discipline_clubs = df1.groupby(['club'],as_index=False)[['fouls_committed','red','yellow','total']].sum().sort_values(by='total',ascending=False)
        fig2 = px.bar(discipline_clubs,x='club',y='total',hover_data=['fouls_committed','red','yellow'])
        st.plotly_chart(fig2,use_container_width=True)
        st.write(f"{discipline_clubs.iloc[0]['club']} was the most notorious")


        #----------------GOALKEEPING DATAFRAME-----------------------------#
        st.header('Goalkeeping Dataframe')
        st.dataframe(gf1.style.background_gradient(cmap='copper'),use_container_width=True)
        csv = gf1.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, mime='csv', file_name='Goalkeeping csv')

        #------GOALKEEPING PLAYERS------------------#
        st.subheader('Goalkeeping Player Points')
        gf1['points'] = gf1['saved'] + gf1['saved_penalties'] + gf1['cleansheets']
        gf1_sorted = gf1.sort_values(by='points',ascending=False)
        fig3 = px.bar(gf1_sorted.head(32), x='player_name',y='points',hover_data=['saved','saved_penalties','cleansheets'])
        st.plotly_chart(fig3,use_container_width=True)
        st.write(f"{gf1_sorted.iloc[0]['player_name']} was the best goalkeeper")

    #---------------OPTION G-------------------------#
    elif selected == 'UCL 1980':
        quarters = pd.read_csv('UCLQuarterFinals.csv')
        #Sorting out columns
        quarters['year'] = quarters['year'].astype(int)
        quarters.drop(['metropol','ecb','cowc'],axis=1,inplace=True)
        quarters['country'].fillna('None',inplace=True)
        quarters['eurostat'].fillna('None',inplace=True)
        quarters['pop'].fillna(quarters['pop'].mean(),inplace=True)
        quarters['gdp'].fillna(quarters['gdp'].mean(),inplace=True)
        quarters['cown'].fillna(quarters['cown'].mean(),inplace=True)

        st.header('UCLQuarters Dataframe')
        year = st.sidebar.multiselect('Pick Year',quarters['year'].unique())
        league = st.sidebar.multiselect('Pick League',quarters['league'].unique())
        if year:
            d = quarters[quarters['year'].isin(year)]
        else:
            d = quarters.copy()

        if league:
            df = d[d['league'].isin(league)]
        else:
            df = d.copy()

        #----------Quarters Dataframe-------------------------#
        st.dataframe(df.style.background_gradient(cmap='cool'),use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, mime='csv', file_name='Quarters csv')

        #-------------LEAGUE PERFORMANCES---------------#
        st.subheader('Qualified Leagues Performances')
        fig = px.histogram(df, x='league')
        st.plotly_chart(fig,use_container_width=True)
        