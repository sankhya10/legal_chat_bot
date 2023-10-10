from textwrap import indent
from urllib import response
import streamlit as st
import pandas as pd

# from turtle import onclick
import itertools

# from agent_calculation import *
import pandas as pd
from streamlit_chat import message
from streamlit.components.v1 import html
import os
from langchain.chat_models import ChatOpenAI
from law_formulation import *
from streamlit_keycloak import login

st.set_page_config(
        page_title="Legally Yours: ChatBot",
        page_icon="🤖",
        layout="wide",
    )

tabs_font_css = """
<style>
div[class*="stTextInput"] label p {
  font-size: 36px;
  color: black;
}
</style>
"""
st.write(tabs_font_css, unsafe_allow_html=True)


def main():
    c30, c31, c32 = st.columns([2.5, 1, 3])
    with c30:
        # st.image("logo.png", width=400)
        st.markdown(
            """ <style> .font {
            font-size:36px ; font-family: 'Arial'; color: black; text-align: centre;} 
                </style> """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="font">🤖 Legally Yours:ChatBot</p>',
            unsafe_allow_html=True,
        )
        st.header("")

    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"
            "2. Optimized for GPT-4: 🚀 GPT-3 and 3.5 might encounter occasional quirks and problems\n"
            "3. OpenAI Api-key 👇"
        )
        api_key_input = st.text_input(
            "Open ai key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            label_visibility = "collapsed",
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )



    def clear_query():
        st.session_state.input_query = input_query
        st.session_state[str(10)] = ""


    def get_text(user_name):
        prompt = st.chat_input("Insert query")
        if prompt:
            return prompt


    def clear():
        st.session_state[str(1)] = ""
        st.session_state[str(2)] = 18


    if "open_api_key" not in st.session_state:
        st.session_state.open_api_key = api_key_input

    if "generated" not in st.session_state:
        st.session_state["generated"] = []

    if "past" not in st.session_state:
        st.session_state["past"] = []

    if "input_query" not in st.session_state:
        st.session_state["input_query"] = []


    def create_law_list(law_dict):
        business = []
        personal = []
        for item in law_dict["business-law"]:
            if isinstance(item, set):
                business.append(item[0])
            if isinstance(item, dict):
                business.append(list(item.keys()[0]))

        for item in law_dict["personal-law"]:
            if isinstance(item, set):
                personal.append(item[0])
            if isinstance(item, dict):
                personal.append(list(item.keys()[0]))
        return business, personal


    def create_legal_url(type, location, law_dict, expertise, third_key):
        business, personal = law_dict
        if third_key == None:
            for item in law_dict[f"{type}"]:
                if isinstance(item, set):
                    if expertise in item:
                        current_item = item.pop()
                        current_item = current_item.lower()
                        if " " in current_item:
                            current_item = current_item.replace(" ", "-")
                        if "personal" in type:
                            if current_item in business:
                                url = f"https://legallyyours.com.au/lawyers/?location={location}-personal-law&expertise={current_item}&specialised="
                                return url
                            else:
                                url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={current_item}&specialised="
                                return url
                        elif "business" in type:
                            url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={current_item}&specialised="
                            return url
                if isinstance(item, dict):
                    expertise = expertise.lower()
                    if " " in expertise:
                        expertise = expertise.replace(" ", "-")
                    if expertise in list(item.keys()):
                        if "personal" in type:
                            if list(item.keys())[0] in business:
                                url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={list(item.keys())[0]}-personal-law&specialised={list(item.values())[0]}"
                                return url
                            else:
                                url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={list(item.keys())[0]}&specialised={list(item.values())[0]}"
                                return url
                        elif "business" in type:
                            url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={list(item.keys())[0]}&specialised={list(item.values())[0]}"
                            return url
        else:
            if isinstance(third_key,str):
                third_key = third_key.lower()
                if " " in third_key:
                    third_key = third_key.replace(" ", "-")
                if "personal" in type:
                    if expertise in business:
                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={expertise}-personal-law&specialised={third_key}"
                        return url
                    else:
                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={expertise}&specialised={third_key}"
                        return url
                elif "business" in type:
                    url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={expertise}&specialised={third_key}"
                    return url
            elif isinstance(third_key,dict):
                if "personal" in type:
                    if list(third_key.keys())[0] in  business:
                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={list(third_key.keys())[0]}-personal-law&specialised={third_key[f'{list(third_key.keys())[0]}'][0]}"
                        return url
                    else:
                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={list(third_key.keys())[0]}&specialised={third_key[f'{list(third_key.keys())[0]}'][0]}"
                        return url
                elif "business" in type:
                    url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={list(third_key.keys())[0]}&specialised={third_key[f'{list(third_key.keys())[0]}'][0]}"
                    return url
            elif isinstance(third_key,set):
                third_key = next(iter(third_key))
                if isinstance(expertise,set):
                    expertise = next(iter(expertise))
                third_key = third_key.lower()
                if " " in third_key:
                    third_key = third_key.replace(" ", "-")
                if "personal" in type:
                    if expertise in business:
                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={expertise}-personal-law&specialised={third_key}"
                        return url
                    else:
                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={expertise}&specialised={third_key}"
                        return url
                elif "business" in type:
                    url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={expertise}&specialised={third_key}"
                    return url


    if __name__ == "__main__":
        option = st.selectbox(
            "Please select the jurisdiction of your lawyer ",
            options=(
                "",
                "australian-capital-territory",
                "nationwide",
                "new-south-wales",
                "victoria",
                "western-australia",
                "tasmania",
                "northern-territory",
                "queensland",
                "south-australia",
                "western-australia",
            ),
            index=0,
            placeholder="Choose a State",
        )
        st.write("You selected:", option)
        if option != "":
            input_query = []
            law_dict = create_lawyer_dict("keywords.html")

            placeholder = st.empty()
            user_name = "User"
            user_input = get_text(user_name)
            new_message = f"{user_name[0]} says {user_input}"

            if user_input != None:
                st.session_state["past"].append(user_input)
                if len(api_key_input) == 0:
                    st.warning("Please enter your OPEN-AI API key at sidebar and press enter",icon = "🚨")
                else:
                    if create_llm(api_key_input):
                        with placeholder.container():
                            message(user_input, is_user=True, key=str(19) + "_user")
                        refine = outline_guided(law_dict, user_input).content
                        refine = refine.lower()

                        with st.spinner("Generating response ..."):
                            if "not relevant" in refine:
                                not_relevant = "Sorry this query is out of scope for Legally:Yours,Please enter query relevant to our services"
                                st.session_state.generated.append(not_relevant)
                                with placeholder.container():
                                    message(user_input, is_user=True, key=str(30) + "_user")
                                    message(not_relevant, key=str(20))
                            else:
                                keywords = ["personal", "business", "business law", "personal law"]
                                pattern = "|".join(re.escape(keyword) for keyword in keywords)
                                what_law = create_agent_schema(keywords, user_input).content
                                matches = re.findall(pattern, what_law, flags=re.IGNORECASE)

                                if matches:
                                    if "business" in matches[0]:
                                        extracted_answer = refine_keywords(
                                            law_dict["business-law"], user_input
                                        ).content
                                        try:
                                            sec_key, third_key = search_dict_pattern(
                                                extracted_answer, user_input
                                            )
                                            if len(third_key) > 40:
                                                rel_answer = identify_answer(
                                                    law_dict["business-law"], third_key
                                                ).content
                                                st.write("Length of rel_answer", len(rel_answer))
                                                rel_answer = rel_answer.lower()
                                                if "no" in rel_answer:
                                                    url = create_legal_url(
                                                        "business-law",
                                                        option,
                                                        law_dict,
                                                        sec_key,
                                                        None,
                                                    )
                                                    response = f"""The keywords that you can explore : business-law :{sec_key} /
                                                                url: {url}"""
                                                else:
                                                    url = create_legal_url(
                                                        "business-law",
                                                        option,
                                                        law_dict,
                                                        sec_key,
                                                        rel_answer,
                                                    )
                                                    response = f"""The appropiate keywords for query are : business-law :{sec_key}:{rel_answer} /
                                                                url: {url}"""
                                            else:
                                                url = create_legal_url(
                                                    "business-law",
                                                    option,
                                                    law_dict,
                                                    sec_key,
                                                    third_key,
                                                )
                                                response = f"""The appropiate keywords for your query are : business-law : {sec_key} : {third_key} /
                                                            url: {url}"""

                                        except ValueError:
                                            answer = search_dict_pattern(
                                                extracted_answer, user_input
                                            )
                                            if len(answer) > 30:
                                                rel_answer = identify_answer(
                                                    law_dict["business-law"], answer
                                                ).content
                                                rel_answer = rel_answer.lower()
                                                if "no" in rel_answer:
                                                    response = "Sorry we can't find appropiate keywords for your query Please modify your query to blend with our services"
                                                else:
                                                    url = create_legal_url(
                                                        "business-law",
                                                        option,
                                                        law_dict,
                                                        rel_answer,
                                                        None,
                                                    )
                                                    response = f"""The appropiate keywords for query are : business-law :{rel_answer} /
                                                                    URL: {url}"""
                                            else:
                                                url = create_legal_url(
                                                    "business-law", option, law_dict, answer, None
                                                )
                                                response = f"""The appropiate keywords for query are : business-law :{answer} /
                                                            URL: {url}"""
                                        st.session_state.generated.append(response)
                                        with placeholder.container():
                                            message(user_input, is_user=True, key=str(28) + "_user")
                                            message(response, key=str(22))
                                    if "personal" in matches[0]:
                                        extracted_answer = refine_keywords(
                                            law_dict["personal-law"], user_input
                                        ).content
                                        try:
                                            sec_key, third_key = search_dict_pattern(
                                                extracted_answer, user_input
                                            )
                                            if len(third_key) > 40:
                                                rel_answer = identify_answer(
                                                    law_dict["personal-law"], third_key
                                                ).content
                                                # st.write("Length of rel_answer",len(rel_answer),rel_answer)
                                                rel_answer = rel_answer.lower()
                                                if "no" in rel_answer:
                                                    url = create_legal_url(
                                                        "personal-law",
                                                        option,
                                                        law_dict,
                                                        sec_key,
                                                        None,
                                                    )
                                                    response = f"""The keywords that you can explore : personal-law :{sec_key} /
                                                                    URL: {url}"""
                                                else:
                                                    url = create_legal_url(
                                                        "personal-law",
                                                        option,
                                                        law_dict,
                                                        sec_key,
                                                        rel_answer,
                                                    )
                                                    response = f"""The appropiate keywords for query are : personal-law :{sec_key}:{rel_answer} /
                                                                    URL:  {url}"""
                                            else:
                                                url = create_legal_url(
                                                    "personal-law",
                                                    option,
                                                    law_dict,
                                                    sec_key,
                                                    third_key,
                                                )
                                                response = f"""The appropiate keywords for your query are : personal-law : {sec_key} : {third_key} /
                                                            URL: {url}"""
                                        except ValueError:
                                            answer = search_dict_pattern(
                                                extracted_answer, user_input
                                            )
                                            if len(answer) > 30:
                                                rel_answer = identify_answer(
                                                    law_dict["personal-law"], answer
                                                ).content
                                                rel_answer = rel_answer.lower()
                                                if "no" in rel_answer:
                                                    response = "Sorry we can't find appropiate keywords for your query Please modify your query to blend with our services"
                                                else:
                                                    url = create_legal_url(
                                                        "personal-law",
                                                        option,
                                                        law_dict,
                                                        rel_answer,
                                                        None,
                                                    )
                                                    response = f"""The appropiate keywords for query are : personal-law :{rel_answer} /
                                                                    URL: {url}"""
                                            else:
                                                url = create_legal_url(
                                                    "personal-law", option, law_dict, answer, None
                                                )
                                                response = f"The appropiate keywords for query are : personal-law :{answer} url :{url}"
                                        st.session_state.generated.append(response)
                                        with placeholder.container():
                                            message(user_input, is_user=True, key=str(29) + "_user")
                                            message(response, key=str(25))



def check_password():
    """Returns `True` if the user had the correct password."""
    c36,c37,c38 = st.columns([1.3,2.8,1.3])
    with c37:
        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if st.session_state["password"] == st.secrets["password"]:
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # don't store password
            else:
                st.session_state["password_correct"] = False

        if "password_correct" not in st.session_state:
            # First run, show input for password.
            c37.text_input(
                "Enter the password for streamlit app", type="password", on_change=password_entered, key="password"
            )
            return False
        elif not st.session_state["password_correct"]:
            # Password not correct, show input + error.
            c37.text_input(
                "Enter the password for streamlit app", type="password", on_change=password_entered, key="password"
            )
            st.error("😕 Password incorrect")
            return False
        else:
            # Password correct.
            return True
if check_password():
    main()