import base64
import requests
import json

import streamlit as st
from streamlit_option_menu import option_menu

from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import streamlit.components.v1 as components


st.set_page_config(page_title='Hitendra Vaghela', page_icon='🖖', initial_sidebar_state="collapsed", layout="wide")

ip = "http://" + os.environ.get("ip")

#ip = "http://##.###.###.##"
resume_ner_url = ip + ":443/resume-ner"
senti_url = ip + ":80/sentiment"
sent_score_url = ip + ":80/sent-sim"
text_summarization_url = ip + ":80/text-summary"
medical_ner_url = ip + ":80/medical-ner"
generic_ner_url = ip + ":80/generic-ner"

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def get_image_as_base64(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


lottie_pos = load_lottiefile("./lottie/107795-positive.json")
lottie_neg = load_lottiefile("./lottie/19640-negative.json")
lottie_summary = load_lottiefile("./lottie/90349-summary.json")
# MainMenu {visibility: hidden;}
# links, hide side bar and hide hamburger menu
html_snippet = """
    <style>
        [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{gap: 0rem;}        
        div[data-testid="stSidebarNav"] {display: none;}

        [data-testid="stAppViewContainer"]
    </style>
"""
st.markdown(html_snippet, unsafe_allow_html=True)

st.title("Hitendra Vaghela")
choose = option_menu("Data scientist", ["Text Analysis", "Machine Learning",  "Image Analysis"],
                     icons=['keyboard', 'house', 'file-person'],
                     menu_icon="laptop", default_index=0, orientation="horizontal",
                     styles={"container": {"background-color": "#007bbf"},  # light blue
                             "menu-title": {"color": "white"},
                             "menu-icon": {"color": "pink"},
                             "icon": {"color": "pink", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#fafafa", "color": "white"},  # white
                             "nav-link-selected": {"background-color": "#02ab21"}})  # green

if choose == "Machine Learning":
    col1, col2 = st.columns([7, 25])

    with col1:
        selected_sub_area = col1.radio("Select problem", ('Customer churn prediction',
                                                          'Demand Forecasting for cab',
                                                          ))
    with col2:
        if selected_sub_area == "Customer churn prediction":
            p = open("./data/customer_churn.html")
            components.html(p.read(), width=1000, height=500, scrolling=True)
        elif selected_sub_area == "Demand Forecasting for cab":
            p = open("./data/demand_forecasting_for_cab.html")
            components.html(p.read(), width=1000, height=500, scrolling=True)

elif choose == "Image Analysis":
    st.write("Coming soon...")
elif choose == "Text Analysis":
    col1, col2 = st.columns([7, 25])

    with col1:
        selected_sub_area = col1.radio("Select problem", ('Keywords extractor',
                                                          'Text Summarization', 'Sentiment Analysis',
                                                          'Text Semantic Similarity', 'Knowledge Graph Generator',
                                                          'Reading Comprehension'))
    if selected_sub_area in ["Knowledge Graph Generator', 'Reading Comprehension"]:
        st.write("Coming soon . . . ")
    if selected_sub_area == "Text Semantic Similarity":
        with col2:
            input_article_1 = st.selectbox("Example inputs", ('<select>',
                                                              'The cat is sitting on the mat.',
                                                              'I am running late for my meeting.',
                                                              'I am going to the store.'
                                                              ), key=1)
            input_article_2 = st.selectbox("Example inputs", ('<select>',
                                                              'The feline is lounging on the rug.',
                                                              'I am behind schedule for my appointment.',
                                                              'I am going to the park.'
                                                              ), key=2)
        if input_article_1 != '<select>':
            input_article1 = col2.text_area("Enter article for prediction (English language only)", input_article_1,
                                            key=3)
        else:
            input_article1 = col2.text_area("Enter article for prediction (English language only)", key=4)
        if input_article_2 != '<select>':
            input_article2 = col2.text_area("Enter article for prediction (English language only)", input_article_2,
                                            key=5)
        else:
            input_article2 = col2.text_area("Enter article for prediction (English language only)", key=6)
        if col2.button("Submit"):
            data = {'text1': input_article1, 'text2': input_article2}
            response = requests.post(sent_score_url, json=data)
            d = response.json()
            score = float(d["score"])
            with col2:
                if score > 0.5:
                    st_lottie(lottie_pos, loop=True, key="pos2", height=100, width=100, speed=1)
                    score_ = str(":green[") + str(round(score, 3)) + str("]")
                    st.markdown(score_)
                else:
                    st_lottie(lottie_neg, loop=True, key="neg2", height=100, width=100, speed=1)
                    score_ = str(":red[") + str(round(score, 3)) + str("]")
                    st.markdown(score_)

    elif selected_sub_area == "Text Summarization":
        with col2:
            input_article_1 = st.selectbox("Example inputs", ('<select>',
                                                              'The Bharat Jodo Yatra went from south to north but it '
                                                              'has had a countrywide effect, Congress leader Rahul '
                                                              'Gandhi said on Sunday, asserting the march have an '
                                                              'alternative vision to the country. Speaking at a '
                                                              'press conference after the march ended with the '
                                                              'hoisting of the tricolour at the Lal Chowk here, '
                                                              'Gandhi said he got to learn and understand a lot '
                                                              'during the over 4,000-km journey. He also said he '
                                                              'would think about whether a west to east yatra can be '
                                                              'undertaken in future.',
                                                              ), key=10)
    elif selected_sub_area == "Sentiment Analysis":
        with col2:
            input_article_1 = st.selectbox("Example inputs", ('<select>',
                                                              'You have amazing collection of Sneakers',
                                                              'Your support staff is useless',
                                                              'Product is ok I guess'
                                                              ))
    elif selected_sub_area == "Keywords extractor":
        with col2:
            selected_ner = col2.radio("Select problem", ('Generic', 'Resume', 'Medical'), horizontal = True)
        if selected_ner == "Resume":
            with col2:
                input_article_1 = st.selectbox("Example inputs", ('<select>',
                                                                   "Rahul Mahajan Application Development Associate - "
                                                                   "Accenture  Bengaluru, Karnataka - Email me on "
                                                                   "Indeed: "
                                                                   "indeed.com/r/Abhishek-Jha/10e7a8cb732bc43a  • To "
                                                                   "work for an organization that provides me the "
                                                                   "opportunity to improve my skills and knowledge "
                                                                   "for my individual and company's growth in best "
                                                                   "possible ways.  Willing to relocate to: "
                                                                   "Bangalore, Karnataka  WORK EXPERIENCE  "
                                                                   "Application Development Associate  Accenture -  "
                                                                   "November 2017 to Present  Role: Currently working "
                                                                   "on Chatbot. Developing Backend Oracle PeopleSoft "
                                                                   "Queries for the Bot which will be triggered based "
                                                                   "on a given input. Also, Train the bot for "
                                                                   "different possible utterances (Both positive and "
                                                                   "negative), which will be given as input by the "
                                                                   "user.  EDUCATION  B.E in Information science and "
                                                                   "engineering  B.v.b college of engineering and "
                                                                   "technology -  Hubli, Karnataka  August 2013 to "
                                                                   "June 2017  12th in Mathematics  Woodbine modern "
                                                                   "school  April 2011 to March 2013  10th  Kendriya "
                                                                   "Vidyalaya  April 2001 to March 2011  SKILLS  C ("
                                                                   "Less than 1 year), Database (Less than 1 year), "
                                                                   "Database Management (Less than 1 year), "
                                                                   "Database Management System (Less than 1 year), "
                                                                   "Java (Less than 1 year)  ADDITIONAL INFORMATION  "
                                                                   "Technical Skills  "
                                                                   "https://www.indeed.com/r/Abhishek-Jha"
                                                                   "/10e7a8cb732bc43a?isid=rex-download&ikw=download-top&co=IN   • Programming language: C, C++, Java • Oracle PeopleSoft • Internet Of Things • Machine Learning • Database Management System • Computer Networks • Operating System worked on: Linux, Windows, Mac  Non - Technical Skills  • Honest and Hard-Working • Tolerant and Flexible to Different Situations • Polite and Calm • Team-Player",
                                                                   "Koushik Katta Devops  Hyderabad, Telangana - Email me on Indeed: indeed.com/r/Koushik-Katta/a6b19244854199ec  DevOps Administrator with an experience of 3.4 years working in a challenging agile environment, looking forward for a position where I can use my knowledge pursuing my domain interests. I'm more aligned to work for companies where knowledge and intellectual ability takes the lead which can utilize a performance driven individual efficiently.  WORK EXPERIENCE  Devops Engineer  Infosys limited -  Hyderabad, Telangana -  December 2014 to Present  Hyderabad, since December 2014 to till date.  Skill and Abilities: Atlassian Tools: Jira, Confluence Configuration Management: Ansible /Chef CI Tools: Jenkins Monitoring Tools: Nagios Cloud: AWS Containerization: Docker Build Tools: Bamboo\\Maven Log Tools: Splunk Databases: RDBMS, MYSQL, Oracle Database Programming Languages: Python and Java Scripting: Power Shell Operating Systems: Windows, Linux family, Redhat Linux Middleware: Websphere, Tomcat, Websphere MQ  Responsibilities: DEVOPS ADMINISTRATOR INFOSYS LTD.  Atlassian tools Release Management according  Infosys limited -  December 2014 to Present  to project needs. ✓ Review and upgrade of Plugins to meet project requirements and to achieve better performance. ✓ Configuring Automated Mail handlers, Webhooks as POC to test the new demands raised by client.  https://www.indeed.com/r/Koushik-Katta/a6b19244854199ec?isid=rex-download&ikw=download-top&co=IN   ✓ JIRA Project Management/Administration. ✓ Confluence Space Management/Administration. ✓ Bitbucket Project/Repository Management/Administration (Enterprise/DataCenter) ✓ Integration of Webhooks in Bitbucket. ✓ Streamlining tools access management with Crowd. 2. Administration and Maintenance of Jenkins ✓ Configure and maintain Jenkins slaves as per the requirement. ✓ Jenkins release management. ✓ Work closely with Development teams to configure CI/CD Pipelines to automate their build & deployment process. ✓ Review, Installation/Upgrade and configuration of Jenkins Plugins. ✓ Configuring proxy on the environments to enable security ✓ Debug build issues 3. Administration and Maintenance of Docker registry 4. Working with Open-Source Nagios plugins on demand basis to setup ICINGA monitoring for our on-premise Servers/Applications. 5. Alerting Setup Splunk. 6. Monitoring Dashboards setup using kibana. 7. Working with product support teams to resolve the product bugs. 8. Involve in client meetings and tool performance reviews to ensure stakeholder satisfaction. 9. Work closely with Infrastructure Teams to setup/maintain/improve the above mentioned application on large scale.  EDUCATION  Bachelor Of Engineering in Mechanical Engineering  Lovely Professional University  2010 to 2014  Secondary School Certificate in education  Board of Intermediate education -  Hyderabad, Telangana  2008 to 2010  Sister Nivedita School -  Karimnagar, Telangana  2008  SKILLS  Jira, Ansible, Jenkins, Splunk, Nagios, Docker, Python, AWS, Bamboo, Linux, Git, Chef, Windows, Powershell Scripting  ADDITIONAL INFORMATION  • Ability to learn new technologies and processes rapidly and implement them in the project. • Highly motivated with very good problem solving and analytical skills Well organized, with excellent in multitasking and prioritizing the work.    • Effective communicator with an ability to convey ideas in speaking and writing. • Excellent analytical and decision making skills. • Ability to work in pressurized situation. • Hard worker and goal oriented. • Always ready to learn new skills"
                                                                   ))
        elif selected_ner == "Medical":
            with col2:
                input_article_1 = st.selectbox("Example inputs", ('<select>',
                                                                   "While bismuth compounds (Pepto-Bismol) decreased the number of bowel movements in those with travelers' diarrhea, they do not decrease the length of illness.[91] Anti-motility agents like loperamide are also effective at reducing the number of stools but not the duration of disease.[8] These agents should be used only if bloody diarrhea is not present.[92] Diosmectite, a natural aluminomagnesium silicate clay, is effective in alleviating symptoms of acute diarrhea in children,[93] and also has some effects in chronic functional diarrhea, radiation-induced diarrhea, and chemotherapy-induced diarrhea.[45] Another absorbent agent used for the treatment of mild diarrhea is kaopectate. Racecadotril an antisecretory medication may be used to treat diarrhea in children and adults.[86] It has better tolerability than loperamide, as it causes less constipation and flatulence.[94]"
                                                                   ))

        elif selected_ner == "Generic":
            with col2:
                input_article_1 = st.selectbox("Example inputs", ('<select>',
                                                                   'On August 10, 1961, Nikita S. Khrushchev, the premier of the Soviet Union, attended a birthday party in Moscow for Sergei S. Verentsov, the Soviet marshal in charge of the missile program of the Union of Soviet Socialist Republics. Khrushchev informed the celebrating assembly of leading Soviet military and political dignitaries that something momentous was about to occur.',
                                                                   'Nato chief on Tuesday said that they were confident that a solution on battle tanks for Ukraine would be achieved soon. He further added that there are no indications that Russian President Vladimir Putin has changed his goals on Ukraine. Stay with TOI for the latest updates.'
                                                                   ))
    if input_article_1 != '<select>':
        input_article = col2.text_area("Enter text for prediction (English language only)", input_article_1)
    else:
        input_article = col2.text_area("Enter text for prediction (English language only)")
    if len(input_article) == 0 or input_article.isspace():
        col2.warning('Please input a text.')
        st.stop()
    if selected_sub_area == "Text Summarization":
        max_ = col2.slider('Select max', 50, 500, step=10, value=150)
        min_ = col2.slider('Select min', 10, 450, step=10, value=50)
        do_sample_ = col2.checkbox("Do sample", value=False)

        data = {"text": input_article,
                "max": max_,
                "min": min_,
                "do_sample": do_sample_}

        if col2.button("Submit", key=11):
            with col2:
                with st_lottie_spinner(lottie_summary, loop=True, key="success", height=100, width=100, speed=1):
                    response = requests.post(text_summarization_url, json=data)
                    d = response.json()
                    col2.text_area(label="", value=d['summary'], height=100)

    elif col2.button("Submit", key=12):
        data = {"text": input_article}
        if selected_sub_area == "Sentiment Analysis":
            response = requests.post(senti_url, json=data)
            d = response.json()
            with col2:
                if d["label"] == "POSITIVE":
                    st_lottie(lottie_pos, loop=True, key="success", height=100, width=100, speed=1)
                    score_ = str(":green[") + str(round(d["score"], 3)) + str("]")
                    st.markdown(score_)
                elif d["label"] == "NEGATIVE":
                    st_lottie(lottie_neg, loop=False, key="neg", height=100, width=100, speed=1)
                    score_ = str(":red[") + str(round(d["score"], 3)) + str("]")
                    st.markdown(score_)
                else:
                    st_lottie(lottie_pos, loop=False, key="neutral", height=100, width=100, speed=1)
                    st.markdown(str(round(d['score'], 3)))
        elif selected_sub_area == "Keywords extractor":
            # Make a POST request to the API
            if selected_ner == "Medical":
                response = requests.post(medical_ner_url, json=data)
            elif selected_ner == "Resume":
                response = requests.post(resume_ner_url, json=data)
            elif selected_ner == "Generic":
                response = requests.post(generic_ner_url, json=data)

            col2.write(response.text, unsafe_allow_html=True)
