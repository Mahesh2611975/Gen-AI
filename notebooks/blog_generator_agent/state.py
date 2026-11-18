from pydantic import BaseModel

class BlogState(BaseModel):
    #### User Imput
    topic: str =""
    audience: str ="general reader"

    ### Researcher Output
    research: str = ""
    research_feedback: str = ""


    ### Writer Output
    draft: str = ""
    research_feedback: str = ""

    ### Editor Output
    final_blog: str = ""


    ### Metadata
    revision_count: int = 0


