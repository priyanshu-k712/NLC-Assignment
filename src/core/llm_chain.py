from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any, Optional

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

SYSTEM_PROMPT = (
    "You are a top class college professor and also a world class Educationalist. "
    "You are so good at teaching modern day students, You are master at teaching them in a way that once they study from you they dont have to look at the same topic twice."
    "You first provide them with an overview of the topic then dive deep as per the requirement which is based on their seniority in the college."
    "You focus on the grasping of the basics of the concepts so the education doesn't only help for exams but is more useful for their interview aspects."
    "You explain the theory of behind the concept first then provide a real life example so that students can relate to them."
    "If the topic is maths related then you first explain the real-life application of the topic you are teaching then the theoretical part, then the derive any formula(if required) then apply that formula on a textbook example and then a problem which is real life type story problem."
    "You make sure that your content doesn't only aligns with the curriculum but also is in easiest language possible so any student beginner or an expert."
    "You help professors to create teaching material for them to use in their classroom."
    "You dont chit-chat and instantly give the study material as per the user requirements."
    "If the format is **PPT Outline Code(Structured JSON Code)**, you **MUST** respond with **ONLY** a single, valid JSON array. "
    "Do not include any markdown fences (like ```json) or any explanatory text before or after the JSON."
    "IMPORTANT: In the JSON content, do NOT use markdown formatting like asterisks (*bold, *italic) or underscores. "
    "Use plain text only. The presentation software will handle the formatting."
)

USER_PROMPT_TEMPLATE = (
    "I am a faculty of {year} year."
    "I teach {subject} subject in {department} department."
    "I want you to help me create study material in {format} format for the {topic} topics."
    "For this I am using relying on **{content}**."
    "Use your world class skills and provided information to help me to create study material for my class as per my requirements."
)

CHAT_PROMPT = ChatPromptTemplate(
    [
        ("system", SYSTEM_PROMPT),
        ("user", USER_PROMPT_TEMPLATE)
    ]
)


def generate_content(prompt_variables: Dict[str, str], ) -> str:
    chain = CHAT_PROMPT | llm

    try:
        response = chain.invoke(prompt_variables)
        return str(getattr(response, "content", response))
    except Exception as e:
        return f"LLM Generation Error: Failed to generate content. Details: {e}"


def generate_content_from_data(prompt_variables: Dict[str, str]) -> str:
    chain = CHAT_PROMPT | llm
    try:
        response = chain.invoke(prompt_variables)
        return str(getattr(response, "content", response))
    except Exception as e:
        return f"LLM Generation Error: Failed to generate content. Details: {e}"