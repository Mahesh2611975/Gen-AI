import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

#### GET LLM

def get_llm(model_name: str = "openai/gpt-oss-20b", temperature: float = 0.5):
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model=model_name, temperature=temperature, api_key=api_key)
    return llm



#### Researcher Agent
RESEARCHER_PROMPT = ChatPromptTemplate.from_messages([
    {"role":"system", "content":"""
        
        "You are a Researcher Agent. given a blog topic and target audience, produce a clear,structured reseaarch outline. unclude:\n"
        "1. 5-7 key points the blog should cover\n"
        "2. Important facts, stats, or examples for each point\n"
        "3. Suggested angle or hook\n"
        "Be concide. use Bullet points. Do NOT write the full blog yet."

     """},
    {"role":"user", "content":"Topic: {topic}, Audience: {audience}, {revision_hints}, Write the research outline now."}
])


def researcher_agent(llm:ChatGroq, topic: str, audience: str, feedback:str = ""):
    revision_hints = f"The human provided this feedback on your previous research - please address it: {feedback}."
    if not feedback:
        revision_hints = "This is your first attempt."

    chain = RESEARCHER_PROMPT | llm

    result = chain.invoke({
        "topic": topic,
        "audience": audience,
        "revision_hints": revision_hints    
    })

    return result.content



#### Writter Agent
WRITER_PROMPT = ChatPromptTemplate.from_messages([
    {"role":"system", "content":"""
        
        "You are a blog Writer Agent. Using the researcher note provided , write a complete,engaging blog post.\n" 
        "Rules:\n"
        "- Length: Approximately 500-700 words\n"
        "- structure:catchi title, intro hooks, 3-5 sections with H2 headings, conclusion\n"
        "-Tone: clear friendly, suited to the target audience\n"
        "-Use markdown formatting\n"
        "-Do NOT add a 'Word count' line ar the end"

     """},
    {"role":"user", "content":"""
            Topic: {topic}, 
            Audience: {audience},
            Research Notes: {research},
            {revision_hints},
            Write the blog post now.
     """}
])


def writer_agent(llm:ChatGroq, topic: str, audience: str, research: str = "", feedback:str = "") -> str:
    revision_hints = f"The human provided this feedback on your previous draft and asked for these changes {feedback}. Please apply these changes during writting the blog."

    if not feedback:
        revision_hints = "This is your first attempt."

    chain = WRITER_PROMPT | llm

    result = chain.invoke({
        "topic": topic,
        "audience": audience,
        "research": research,
        "revision_hints": revision_hints    
    })

    return result.content


#### Editor Agent


EDITOR_PROMPT = ChatPromptTemplate.from_messages([
    {"role":"system", "content":"""
        
        "You are a Editor Agent -The final quality gate before publishing.\n" 
        "Take the draft and produce the FINAL polished version. specifically:\n"
        
        "- Fix grammar , spelling and awkward phrasing\n"
        "- Tighten words sentences\n"
        "-Improve flow and trasaction between sections\n"
        "-make the title and intro more compelling if needed\n"
        "-Keep the same strucuture and markdown formatting\n"
        "-Blog Wordings should look like human, not a Ai, and dont't use any special chars and complex / fancy words.\n"
        "Output only the final polished blog post - no commentary."

     """},
    {"role":"user", "content":"""
            Topic: {topic}, 
            Audience: {audience},
            Draft: {draft},
            
            return the published blog post.
     """}
])


def editor_agent(llm:ChatGroq, topic: str, audience: str, draft: str = "") -> str:
    

    chain = EDITOR_PROMPT | llm

    result = chain.invoke({
        "topic": topic,
        "audience": audience,
        "draft": draft
           
    })

    return result.content
