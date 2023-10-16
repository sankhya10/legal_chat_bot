import streamlit as st
import pandas as pd
from streamlit_chat import message
import os
from law_formulation import *
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

st.set_page_config(
        page_title="Legally Yours: ChatBot",
        page_icon="🤖",
        layout="wide",
    )


os.environ['AZURE_CLIENT_ID'] = st.secrets["client_id"]
os.environ['AZURE_TENANT_ID'] = st.secrets["tenant_id"]
os.environ['AZURE_CLIENT_SECRET']= st.secrets["secret_id"]

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

    
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=st.secrets["vault_url"], credential=credential)

    
    api_key = client.get_secret("openai-key")
    api_key_input = api_key.value



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
                business.append(next(iter(item)))
            if isinstance(item, dict):
                business.append(list(item.keys())[0])

        for item in law_dict["personal-law"]:
            if isinstance(item, set):
                personal.append(next(iter(item)))
            if isinstance(item, dict):
                personal.append(list(item.keys())[0])
        return business, personal


    def create_legal_url(type, location, law_dict, expertise, third_key):
        business, personal = create_law_list(law_dict)
        if third_key == None:
            for item in law_dict[f"{type}"]:
                if isinstance(item, set):
                    item_copy = next(iter(item))
                    item_copy = item_copy.lower()
                    expertise_copy = expertise.lower()
                    if expertise_copy in item_copy:
                        current_item = item.pop()
                        current_item = current_item.lower()
                        current_item = current_item.lstrip()
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
                        for key_pair,value_pair in item.items():
                            value_copy = value_pair
                            value_copy = [element.lower() for element in value_copy]
                            value_copy = [ments.lstrip() for ments in value_copy]
                            value_copy = [ele.replace(" ","-") for ele in value_copy]
                            expertise = expertise.lower()
                            expertise = expertise.lstrip()
                            if " " in expertise:
                                expertise = expertise.replace(" ", "-")
                            if expertise in key_pair:
                                if "personal" in type:
                                    if key_pair in business:
                                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={key_pair}-personal-law&specialised={value_copy[0]}"
                                        return url
                                    else:
                                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={key_pair}&specialised={value_copy[0]}"
                                        return url
                                elif "business" in type:
                                    url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={key_pair}&specialised={value_copy[0]}"
                                    return url  
                            elif expertise in value_copy:
                                if "personal" in type:
                                    if key_pair in business:
                                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={key_pair}-personal-law&specialised={expertise}"
                                        return url
                                    else:
                                        url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={key_pair}&specialised={expertise}"
                                        return url
                            elif "business" in type:
                                url = f"https://legallyyours.com.au/lawyers/?location={location}&expertise={key_pair}&specialised={expertise}"
                                return url
        else:
            if isinstance(third_key,str):
                third_key = third_key.lower()
                third_key = third_key.lstrip()
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
                    expertise = expertise.lower()
                    expertise = expertise.lstrip()
                    if " " in expertise:
                        expertise = expertise.replace(" ", "-")
                third_key = third_key.lower()
                third_key = third_key.lstrip()
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
            variations = []
            variation_response = {}
            law_dict = create_lawyer_dict("keywords.html")

            placeholder = st.empty()
            user_name = "User"
            user_input = get_text(user_name)
            input_copy = user_input
            
            if user_input != None:
                st.session_state["past"].append(user_input)
                if len(api_key_input) == 0:
                    st.warning("Please enter your OPEN-AI API key at sidebar and press enter",icon = "🚨")
                else:
                    if create_llm(api_key_input):
                        with placeholder.container():
                            message(user_input, is_user=True, key=str(19) + "_user")
                        if "lawyer" not in user_input:
                                user_input = user_input + " and I need a lawyer"
                        variations.append(user_input)        
                        variations.append(further_refine(user_input).content)
                        
                       

                        with st.spinner("Generating response ..."):
                            for vars in variations:
                                refine = outline_guided(law_dict, vars).content
                                refine = refine.lower()
                                if "not relevant" in refine:
                                    variation_response[vars] = False
                                    continue
                                else:
                                    keywords = ["personal", "business", "business law", "personal law"]
                                    pattern = "|".join(re.escape(keyword) for keyword in keywords)
                                    what_law = create_agent_schema(keywords, vars).content
                                    matches = re.findall(pattern, what_law, flags=re.IGNORECASE)

                                    if matches:
                                        if "business" in matches[0]:
                                            extracted_answer = refine_keywords(
                                                law_dict["business-law"], vars
                                            ).content
                                            if len(extracted_answer) == 2:
                                                variation_response[vars] = False
                                                continue
                                            else:
                                                try:
                                                    sec_key, third_key = search_dict_pattern(
                                                        extracted_answer, vars
                                                    )
                                                    if len(third_key) > 60:
                                                        rel_answer = identify_answer( 
                                                            law_dict["business-law"], third_key
                                                        ).content
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
                                                            variation_response[vars] = response
                                                            break
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
                                                            variation_response[vars] = response
                                                            break
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
                                                        variation_response[vars] = response
                                                        break
                                                except ValueError:
                                                    answer = search_dict_pattern(
                                                        extracted_answer, vars
                                                    )
                                                    if len(answer) > 60:
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
                                                if "Sorry" in response:
                                                    continue
                                                else:
                                                    variation_response[vars] = response
                                                    break
                                        if "personal" in matches[0]:
                                            extracted_answer = refine_keywords(
                                                law_dict["personal-law"], vars
                                            ).content
                                            if len(extracted_answer) == 2:
                                                variation_response[vars] = False
                                                continue
                                            else:        
                                                try:
                                                    sec_key, third_key = search_dict_pattern(
                                                        extracted_answer, vars
                                                    )
                                                    if len(third_key) > 60:
                                                        rel_answer = identify_answer(
                                                            law_dict["personal-law"], third_key
                                                        ).content
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
                                                            variation_response[vars] = response
                                                            break
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
                                                            variation_response[vars] = response
                                                            break
                                                    else:
                                                        url = create_legal_url(
                                                            "personal-law",
                                                            option,
                                                            law_dict,
                                                            sec_key,
                                                            third_key,
                                                        )
                                                        if isinstance(third_key,dict):
                                                            sec_key = list(third_key.keys())[0]
                                                            third_key = third_key[f'{list(third_key.keys())[0]}'][0]
                                                            response = f"""The appropiate keywords for your query are : personal-law : {sec_key} : {third_key} /
                                                                    URL: {create_legal_url("personal-law",option,law_dict,sec_key,third_key)}"""
                                                            variation_response[vars] = response
                                                            break
                                                        else:    
                                                            response = f"""The appropiate keywords for your query are : personal-law : {sec_key} : {third_key} /
                                                                        URL: {url}"""
                                                            variation_response[vars] = response
                                                            break
                                                except ValueError:
                                                    answer = search_dict_pattern(
                                                        extracted_answer, vars
                                                    )
                                                    if len(answer) > 60:
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
                                                if "Sorry" in response:
                                                    continue        
                                                else:
                                                    variation_response[vars] = response
                                                    break
                            if len(variation_response) == 0:
                                 response = "Sorry we can't find appropiate keywords for your query; Please modify your query to blend with our services"
                                 with placeholder.container():
                                    message(input_copy, is_user=True, key=str(31) + "_user")
                                    message(response, key=str(21))
                            else:
                                string_found = False
                                for value in variation_response.values():
                                    if isinstance(value, str):
                                        string_found = True
                                        with placeholder.container():
                                            message(input_copy, is_user=True, key=str(109) + "_user")
                                            message(value, key=str(189))
                                            break
                                if not string_found:
                                    response = "Sorry we can't find appropiate keywords for your query; Please modify your query to blend with our services"
                                    with placeholder.container():
                                        message(input_copy, is_user=True, key=str(898) + "_user")
                                        message(response,key = str(203))

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